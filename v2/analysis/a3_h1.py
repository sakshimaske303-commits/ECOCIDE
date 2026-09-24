"""A3 — H1: matched flood design (plan §4.1, §6, §8).

    Y_iy = a_i + l_(y, bank x class) + b F_i Post_y + d F_i War_y + g'W_iy + e_iy

Main estimate, inference (cluster, WCR bootstrap, Conley), event study,
pre-trend test, Rambachan–Roth bounds, balance and all H1 robustness checks.
Output: outputs/v2/h1_results.json
"""
import json
import os
import sys
import time

import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import f as fdist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

YI = {y: i for i, y in enumerate(L.YEARS)}
PRE_I = [YI[y] for y in L.PRE]
OUT = "outputs/v2"
CLASSES = ["tree", "shrub", "grass", "crop", "built", "bare", "snow", "water", "wetland", "mangrove", "moss"]


def load():
    return dict(np.load(f"{L.D}/derived/h1_pixels.npz"))


def match(H, treat, ctrl, outcome="ndvi_jo", k=3, caliper_sd=0.25, seed=1):
    """Mahalanobis matching on the six pre-war (2016–2021) outcome values, within
    bank x dominant-class strata, k controls with replacement, caliper = 0.25 SD
    of the treated–control distance distribution in the stratum.
    Returns weights (treated 1, control sum of 1/k_i), and diagnostics."""
    Y = H[outcome]
    pre = Y[:, PRE_I]
    complete = np.isfinite(pre).all(1)
    stratum = H["bank"].astype(int) * 100 + H["dom"].astype(int)
    w = np.zeros(len(Y))
    rng = np.random.default_rng(seed)
    diag = {"treated_in": int(treat.sum()), "treated_complete_pre": int((treat & complete).sum()),
            "matched_treated": 0, "unmatched_by_caliper": 0, "no_controls_in_stratum": 0, "strata": {}}
    for s in np.unique(stratum[treat]):
        ti = np.flatnonzero(treat & complete & (stratum == s))
        ci = np.flatnonzero(ctrl & complete & (stratum == s))
        if len(ti) == 0:
            continue
        if len(ci) < k:
            diag["no_controls_in_stratum"] += len(ti)
            continue
        Z = np.vstack([pre[ti], pre[ci]])
        S = np.cov(Z, rowvar=False) + 1e-9 * np.eye(Z.shape[1])
        Wm = np.linalg.cholesky(np.linalg.inv(S))
        zt, zc = pre[ti] @ Wm, pre[ci] @ Wm
        # caliper: SD of distances between random treated–control pairs in the stratum
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
        diag["strata"][f"{'right' if s // 100 == 1 else 'left'}-{CLASSES[s % 100]}"] = {
            "treated": int(len(ti)), "matched": int(got.sum()), "controls_pool": int(len(ci)), "caliper": float(cal)}
    return w, diag


def balance(H, treat, w, outcome="ndvi_jo"):
    """Standardised mean differences of the six pre-war values, before and after matching."""
    pre = H[outcome][:, PRE_I]
    out = {}
    for k, y in enumerate(L.PRE):
        v = pre[:, k]
        t = treat & np.isfinite(v)
        c_all = (~treat) & np.isfinite(v)
        c_m = c_all & (w > 0)
        sd = np.sqrt((np.nanvar(v[t]) + np.nanvar(v[c_all])) / 2)
        mt = np.nanmean(v[t & (w > 0)])
        out[str(y)] = {
            "treated_mean": float(np.nanmean(v[t])),
            "control_mean_unmatched": float(np.nanmean(v[c_all])),
            "control_mean_matched": float(np.average(v[c_m], weights=w[c_m])),
            "smd_before": float((np.nanmean(v[t]) - np.nanmean(v[c_all])) / sd),
            "smd_after": float((mt - np.average(v[c_m], weights=w[c_m])) / sd),
        }
    return out


