"""A4 — H2: irrigation-loss triple difference (plan §4.3, §6, §8).

    Y_iy = a_i + l_(y,oblast) + m_(y,irrigated) + k_(y,zone) + b Irr_i K_i Post_y + d Irr_i K_i War_y + g'W_iy + e_iy

Output: outputs/v2/h2_results.json
"""
import json
import os
import sys
import time

import numpy as np
from scipy.stats import f as fdist

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

OUT = "outputs/v2"
RES = 231.656358


def load():
    """Arrays from h2_pixels.npz, cached as .npy and memory-mapped (keeps RAM low)."""
    d = f"{L.D}/derived/h2_npy"
    src = f"{L.D}/derived/h2_pixels.npz"
    if not os.path.exists(f"{d}/done") or os.path.getmtime(f"{d}/done") < os.path.getmtime(src):
        os.makedirs(d, exist_ok=True)
        z = np.load(src)
        for k in z.files:
            np.save(f"{d}/{k}.npy", z[k])
        open(f"{d}/done", "w").close()
    return {f[:-4]: np.load(f"{d}/{f}", mmap_mode="r") for f in os.listdir(d) if f.endswith(".npy")}


def classify(H, hi=0.45, lo=0.35):
    ja = H["ja_pre"]
    irr = (ja >= hi).sum(1) >= 3
    rain = (ja < lo).sum(1) >= 4
    return irr & ~rain, rain & ~irr


def build(H, irr, rain, outcome="ndvi_jo", use_weather=True, event=False, sub=None, Kmask=None):
    Kz = H["K"].astype(bool) if Kmask is None else Kmask
    Oz = H["O"].astype(bool)
    Y = H[outcome]
    keep = (irr | rain) & (Kz | Oz) & (np.isfinite(Y).sum(1) >= L.MIN_YEARS)
    if sub is not None:
        keep &= sub
    u = np.flatnonzero(keep)
    Yu = Y[u]
    N, T = Yu.shape
    rep = lambda a: np.repeat(a[u].astype(np.float32)[:, None], T, 1)  # noqa: E731
    extra = {"I": rep(irr), "K": rep(Kz), "ob": rep(H["oblast"]), "blk": rep(H["block"]),
             "yr": np.tile(np.array(L.YEARS, np.float32)[None, :], (N, 1)), "P": H["P"][u], "Tm": H["T"][u]}
    lf = L.long_format(Yu, extra)
    yrs = lf["yr"].astype(int)
    IK = lf["I"] * lf["K"]
    if event:
        cols, names = [], []
        for y in L.YEARS:
            if y != 2021:
                cols.append(IK * (yrs == y))
                names.append(f"IrrK_x_{y}")
    else:
        cols = [IK * np.isin(yrs, L.POST), IK * np.isin(yrs, L.WAR)]
        names = ["IrrK_x_Post", "IrrK_x_War"]
    if use_weather:
        cols += [lf["P"] / 100.0, lf["Tm"]]
        names += ["precip_100mm", "temp_C"]
    X = np.column_stack(cols).astype(np.float32)
    del cols
    g_ob = np.unique(lf["ob"].astype(int) * 10000 + yrs, return_inverse=True)[1]
    g_ir = np.unique(lf["I"].astype(int) * 10000 + yrs, return_inverse=True)[1]
    g_k = np.unique(lf["K"].astype(int) * 10000 + yrs, return_inverse=True)[1]
    groups = [lf["unit"], g_ob, g_ir, g_k]
    w = np.ones(len(lf["y"]))
    return lf, X, names, groups, u, w


def estimate(H, irr, rain, outcome="ndvi_jo", use_weather=True, sub=None, full=False, Kmask=None, B=9999):
    lf, X, names, groups, u, w = build(H, irr, rain, outcome, use_weather, sub=sub, Kmask=Kmask)
    fit = L.fe_ols(lf["y"], X, groups, w, lf["blk"].astype(int), names)
    b, se = fit["coef"][0], fit["se"][0]
    Kz = H["K"].astype(bool) if Kmask is None else Kmask
    cnt = {"K_irr": int((Kz[u] & irr[u]).sum()), "K_rain": int((Kz[u] & rain[u]).sum()),
           "O_irr": int((~Kz[u] & irr[u]).sum()), "O_rain": int((~Kz[u] & rain[u]).sum())}
    pre = np.nanmean(H[outcome][u][(Kz[u] & irr[u])][:, :6])
    res = {"beta": float(b), "se_cluster": float(se), "p_cluster": float(fit["p"][0]),
           "ci95_cluster": [float(b - 1.96 * se), float(b + 1.96 * se)],
           "delta_war": float(fit["coef"][1]), "delta_war_se": float(fit["se"][1]), "delta_war_p": float(fit["p"][1]),
           "n_obs": fit["n"], "n_pixels": int(len(u)), "counts": cnt, "clusters": fit["G"],
           "pre_mean_K_irrigated": float(pre), "beta_pct_of_pre_mean": float(b / pre * 100)}
    if full:
        res["wcr"] = L.wild_cluster_p(fit, 0, B=B)
        xy = np.c_[H["col"][u] * RES, -H["row"][u] * RES]
        res["se_conley25km"] = L.conley_se(fit, 0, xy, lf["unit"], cell_m=4 * RES * 5)
        res["p_conley25km"] = float(2 * L.norm.sf(abs(b / res["se_conley25km"])))
    return res


