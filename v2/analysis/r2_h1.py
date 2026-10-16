"""R2-H1 — Registered Revision 2 for H1 (ANALYSIS_PLAN_v2_ADDENDUM_2.md: R7, R10, R11).

Revision 1 model and data (R4 band fixed effects and conflict, R5 water rule), with
  * covariate matching on relative height and WorldCover shares (primary unless fewer than 25 % of
    flooded pixels are matched: then the unmatched estimate is primary — the overlap rule),
  * placebo in time: matching on 2016–2018 NDVI, "effect" for 2019–2021 on 2016–2021,
  * the unmatched estimate (all flooded pixels against all candidate controls),
  * event studies relative to the 2016–2018 mean and to 2021, Conley errors at 25/50/100 km.
Output: outputs/v2/r2_h1_results.json
"""
import json
import os
import sys
import time

import numpy as np
import xarray as xr
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
import a3_h1 as H1  # noqa: E402
import r1_h1 as R1H1  # noqa: E402
import r2lib as R2L  # noqa: E402

OUT = "outputs/v2"
YRS = np.array(L.YEARS)
WC_COV = ["tree", "shrub", "grass", "crop", "built", "bare", "water", "wetland"]


def covariates(H, R1, R2):
    idx = H["idx"]
    wc = xr.open_dataset(f"{L.D}/worldcover_2021_fractions.nc")
    cols = [R2["relh_dnipro"].ravel()[idx]]
    for c in WC_COV:
        v = wc[f"frac_{c}"].values.ravel()[idx].astype(np.float32)
        cols.append(np.where(v == 255, np.nan, v))
    wc.close()
    return np.column_stack(cols).astype(np.float64), ["relative_height_m"] + [f"wc_{c}_pct" for c in WC_COV]


def match_on(Z, H, treat, ctrl, k=3, caliper_sd=0.25, seed=1):
    """H1.match with an arbitrary matching matrix Z (rows = pixels): Mahalanobis distance within
    bank x dominant-class strata, k controls with replacement, caliper 0.25 SD of the distances of
    random treated–control pairs in the stratum. Columns without variance in a stratum are dropped there."""
    complete = np.isfinite(Z).all(1)
    stratum = H["bank"].astype(int) * 100 + H["dom"].astype(int)
    w = np.zeros(len(Z))
    rng = np.random.default_rng(seed)
    diag = {"treated_in": int(treat.sum()), "treated_complete": int((treat & complete).sum()),
            "matched_treated": 0, "unmatched_by_caliper": 0, "no_controls_in_stratum": 0}
    for s in np.unique(stratum[treat]):
        ti = np.flatnonzero(treat & complete & (stratum == s))
        ci = np.flatnonzero(ctrl & complete & (stratum == s))
        if len(ti) == 0:
            continue
        if len(ci) < k:
            diag["no_controls_in_stratum"] += len(ti)
            continue
        Zs = np.vstack([Z[ti], Z[ci]])
        sd = Zs.std(0)
        keep = sd > 1e-9
        Zs = (Zs[:, keep] - Zs[:, keep].mean(0)) / sd[keep]
        S = np.cov(Zs, rowvar=False).reshape(keep.sum(), keep.sum()) + 1e-9 * np.eye(keep.sum())
        Wm = np.linalg.cholesky(np.linalg.inv(S))
        zt, zc = Zs[:len(ti)] @ Wm, Zs[len(ti):] @ Wm
        a = rng.integers(0, len(ti), 20000)
        b = rng.integers(0, len(ci), 20000)
        cal = caliper_sd * np.std(np.linalg.norm(zt[a] - zc[b], axis=1))
        dist, nn = cKDTree(zc).query(zt, k=k)
        ok = dist <= cal
        nmatch = ok.sum(1)
        got = nmatch > 0
        diag["unmatched_by_caliper"] += int((~got).sum())
        diag["matched_treated"] += int(got.sum())
        w[ti[got]] = 1.0
        for r in np.flatnonzero(got):
            for q in range(k):
                if ok[r, q]:
                    w[ci[nn[r, q]]] += 1.0 / nmatch[r]
    diag["share_of_flooded_matched"] = diag["matched_treated"] / max(diag["treated_in"], 1)
    return w, diag


def smd(Z, names, treat, w):
    out = {}
    for j, n in enumerate(names):
        v = Z[:, j]
        t, c = treat & np.isfinite(v), (~treat) & np.isfinite(v)
        sd = np.sqrt((np.nanvar(v[t]) + np.nanvar(v[c])) / 2) or 1.0
        cm = c & (w > 0)
        out[n] = {"smd_before": float((v[t].mean() - v[c].mean()) / sd),
                  "smd_after": float((v[t & (w > 0)].mean() - np.average(v[cm], weights=w[cm])) / sd) if cm.any() else None}
    return out