def build(H, treat, w, outcome="ndvi_jo", use_weather=True, event=False, sub=None):
    Y = H[outcome].copy()
    keepu = (w > 0) & (np.isfinite(Y).sum(1) >= L.MIN_YEARS)
    if sub is not None:
        keepu &= sub
    u = np.flatnonzero(keepu)
    Yu = Y[u]
    N, T = Yu.shape
    Fm = np.repeat(treat[u].astype(float)[:, None], T, 1)
    yr = np.tile(np.array(L.YEARS)[None, :], (N, 1))
    extra = {"F": Fm, "yr": yr.astype(float), "P": H["P"][u], "Tm": H["T"][u],
             "strat": np.repeat((H["bank"][u].astype(int) * 100 + H["dom"][u].astype(int))[:, None], T, 1).astype(float),
             "blk": np.repeat(H["block"][u][:, None], T, 1).astype(float),
             "w": np.repeat(w[u][:, None], T, 1)}
    lf = L.long_format(Yu, extra)
    yrs = lf["yr"].astype(int)
    if event:
        cols, names = [], []
        for y in L.YEARS:
            if y == 2021:
                continue
            cols.append(lf["F"] * (yrs == y))
            names.append(f"F_x_{y}")
    else:
        cols = [lf["F"] * np.isin(yrs, L.POST), lf["F"] * np.isin(yrs, L.WAR)]
        names = ["F_x_Post", "F_x_War"]
    if use_weather:
        cols += [lf["P"] / 100.0, lf["Tm"]]
        names += ["precip_100mm", "temp_C"]
    X = np.column_stack(cols)
    ys = np.unique(lf["strat"].astype(int) * 10000 + yrs, return_inverse=True)[1]
    groups = [lf["unit"], ys]
    return lf, X, names, groups, u


def estimate(H, treat, w, outcome="ndvi_jo", use_weather=True, sub=None, full=False, B=9999):
    lf, X, names, groups, u = build(H, treat, w, outcome, use_weather, sub=sub)
    fit = L.fe_ols(lf["y"], X, groups, lf["w"], lf["blk"].astype(int), names)
    j = 0
    b, se = fit["coef"][j], fit["se"][j]
    res = {"beta": float(b), "se_cluster": float(se), "p_cluster": float(fit["p"][j]),
           "ci95_cluster": [float(b - 1.96 * se), float(b + 1.96 * se)],
           "delta_war": float(fit["coef"][1]), "delta_war_se": float(fit["se"][1]), "delta_war_p": float(fit["p"][1]),
           "n_obs": fit["n"], "n_pixels": int(len(u)), "n_treated_px": int(treat[u].sum()),
           "n_control_px": int((~treat[u]).sum()), "clusters": fit["G"]}
    if len(names) > 2:
        res["weather_coef"] = {names[q]: float(fit["coef"][q]) for q in range(2, len(names))}
    pre_mean = np.nanmean(H[outcome][u][treat[u]][:, PRE_I])
    res["pre_mean_treated"] = float(pre_mean)
    res["beta_pct_of_pre_mean"] = float(b / pre_mean * 100)
    if full:
        res["wcr"] = L.wild_cluster_p(fit, j, B=B)
        xy = np.c_[H["col"][u] * 231.656358, -H["row"][u] * 231.656358]
        res["se_conley25km"] = L.conley_se(fit, j, xy, lf["unit"])
        res["p_conley25km"] = float(2 * L.norm.sf(abs(b / res["se_conley25km"])))
    return res


