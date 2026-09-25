"""R1-H1 — Registered Revision 1 for H1 (ANALYSIS_PLAN_v2_ADDENDUM_1.md: R4, R5).

Adds year x 2 km band of distance to the Dnipro main channel fixed effects and conflict
intensity (R4), and sets pixel-years with annual water share > 10 % or a change of more than
10 points from 2021 to missing (R5); matching, controls and inference as in the plan.
Output: outputs/v2/r1_h1_results.json
"""
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
import a3_h1 as H1  # noqa: E402

OUT = "outputs/v2"
CLASSES = H1.CLASSES


def water_rule(Y, R, idx):
    """R5: NaN where the annual water share (years with data) > 10 % or differs from 2021 by > 10 points."""
    Y = np.array(Y, dtype=np.float32, copy=True)
    W = np.stack([R["water_annual"][k].ravel()[idx] for k in range(len(L.YEARS))], 1)
    w21 = W[:, L.YEARS.index(2021)]
    bad = (W > 10) | (np.abs(W - w21[:, None]) > 10)
    bad &= np.isfinite(W)
    Y[bad] = np.nan
    return Y


def prepare():
    H = H1.load()
    R = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    idx = H["idx"]
    ny = len(L.YEARS)
    H["band"] = (R["dist_channel_km"].ravel()[idx] // 2).astype(int)
    H["CI"] = np.stack([R["conflict"][k].ravel()[idx] for k in range(ny)], 1)
    n_before = int(np.isfinite(H["ndvi_jo"]).sum())
    for v in ("ndvi_jo", "evi_jo", "ndvi_ja", "ndvi_ao"):
        H[v] = water_rule(H[v], R, idx)
    return H, R, {"pixel_years_removed_by_water_rule": n_before - int(np.isfinite(H["ndvi_jo"]).sum())}


def main():
    t0 = time.time()
    H, R, wr = prepare()
    rmeta = json.load(open(f"{L.D}/derived/r1_meta.json"))
    F, C15, C25, F25 = H["F"].astype(bool), H["C15"].astype(bool), H["C25"].astype(bool), H["F25"].astype(bool)
    out = {"label": "registered revision (Addendum 1)", "water_rule": wr,
           "water_years_used": rmeta["water_years_used"], "conflict_source": rmeta["conflict_source"]}
    w, diag = H1.match(H, F, C15)
    out["matching"] = diag
    out["balance"] = H1.balance(H, F, w)
    out["main"] = H1.estimate(H, F, w, full=True)
    out["event_study"] = H1.event_study(H, F, w)
    print("R1-H1 main", {k: out["main"][k] for k in ("beta", "se_cluster", "p_cluster", "n_pixels")},
          "WCR", out["main"]["wcr"]["p_two_sided"], "pretrend", out["event_study"]["pretrend_joint_p"], flush=True)
    ones = (F | C15).astype(float)
    rob = {"1_no_matching": H1.estimate(H, F, ones, full=True)}
    rob["1_no_matching"]["event_study"] = H1.event_study(H, F, ones)
    w25, _ = H1.match(H, F, C25)
    rob["2_control_band_5_25km"] = H1.estimate(H, F, w25)
    rob["3_no_weather"] = H1.estimate(H, F, w, use_weather=False)
    wA, _ = H1.match(H, F25, C15)
    rob["4a_flood_threshold_25pct"] = H1.estimate(H, F25, wA)
    F75 = F & (H["flood"] >= 0.75)
    wB, _ = H1.match(H, F75, C15)
    rob["4b_flood_threshold_75pct"] = H1.estimate(H, F75, wB)
    wE, _ = H1.match(H, F, C15, outcome="evi_jo")
    rob["6_evi"] = H1.estimate(H, F, wE, outcome="evi_jo")
    rob["7a_right_bank"] = H1.estimate(H, F, w, sub=H["bank"] == 1)
    rob["7b_left_bank"] = H1.estimate(H, F, w, sub=H["bank"] == 2)
    for c in ("crop", "grass", "wetland", "tree"):
        sub = H["dom"] == CLASSES.index(c)
        n_m = int((F & sub & (w > 0)).sum())
        rob[f"8_class_{c}"] = H1.estimate(H, F, w, sub=sub) if n_m >= 30 else {"skipped": f"{n_m} matched flooded pixels"}
        rob[f"8_class_{c}_no_matching"] = H1.estimate(H, F, ones, sub=sub) if (F & sub).sum() >= 30 else {"skipped": True}
    rob["9_excl_within_3km_built"] = H1.estimate(H, F, w, sub=H["dist_built"] > 3)
    out["robustness"] = rob
    out["seconds"] = round(time.time() - t0)
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/r1_h1_results.json", "w"), indent=1)
    for k, v in rob.items():
        if "beta" in v:
            print(f"{k:34s} beta={v['beta']:+.4f} se={v['se_cluster']:.4f} p={v['p_cluster']:.4f} nT={v['n_treated_px']}")


if __name__ == "__main__":
    main()