def build(H, treat, w, years, terms, event=False, min_years=None):
    """Revision 1 H1 model on a subset of years: pixel FE, year x (bank x class) FE, year x 2 km
    channel-band FE, weather, conflict; treatment terms F x (years in terms[name])."""
    yk = np.isin(YRS, years)
    Y = H["ndvi_jo"][:, yk]
    mn = (L.MIN_YEARS if len(years) == 9 else len(years) - 1) if min_years is None else min_years
    u = np.flatnonzero((w > 0) & (np.isfinite(Y).sum(1) >= mn))
    Yu = Y[u]
    N, Tn = Yu.shape
    rep = lambda a: np.repeat(np.asarray(a)[u].astype(float)[:, None], Tn, 1)  # noqa: E731
    extra = {"F": rep(treat), "yr": np.tile(YRS[yk][None, :].astype(float), (N, 1)), "P": H["P"][u][:, yk],
             "Tm": H["T"][u][:, yk], "strat": rep(H["bank"].astype(int) * 100 + H["dom"].astype(int)),
             "blk": rep(H["block"]), "w": rep(w), "band": rep(H["band"]), "CI": H["CI"][u][:, yk]}
    lf = L.long_format(Yu, extra)
    yrs = lf["yr"].astype(int)
    cols, names = [], []
    if event:
        for y in years:
            if y != R2L.EV_DROP:
                cols.append(lf["F"] * (yrs == y))
                names.append(f"F_x_{y}")
    else:
        for n, yy in terms.items():
            cols.append(lf["F"] * np.isin(yrs, yy))
            names.append(n)
    cols += [lf["P"] / 100.0, lf["Tm"]]
    names += ["precip_100mm", "temp_C"]
    if np.any(lf["CI"] != 0):
        cols.append(lf["CI"])
        names.append("conflict_log1p_events_5km")
    groups = [lf["unit"], np.unique(lf["strat"].astype(int) * 10000 + yrs, return_inverse=True)[1],
              np.unique(lf["band"].astype(int) * 10000 + yrs, return_inverse=True)[1]]
    return lf, np.column_stack(cols), names, groups, u


def estimate(H, treat, w, years=L.YEARS, terms=None, full=True, B=9999):
    terms = terms or {"F_x_Post": L.POST, "F_x_War": L.WAR}
    lf, X, names, groups, u = build(H, treat, w, years, terms)
    fit = L.fe_ols(lf["y"], X, groups, lf["w"], lf["blk"].astype(int), names)
    b, se = float(fit["coef"][0]), float(fit["se"][0])
    r = {"term": names[0], "beta": b, "se_cluster": se, "p_cluster": float(fit["p"][0]),
         "ci95_cluster": [b - 1.96 * se, b + 1.96 * se], "n_obs": fit["n"], "n_pixels": int(len(u)),
         "n_treated_px": int(treat[u].sum()), "n_control_px": int((~treat[u]).sum()), "clusters": fit["G"],
         "coefs": {n: float(c) for n, c in zip(names, fit["coef"])}}
    if full:
        r["wcr"] = L.wild_cluster_p(fit, 0, B=B)
        xy = np.c_[H["col"][u] * R2L.RES, -H["row"][u] * R2L.RES]
        r["conley"] = R2L.conley_set(fit, 0, xy, lf["unit"], cell_m=2316.56)
    return r


def event(H, treat, w):
    lf, X, names, groups, u = build(H, treat, w, L.YEARS, None, event=True)
    fit = L.fe_ols(lf["y"], X, groups, lf["w"], lf["blk"].astype(int), names)
    return R2L.event_summary(fit, [y for y in L.YEARS if y != R2L.EV_DROP])


def main():
    t0 = time.time()
    if "--skip-check" not in sys.argv:
        R2L.check_addendum()
    H, R1, wr = R1H1.prepare()
    R2 = dict(np.load(f"{L.D}/derived/r2_layers.npz"))
    if "relh_dnipro" not in R2:
        sys.exit("r2_layers.npz has no DEM layer: run v2/10_download_dem.py, then r2_prepare.py.")
    F, C15 = H["F"].astype(bool), H["C15"].astype(bool)
    Z, znames = covariates(H, R1, R2)
    out = {"label": "registered revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md)", "water_rule": wr}

    # primary: covariate matching
    w, diag = match_on(Z, H, F, C15)
    out["covariate_matching"] = {"matching": diag}
    if diag["matched_treated"] >= 30:
        out["covariate_matching"].update({"balance_covariates": smd(Z, znames, F, w),
                                          "balance_ndvi_2016_2021": H1.balance(H, F, w)})
        out["matched"] = estimate(H, F, w)
        out["matched"]["event_study"] = event(H, F, w)
        print("R10 cov-matched", {k: out["matched"][k] for k in ("beta", "se_cluster", "n_treated_px")},
              "WCR", out["matched"]["wcr"]["p_two_sided"], round(time.time() - t0), flush=True)
    else:
        out["matched"] = {"skipped": f"only {diag['matched_treated']} flooded pixels matched"}
    # overlap rule (Addendum 2, R10): primary = matched if >= 25 % of flooded pixels are matched, else unmatched
    out["primary"] = "matched" if diag["share_of_flooded_matched"] >= 0.25 else "unmatched"

    # placebo in time: match on 2016–2018 NDVI, effect 2019–2021 on 2016–2021
    base_i = np.isin(YRS, R2L.BASE)
    wp, dp = match_on(H["ndvi_jo"][:, base_i].astype(np.float64), H, F, C15)
    out["placebo_in_time"] = estimate(H, F, wp, years=R2L.BASE + R2L.DEF, terms={"F_x_2019_2021": R2L.DEF})
    out["placebo_in_time"]["matching"] = dp
    print("placebo in time", out["placebo_in_time"]["beta"], out["placebo_in_time"]["p_cluster"], flush=True)

    # unmatched (area-representative)
    ones = (F | C15).astype(float)
    out["unmatched"] = estimate(H, F, ones)
    out["unmatched"]["event_study"] = event(H, F, ones)
    out["main"] = out[out["primary"]]
    out["seconds"] = round(time.time() - t0)
    os.makedirs(OUT, exist_ok=True)
    np.save(f"{L.D}/derived/r2_h1_cov_weights.npy", w)
    json.dump(out, open(f"{OUT}/r2_h1_results.json", "w"), indent=1)
    print("done", out["seconds"], "s")


if __name__ == "__main__":
    main()