def event_study(H, treat, w, outcome="ndvi_jo", use_weather=True, sub=None):
    lf, X, names, groups, u = build(H, treat, w, outcome, use_weather, event=True, sub=sub)
    fit = L.fe_ols(lf["y"], X, groups, lf["w"], lf["blk"].astype(int), names)
    ev_years = [y for y in L.YEARS if y != 2021]
    k = len(ev_years)
    beta, V = fit["coef"][:k], fit["vcov"][:k, :k]
    pre_idx = [ev_years.index(y) for y in [2016, 2017, 2018, 2019, 2020]]
    bp, Vp = beta[pre_idx], V[np.ix_(pre_idx, pre_idx)]
    Wstat = float(bp @ np.linalg.solve(Vp, bp))
    q = len(pre_idx)
    Fstat = Wstat / q
    p_joint = float(fdist.sf(Fstat, q, fit["G"] - 1))
    rows = [{"year": y, "coef": float(beta[i]), "se": float(np.sqrt(V[i, i])), "p": float(fit["p"][i])}
            for i, y in enumerate(ev_years)]
    rr = L.rr_bounds(beta, V, ev_years, ref=2021, pre=[2016, 2017, 2018, 2019, 2020], post_targets=[2023, 2024])
    return {"coefs": rows, "reference": 2021, "pretrend_joint_F": Fstat, "pretrend_joint_p": p_joint,
            "pretrend_df": [q, fit["G"] - 1], "rambachan_roth": rr}


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    H = load()
    F, C15, C25, F25 = H["F"].astype(bool), H["C15"].astype(bool), H["C25"].astype(bool), H["F25"].astype(bool)
    R = {"design": "matched flooded vs unflooded pixels, same bank x dominant class; Mahalanobis on 2016–2021 Jul–Oct NDVI; 3:1 with replacement; caliper 0.25 SD"}

    w, diag = match(H, F, C15)
    R["matching"] = diag
    R["balance"] = balance(H, F, w)
    R["main"] = estimate(H, F, w, full=True)
    print("H1 main:", {k: R["main"][k] for k in ("beta", "se_cluster", "p_cluster", "n_pixels")},
          "WCR", R["main"]["wcr"]["p_two_sided"], "Conley SE", R["main"]["se_conley25km"])
    R["event_study"] = event_study(H, F, w)
    print("pretrend p", R["event_study"]["pretrend_joint_p"])

    rob = {}
    ones = (F | C15).astype(float)
    rob["1_no_matching"] = estimate(H, F, ones * (F | C15))
    w25, d25 = match(H, F, C25)
    rob["2_control_band_5_25km"] = estimate(H, F, w25)
    rob["2_control_band_5_25km"]["matched_treated"] = d25["matched_treated"]
    rob["3_no_weather"] = estimate(H, F, w, use_weather=False)
    wA, dA = match(H, F25, C15)
    rob["4a_flood_threshold_25pct"] = estimate(H, F25, wA)
    F75 = F & (H["flood"] >= 0.75)
    wB, dB = match(H, F75, C15)
    rob["4b_flood_threshold_75pct"] = estimate(H, F75, wB)
    wE, dE = match(H, F, C15, outcome="evi_jo")
    rob["6_evi"] = estimate(H, F, wE, outcome="evi_jo")
    rob["7a_right_bank"] = estimate(H, F, w, sub=H["bank"] == 1)
    rob["7b_left_bank"] = estimate(H, F, w, sub=H["bank"] == 2)
    for c in ("crop", "grass", "wetland", "tree"):
        ci = CLASSES.index(c)
        sub = H["dom"] == ci
        if (F & sub & (w > 0)).sum() >= 30:
            rob[f"8_class_{c}"] = estimate(H, F, w, sub=sub)
        else:
            rob[f"8_class_{c}"] = {"skipped": f"fewer than 30 matched flooded pixels ({int((F & sub & (w > 0)).sum())})"}
    rob["9_excl_within_3km_built"] = estimate(H, F, w, sub=H["dist_built"] > 3)
    # secondary outcomes (plan §5)
    sec = {}
    wja, _ = match(H, F, C15, outcome="ndvi_ja")
    sec["ndvi_jul_aug"] = estimate(H, F, wja, outcome="ndvi_ja")
    Hs = dict(H)
    Hs["ndvi_ao"] = H["ndvi_ao"].copy()
    Hs["ndvi_ao"][:, YI[2023]] = np.nan  # plan: April–October 2023 excluded (breach in June)
    wao, _ = match(Hs, F, C15, outcome="ndvi_ao")
    sec["ndvi_apr_oct_excl2023"] = estimate(Hs, F, wao, outcome="ndvi_ao")
    R["robustness"] = rob
    R["secondary"] = sec
    # EXPLORATORY (not in the plan; reported as such): matching without the caliper, and
    # unmatched estimates by dominant class, to show what the caliper-restricted sample leaves out
    exp = {}
    wn, dn = match(H, F, C15, caliper_sd=np.inf)
    exp["matched_no_caliper"] = estimate(H, F, wn, full=True)
    exp["matched_no_caliper"]["matched_treated"] = dn["matched_treated"]
    exp["matched_no_caliper"]["balance"] = balance(H, F, wn)
    exp["matched_no_caliper"]["event_study"] = event_study(H, F, wn)
    for c in ("crop", "grass", "wetland", "tree", "built"):
        sub = H["dom"] == CLASSES.index(c)
        nF = int((F & sub).sum())
        exp[f"no_matching_class_{c}"] = estimate(H, F, ones * (F | C15), sub=sub) if nF >= 30 else {"skipped": nF}
    R["exploratory"] = exp
    R["seconds"] = round(time.time() - t0)
    with open(f"{OUT}/h1_results.json", "w") as fh:
        json.dump(R, fh, indent=1)
    for k, v in rob.items():
        if "beta" in v:
            print(f"{k:30s} beta={v['beta']:+.4f} se={v['se_cluster']:.4f} p={v['p_cluster']:.4f} n={v['n_pixels']}")
    for k, v in sec.items():
        print(f"{k:30s} beta={v['beta']:+.4f} se={v['se_cluster']:.4f} p={v['p_cluster']:.4f}")
    print("seconds", R["seconds"])


if __name__ == "__main__":
    main()
