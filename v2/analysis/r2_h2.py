"""R2-H2 — Registered Revision 2 for H2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md: R6, R7, R9, R11).

Independent irrigation exposure (Baber et al. 2026b maps): canal-fed irrigated cropland vs never-irrigated
cropland in Kherson and Zaporizhzhia oblasts, 2023–24 vs 2016–2018, weather allowed to change the contrast,
raion-clustered inference, event study relative to 2016–2018, placebo test 2019–21 vs 2016–18, and (if
feasible) the triple difference with irrigated land that was not canal-fed.
Output: outputs/v2/r2_h2_results.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
import r2lib as R2L  # noqa: E402

OUT = "outputs/v2"
YRS = np.array(L.YEARS)
MIN_GROUP = 1000


def sample(A, R1, R2):
    base = R2["crop_r2"] & R2["two_oblasts"] & R2["covered"]
    canal = A["dist_net"] <= 30
    irr_any = base & (R2["irr_mean_1921"] >= 0.5)
    groups = {"irr_canal": irr_any & canal, "irr_other": irr_any & ~canal}
    never_all = base & (R2["irr_max_1921"] < 0.05)
    idx = np.flatnonzero((irr_any | never_all).ravel())
    Y = L.load_outcomes(idx)
    ok = R2L.fixed_panel(Y, L.MIN_YEARS)
    dist = R2["dist_field_km"].ravel()[idx]
    g_irr = groups["irr_canal"].ravel()[idx] & ok
    rule_km = 5
    g_never = never_all.ravel()[idx] & (dist > 5) & ok
    if g_irr.sum() < MIN_GROUP or g_never.sum() < MIN_GROUP:
        rule_km = 2
        g_never = never_all.ravel()[idx] & (dist > 2) & ok
    g_other = groups["irr_other"].ravel()[idx] & ok
    keep = g_irr | g_never | g_other
    idx, Y = idx[keep], Y[keep]
    rr, cc = np.unravel_index(idx, A["F"].shape)
    P, T = L.weather(A["lon"].ravel()[idx], A["lat"].ravel()[idx])
    ny = len(L.YEARS)
    H = {"idx": idx, "Y": Y, "P": P, "T": T, "row": rr, "col": cc,
         "irr": g_irr[keep], "never": g_never[keep], "other": g_other[keep],
         "canal": canal.ravel()[idx], "oblast": A["oblast"].ravel()[idx], "raion": R1["raion"].ravel()[idx],
         "block": A["block"].ravel()[idx],
         "occ": np.stack([R1["occupied"][k].ravel()[idx] for k in range(ny)], 1),
         "CI": np.stack([R1["conflict"][k].ravel()[idx] for k in range(ny)], 1),
         "irr_mean": R2["irr_mean_1921"].ravel()[idx]}
    info = {"never_distance_rule_km": rule_km, "pixels": {"irrigated_canal_fed": int(H["irr"].sum()),
            "never_irrigated": int(H["never"].sum()), "irrigated_not_canal_fed": int(H["other"].sum())}}
    return H, info


def centre(H, sel):
    """R6: P and T centred at their 2016–2021 means over the irrigated pixels of the sample."""
    pre = np.isin(YRS, L.PRE)
    m = H["irr"] & sel
    return float(np.nanmean(H["P"][m][:, pre])), float(np.nanmean(H["T"][m][:, pre]))


def build(H, sel, years, design="did", event=False, fixed=None):
    yk = np.isin(YRS, years)
    u = np.flatnonzero(sel)
    Y = H["Y"][u][:, yk]
    N, Tn = Y.shape
    rep = lambda a: np.repeat(np.asarray(a)[u].astype(np.float32)[:, None], Tn, 1)  # noqa: E731
    pm, tm = centre(H, sel)
    irr_any = (H["irr"] | H["other"]).astype(np.float32)
    ext = {"I": rep(H["irr"]) if design == "did" else rep(irr_any), "C": rep(H["canal"]), "IC": rep(H["irr"]),
           "ob": rep(H["oblast"]), "rai": rep(H["raion"]), "occ": H["occ"][u][:, yk].astype(np.float32),
           "CI": H["CI"][u][:, yk], "Pc": (H["P"][u][:, yk] - pm) / 100.0, "Tc": H["T"][u][:, yk] - tm,
           "yr": np.tile(YRS[yk].astype(np.float32)[None, :], (N, 1))}
    lf = L.long_format(Y, ext)
    yrs = lf["yr"].astype(int)
    T_ = lf["IC"] if design == "triple" else lf["I"]      # the treated indicator of the design
    cols, names = [], []
    if event:
        for y in years:
            if y != R2L.EV_DROP:
                cols.append(T_ * (yrs == y))
                names.append(f"T_x_{y}")
    else:
        # Post (2023–24) = beta, War (2022), Def (2019–21, the years that define the groups); baseline 2016–18.
        # On the placebo panel (2016–21) only Def is present and is the placebo "effect".
        for lab, yy in (("Post", L.POST), ("War", L.WAR), ("Def", R2L.DEF)):
            if any(y in years for y in yy):
                cols.append(T_ * np.isin(yrs, yy))
                names.append(f"T_x_{lab}")
    w_terms = [("Pc", lf["Pc"]), ("Tc", lf["Tc"])]
    inter = [("I", lf["I"])] + ([("C", lf["C"]), ("IC", lf["IC"])] if design == "triple" else [])
    for wn, wv in w_terms:
        cols.append(wv)
        names.append(wn)
        for gn, gv in inter:
            if fixed and f"{wn}_x_{gn}" in fixed:
                # event study (R7): with a full set of year x group indicators the weather x group slopes
                # are barely identified when weather varies mostly between years, so they are fixed at
                # their main-model estimates and taken off the outcome
                lf["y"] = lf["y"] - fixed[f"{wn}_x_{gn}"] * wv * gv
                continue
            cols.append(wv * gv)
            names.append(f"{wn}_x_{gn}")
    if np.any(lf["CI"] != 0):
        cols.append(lf["CI"])
        names.append("conflict_log1p_events_5km")
    X = np.column_stack(cols)
    groups = [lf["unit"],
              np.unique(lf["ob"].astype(int) * 10000 + yrs, return_inverse=True)[1],
              np.unique(lf["occ"].astype(int) * 10000 + yrs, return_inverse=True)[1]]
    if design == "triple":
        groups += [np.unique(lf["I"].astype(int) * 10000 + yrs, return_inverse=True)[1],
                   np.unique(lf["C"].astype(int) * 10000 + yrs, return_inverse=True)[1]]
    return lf, X, names, groups, u


def fit_model(H, sel, years, design="did", event=False, fixed=None):
    lf, X, names, groups, u = build(H, sel, years, design, event, fixed)
    fit = L.fe_ols(lf["y"], X, groups, np.ones(len(lf["y"])), lf["rai"].astype(int), names)
    return fit, lf, u


def report(fit, lf, u, H, j=0, full=True, B=9999):
    b, se = float(fit["coef"][j]), float(fit["se"][j])
    r = {"term": fit["names"][j], "beta": b, "se_cluster_raion": se, "p_cluster_raion": float(fit["p"][j]),
         "ci95_cluster": [b - 1.96 * se, b + 1.96 * se], "clusters_raion": fit["G"], "n_obs": fit["n"],
         "n_pixels": int(len(u)), "coefs": {n: float(c) for n, c in zip(fit["names"], fit["coef"])}}
    pre = np.isin(YRS, R2L.BASE)
    pm = float(np.nanmean(H["Y"][u][H["irr"][u]][:, pre]))
    r["base_mean_irrigated_2016_2018"] = pm
    r["beta_pct_of_base_mean"] = b / pm * 100
    if full:
        r["wcr"] = L.wild_cluster_p(fit, j, B=B)
        xy = np.c_[H["col"][u] * R2L.RES, -H["row"][u] * R2L.RES]
        r["conley"] = R2L.conley_set(fit, j, xy, lf["unit"])
    return r


def main():
    t0 = time.time()
    if "--skip-check" not in sys.argv:
        R2L.check_addendum()
    A = L.layers()
    R1 = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    R2 = dict(np.load(f"{L.D}/derived/r2_layers.npz"))
    m2 = json.load(open(f"{L.D}/derived/r2_meta.json"))
    H, info = sample(A, R1, R2)
    out = {"label": "registered revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md)", "sample": info,
           "validation_R1_vs_R9_pixels": m2["validation_R1_vs_R9_pixels"]}
    print(json.dumps(info), flush=True)
    did = H["irr"] | H["never"]
    if H["irr"].sum() < MIN_GROUP or H["never"].sum() < MIN_GROUP:
        out["main"] = {"skipped": "fewer than 1,000 pixels in a group even with the 2 km rule"}
    else:
        fit, lf, u = fit_model(H, did, L.YEARS)
        out["main"] = report(fit, lf, u, H)
        print("R9 main", {k: out["main"][k] for k in ("beta", "se_cluster_raion", "p_cluster_raion", "n_pixels")},
              "WCR", out["main"]["wcr"]["p_two_sided"], round(time.time() - t0), flush=True)
        ev = [y for y in L.YEARS if y != R2L.EV_DROP]
        fixed = {k: out["main"]["coefs"][k] for k in ("Pc_x_I", "Tc_x_I")}
        fe, _, _ = fit_model(H, did, L.YEARS, event=True, fixed=fixed)
        out["event_study"] = R2L.event_summary(fe, ev)
        out["event_study"]["weather_x_group_slopes_fixed_at_main_estimates"] = fixed
        # placebo test: 2016–2021 only, "effect" 2019–21 vs 2016–18
        pyears = R2L.BASE + R2L.DEF
        selp = did & R2L.fixed_panel(H["Y"][:, np.isin(YRS, pyears)], 5)
        fp, lp, up = fit_model(H, selp, pyears)
        j = fp["names"].index("T_x_Def")
        out["placebo_test"] = report(fp, lp, up, H, j=j)
        print("placebo", out["placebo_test"]["beta"], out["placebo_test"]["wcr"]["p_two_sided"], flush=True)
    # second comparison (triple difference), only if feasible
    if H["other"].sum() >= MIN_GROUP and "beta" in out["main"]:
        sel3 = H["irr"] | H["never"] | H["other"]
        f3, l3, u3 = fit_model(H, sel3, L.YEARS, design="triple")
        out["triple_difference"] = report(f3, l3, u3, H)
    else:
        out["triple_difference"] = {"skipped": f"only {int(H['other'].sum())} irrigated pixels not canal-fed (< 1,000)"}
    out["seconds"] = round(time.time() - t0)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/r2_h2_results.json", "w"), indent=1)
    print("done", out["seconds"], "s")


if __name__ == "__main__":
    main()
