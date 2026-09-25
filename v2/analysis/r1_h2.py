"""R1-H2 — Registered Revision 1 for H2 (ANALYSIS_PLAN_v2_ADDENDUM_1.md: R1–R4).

Irrigated/rainfed from 2010–2015 (R1); comparison zone restricted to the steppe oblasts (R2);
raion placebo units (R3); year x irrigated x occupied fixed effects and conflict intensity (R4).
Output: outputs/v2/r1_h2_results.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
import a4_h2 as H2  # noqa: E402

OUT = "outputs/v2"


def build_sample(R, meta, zoneO_key="zoneO_r2"):
    Hf = H2.load()                                      # all zone K + zone O pixels (pre-registered set)
    idx_all = np.asarray(Hf["idx"])
    Kf = np.asarray(Hf["K"]).astype(bool)
    O2 = R[zoneO_key].ravel()[idx_all]
    keep = np.flatnonzero(Kf | O2)
    idx = idx_all[keep]
    H = {k: np.asarray(v[keep]) if getattr(v, "shape", ())[:1] == (len(idx_all),) else v for k, v in Hf.items()}
    H["K"] = Kf[keep]
    H["O"] = O2[keep]
    irr = R["irr_r1"].ravel()[idx]
    rain = R["rain_r1"].ravel()[idx]
    ny = len(L.YEARS)
    H["occ"] = np.stack([R["occupied"][k].ravel()[idx] for k in range(ny)], axis=1)
    H["CI"] = np.stack([R["conflict"][k].ravel()[idx] for k in range(ny)], axis=1)
    H["raion"] = R["raion"].ravel()[idx]
    return H, irr, rain, idx


def classify_r1(R, idx, hi, lo):
    """R1 with alternative thresholds (plan robustness 5), from the stored 2010–2015 July–August NDVI."""
    import xarray as xr
    ja = []
    for y in range(2010, 2016):
        ds = xr.open_dataset(f"{L.D}/annual/annual_{y}.nc")
        v = ds["ndvi_ja"].values.ravel()[idx] / 10000.0
        n = ds["n_ja"].values.ravel()[idx]
        ja.append(np.where(n >= 2, v, np.nan))
        ds.close()
    ja = np.stack(ja, 1)
    irr = (ja >= hi).sum(1) >= 4
    rain = (ja < lo).sum(1) >= 5
    return irr & ~rain, rain & ~irr


def main():
    t0 = time.time()
    R = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    rmeta = json.load(open(f"{L.D}/derived/r1_meta.json"))
    names = json.load(open(f"{L.D}/derived/layers_meta.json"))["oblast_names"]
    raion_names = rmeta["raion_names"]
    H, irr, rain, idx = build_sample(R, rmeta)
    out = {"label": "registered revision (Addendum 1)",
           "occupation_source": rmeta["occupation_source"], "conflict_source": rmeta["conflict_source"],
           "classification_counts": {"K_irr": int((H["K"] & irr).sum()), "K_rain": int((H["K"] & rain).sum()),
                                     "O_irr": int((H["O"] & irr).sum()), "O_rain": int((H["O"] & rain).sum())}}
    out["main"] = H2.estimate(H, irr, rain, full=True)
    print("R1-H2 main", {k: out["main"][k] for k in ("beta", "se_cluster", "p_cluster", "n_pixels")},
          "WCR", out["main"]["wcr"]["p_two_sided"], round(time.time() - t0), flush=True)
    out["event_study"] = H2.event_study(H, irr, rain)
    print("pretrend p", out["event_study"]["pretrend_joint_p"], flush=True)

    rob = {}
    rob["3_no_weather"] = H2.estimate(H, irr, rain, use_weather=False)
    i2, r2 = classify_r1(R, idx, 0.40, 0.30)
    rob["5a_thresholds_040_030"] = H2.estimate(H, i2, r2)
    i3, r3 = classify_r1(R, idx, 0.50, 0.40)
    rob["5b_thresholds_050_040"] = H2.estimate(H, i3, r3)
    rob["6_evi"] = H2.estimate(H, irr, rain, outcome="evi_jo")
    kh, zp = names.index("Kherson") + 1, names.index("Zaporizhia") + 1
    ob = H["oblast"]
    rob["7a_K_Kherson_only"] = H2.estimate(H, irr, rain, sub=~H["K"] | (ob == kh))
    rob["7b_K_Zaporizhzhia_only"] = H2.estimate(H, irr, rain, sub=~H["K"] | (ob == zp))
    rob["9_excl_within_3km_built"] = H2.estimate(H, irr, rain, sub=H["dist_built"] > 3)
    Hd, irrd, raind, _ = build_sample(R, rmeta, "zoneO_r2_dnipro")
    rob["R2_sensitivity_add_Dnipropetrovsk"] = H2.estimate(Hd, irrd, raind)
    del Hd
    out["robustness"] = rob
    out["secondary"] = {"ndvi_jul_aug": H2.estimate(H, irr, rain, outcome="ndvi_ja")}
    print("robustness done", round(time.time() - t0), flush=True)

    # R3: raion placebo units inside the restricted zone O
    Oz = H["O"]
    plac = {}
    Hp_base = {k: v for k, v in H.items()}
    for rid in np.unique(H["raion"][Oz]):
        pk = Oz & (H["raion"] == rid)
        if (pk & irr).sum() < 300 or (pk & rain).sum() < 300:
            continue
        Hp = dict(Hp_base)
        Hp["K"] = pk
        Hp["O"] = Oz & ~pk
        r = H2.estimate(Hp, irr, rain, sub=Oz)
        plac[raion_names[rid - 1]] = {k: r[k] for k in ("beta", "se_cluster", "p_cluster", "n_pixels", "counts")}
    betas = [v["beta"] for v in plac.values()]
    b0 = out["main"]["beta"]
    out["placebo_raions"] = {"units": plac, "n_placebos": len(betas),
                             "p_randomization_one_sided": (1 + sum(x <= b0 for x in betas)) / (1 + len(betas)),
                             "p_randomization_two_sided": (1 + sum(abs(x) >= abs(b0) for x in betas)) / (1 + len(betas))}
    print("placebos", len(betas), "RI p", out["placebo_raions"]["p_randomization_one_sided"], flush=True)
    out["seconds"] = round(time.time() - t0)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/r1_h2_results.json", "w"), indent=1)
    for k, v in {**rob, **out["secondary"]}.items():
        print(f"{k:34s} beta={v['beta']:+.4f} se={v['se_cluster']:.4f} p={v['p_cluster']:.4f} n={v['n_pixels']}")


if __name__ == "__main__":
    main()
