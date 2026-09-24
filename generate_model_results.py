"""
Runs the complete statistical battery once and writes every number used by
the paper, dashboard and figures to outputs/model_results.json.

    python generate_model_results.py

Re-run this (then build_all_figures.py) whenever the NDVI data changes.
To analyse a different NDVI folder without touching data/ndvi:
    ECO_NDVI_DIR=data/ndvi_v3 python generate_model_results.py
"""
import json
import os
from datetime import datetime, timezone

import numpy as np
from scipy import stats

import eco_core as ec


def main():
    data = ec.load_all()
    R = {"meta": {
        "ndvi_dir": ec.NDVI_DIR,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "method": "DiD on monthly treated-minus-control NDVI gap; Newey-West HAC (maxlags=3), t-distribution",
        "event_month": "2023-06",
        "window": "2022-01 to 2024-11",
    }}

    # --- pre-period descriptives (Kherson vs Tulcea) ---
    pre = {z: data[z][data[z]["date"] < ec.EVENT_DATE] for z in ["kherson", "tulcea"]}
    R["pre_period"] = {
        z: {"mean": float(pre[z]["ndvi"].mean()), "sd": float(pre[z]["ndvi"].std()), "n": int(len(pre[z])),
            "seasonal_amplitude": float(pre[z].groupby(pre[z]["date"].dt.month)["ndvi"].mean().pipe(lambda s: s.max() - s.min()))}
        for z in pre
    }
    R["pre_period"]["welch_p"] = float(stats.ttest_ind(pre["kherson"]["ndvi"], pre["tulcea"]["ndvi"], equal_var=False).pvalue)

    # --- primary + validation models ---
    R["main_did"] = ec.did(data)
    R["main_did_seasonal"] = ec.did(data, month_fe=True)
    R["placebo_broad"] = ec.did(data, event_date="2022-06-01", end="2023-06-01")
    R["narrowed_did"] = ec.did(data, start="2023-01-01")
    R["placebo_narrowed"] = ec.did(data, event_date="2023-03-01", start="2023-01-01", end="2023-06-01", maxlags=1)
    R["main_did"]["pct_of_pre_mean"] = abs(R["main_did"]["coef"]) / R["pre_period"]["kherson"]["mean"]

    # --- multi-control panel ---
    R["pooled_did"] = ec.did(data, controls=ec.CONTROLS)
    R["pooled_did_seasonal"] = ec.did(data, controls=ec.CONTROLS, month_fe=True)
    R["pooled_placebo"] = ec.did(data, controls=ec.CONTROLS, event_date="2022-06-01", end="2023-06-01")
    R["per_control"] = {z: ec.did(data, controls=[z]) for z in ec.CONTROLS}

    # --- placebo in space (randomization inference) ---
    pis = {z: ec.did(data, treated=z, controls=[c for c in ec.ALL_ZONES if c != z]) for z in ec.ALL_ZONES}
    k = pis["kherson"]["coef"]
    one = 1 + sum(1 for z in pis if z != "kherson" and pis[z]["coef"] < k)
    two = 1 + sum(1 for z in pis if z != "kherson" and abs(pis[z]["coef"]) > abs(k))
    R["placebo_in_space"] = {"units": pis, "rank_one_sided": one, "rank_two_sided": two,
                             "p_one_sided": one / 5, "p_two_sided": two / 5}

    # --- control-only divergence check (Kherson excluded) ---
    R["control_divergence"] = {z: ec.did(data, treated=z, controls=[c for c in ec.CONTROLS if c != z]) for z in ec.CONTROLS}

    # --- event study + multiple testing ---
    es = ec.event_study(data)
    pvals = [r["p"] for r in es]
    thr, bonf, bh = ec.bonferroni_bh(pvals)
    for r, b1, b2 in zip(es, bonf, bh):
        r["bonferroni"] = bool(b1)
        r["bh"] = bool(b2)
    R["event_study"] = {"quarters": es, "bonferroni_threshold": thr, "reference": "Mar 2023–May 2023"}
    R["event_study_pooled"] = ec.event_study(data, controls=ec.CONTROLS)

    # --- specification robustness ---
    R["lag_sensitivity"] = {str(L): ec.did(data, maxlags=L) for L in range(1, 7)}
    R["log_ndvi"] = ec.did(data, log=True)
    R["log_ndvi"]["pct_change"] = float(np.exp(R["log_ndvi"]["coef"]) - 1)

    # --- low-coverage months ---
    low = {}
    for thr_v in (0.15, 0.25):
        flagged = {z: [d.strftime("%Y-%m") for d in data[z].loc[data[z]["valid_frac"] < thr_v, "date"]] for z in ec.ALL_ZONES}
        low[str(thr_v)] = {
            "flagged": flagged,
            "main": ec.did(data, min_valid=thr_v),
            "pooled": ec.did(data, controls=ec.CONTROLS, min_valid=thr_v),
        }
    R["low_coverage"] = low
    R["valid_fraction"] = {z: {"min": float(data[z]["valid_frac"].min()), "max": float(data[z]["valid_frac"].max()),
                               "min_month": data[z].loc[data[z]["valid_frac"].idxmin(), "date"].strftime("%Y-%m")}
                           for z in ec.ALL_ZONES}

    # --- for documenting the change from the earlier stacked specification ---
    R["legacy_stacked_spec"] = {
        "main": ec.legacy_stacked_did(data),
        "pooled": ec.legacy_stacked_did(data, controls=ec.CONTROLS),
        "note": "stacked OLS + HAC on row order + normal distribution (earlier versions); superseded",
    }

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/model_results.json", "w", encoding="utf-8") as f:
        json.dump(R, f, indent=2, ensure_ascii=False)
    print("Saved: outputs/model_results.json\n")

    print("Main DiD (Kherson vs Tulcea):   ", ec.fmt(R["main_did"]))
    print("  + zone-specific seasonality:  ", ec.fmt(R["main_did_seasonal"]))
    print("Placebo (fake date Jun 2022):   ", ec.fmt(R["placebo_broad"]))
    print("Narrowed baseline (Jan 2023+):  ", ec.fmt(R["narrowed_did"]))
    print("Narrowed placebo (fake Mar 23): ", ec.fmt(R["placebo_narrowed"]))
    print("Pooled 4-control:               ", ec.fmt(R["pooled_did"]))
    print("  + zone-specific seasonality:  ", ec.fmt(R["pooled_did_seasonal"]))
    print("Pooled placebo:                 ", ec.fmt(R["pooled_placebo"]))
    for z, r in R["per_control"].items():
        print(f"Kherson vs {z:10s}:          ", ec.fmt(r))
    print("\nPlacebo in space:")
    for z, r in pis.items():
        print(f"  {z:10s}", ec.fmt(r))
    print(f"  Kherson rank one-sided {one}/5 (p={one/5:.2f}), two-sided {two}/5 (p={two/5:.2f})")
    print("\nControl-only divergence:")
    for z, r in R["control_divergence"].items():
        print(f"  {z:10s}", ec.fmt(r))
    print("\nEvent study (Kherson - Tulcea gap, ref Mar-May 2023):")
    for r in es:
        print(f"  Q{r['quarter']:+d} {r['months']:20s} {r['coef']:+.4f} p={r['p']:.4f} bonf={r['bonferroni']} bh={r['bh']}")
    print("\nLag sensitivity:", {L: round(v["p"], 3) for L, v in R["lag_sensitivity"].items()})
    print("log NDVI:", ec.fmt(R["log_ndvi"]), f"≈{R['log_ndvi']['pct_change']*100:.1f}%")
    for t, v in low.items():
        print(f"Low coverage <{t}: dropped", {z: m for z, m in v["flagged"].items() if m})
        print("   main  ", ec.fmt(v["main"]))
        print("   pooled", ec.fmt(v["pooled"]))
    print("\nLegacy stacked spec:", R["legacy_stacked_spec"])


if __name__ == "__main__":
    main()