def event_study(H, irr, rain, outcome="ndvi_jo"):
    lf, X, names, groups, u, w = build(H, irr, rain, outcome, event=True)
    fit = L.fe_ols(lf["y"], X, groups, w, lf["blk"].astype(int), names)
    ev = [y for y in L.YEARS if y != 2021]
    k = len(ev)
    beta, V = fit["coef"][:k], fit["vcov"][:k, :k]
    pi = [ev.index(y) for y in [2016, 2017, 2018, 2019, 2020]]
    bp, Vp = beta[pi], V[np.ix_(pi, pi)]
    Fs = float(bp @ np.linalg.solve(Vp, bp)) / len(pi)
    rr = L.rr_bounds(beta, V, ev, ref=2021, pre=[2016, 2017, 2018, 2019, 2020], post_targets=[2023, 2024])
    return {"coefs": [{"year": y, "coef": float(beta[i]), "se": float(np.sqrt(V[i, i])), "p": float(fit["p"][i])}
                      for i, y in enumerate(ev)],
            "reference": 2021, "pretrend_joint_F": Fs, "pretrend_joint_p": float(fdist.sf(Fs, len(pi), fit["G"] - 1)),
            "rambachan_roth": rr}


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    H = load()
    names = json.load(open(f"{L.D}/derived/layers_meta.json"))["oblast_names"]
    irr, rain = classify(H)
    R = {"design": "triple difference: irrigated vs rainfed cropland, Kakhovka zone K vs outside zone O, 2023–24 vs 2016–21"}
    R["main"] = estimate(H, irr, rain, full=True)
    print("H2 main", {k: R["main"][k] for k in ("beta", "se_cluster", "p_cluster", "n_pixels")},
          "WCR", R["main"]["wcr"]["p_two_sided"], "Conley", R["main"]["se_conley25km"], round(time.time() - t0))
    R["event_study"] = event_study(H, irr, rain)
    print("pretrend p", R["event_study"]["pretrend_joint_p"], round(time.time() - t0))
    # classification check: share 'irrigated' by oblast in zone O
    ob = H["oblast"]
    R["classification_by_oblast_zoneO"] = {
        names[o - 1]: {"irrigated": int((H["O"].astype(bool) & irr & (ob == o)).sum()),
                       "rainfed": int((H["O"].astype(bool) & rain & (ob == o)).sum())}
        for o in np.unique(ob[H["O"].astype(bool)])}

    rob = {}
    i2, r2 = classify(H, 0.40, 0.30)
    rob["5a_thresholds_040_030"] = estimate(H, i2, r2)
    i3, r3 = classify(H, 0.50, 0.40)
    rob["5b_thresholds_050_040"] = estimate(H, i3, r3)
    rob["3_no_weather"] = estimate(H, irr, rain, use_weather=False)
    rob["6_evi"] = estimate(H, irr, rain, outcome="evi_jo")
    kh, zp = names.index("Kherson") + 1, names.index("Zaporizhia") + 1
    Kz = H["K"].astype(bool)
    rob["7a_K_Kherson_only"] = estimate(H, irr, rain, sub=~Kz | (ob == kh))
    rob["7b_K_Zaporizhzhia_only"] = estimate(H, irr, rain, sub=~Kz | (ob == zp))
    rob["9_excl_within_3km_built"] = estimate(H, irr, rain, sub=H["dist_built"] > 3)
    sec = {"ndvi_jul_aug": estimate(H, irr, rain, outcome="ndvi_ja")}
    Hs = dict(H)
    Hs["ndvi_ao"] = H["ndvi_ao"].copy()
    Hs["ndvi_ao"][:, L.YEARS.index(2023)] = np.nan
    sec["ndvi_apr_oct_excl2023"] = estimate(Hs, irr, rain, outcome="ndvi_ao")
    Hc = dict(H)
    Hc["cropped"] = np.where(np.isfinite(H["ndvi_ao_p90"]), (H["ndvi_ao_p90"] >= 0.5).astype(np.float32), np.nan)
    sec["cropped_indicator"] = estimate(Hc, irr, rain, outcome="cropped")
    R["robustness"] = rob
    R["secondary"] = sec

    # placebo zones (plan §4.4): each oblast of zone O in turn treated as if it were zone K
    Oz = H["O"].astype(bool)
    plac = {}
    for o in np.unique(ob[Oz]):
        pk = Oz & (ob == o)
        if (pk & irr).sum() < 500 or (pk & rain).sum() < 500:
            plac[names[o - 1]] = {"skipped": "fewer than 500 irrigated or rainfed pixels"}
            continue
        Hp = dict(H)
        Hp["K"] = pk
        Hp["O"] = Oz & ~pk
        r = estimate(Hp, irr, rain, sub=Oz)
        plac[names[o - 1]] = {k: r[k] for k in ("beta", "se_cluster", "p_cluster", "n_pixels", "counts")}
        print("placebo", names[o - 1], round(r["beta"], 4))
    betas = [v["beta"] for v in plac.values() if "beta" in v]
    b0 = R["main"]["beta"]
    R["placebo_zones"] = {"units": plac, "n_placebos": len(betas),
                          "p_randomization_one_sided": (1 + sum(x <= b0 for x in betas)) / (1 + len(betas)),
                          "p_randomization_two_sided": (1 + sum(abs(x) >= abs(b0) for x in betas)) / (1 + len(betas))}
    R["seconds"] = round(time.time() - t0)
    with open(f"{OUT}/h2_results.json", "w") as fh:
        json.dump(R, fh, indent=1)
    for k, v in {**rob, **sec}.items():
        print(f"{k:28s} beta={v['beta']:+.4f} se={v['se_cluster']:.4f} p={v['p_cluster']:.4f} n={v['n_pixels']}")
    print("RI", R["placebo_zones"]["p_randomization_one_sided"], "seconds", R["seconds"])


if __name__ == "__main__":
    main()
