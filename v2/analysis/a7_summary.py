"""A7 — applies the pre-registered decision rules (plan §6–§7) and writes one summary.

supported     : beta < 0, Holm-adjusted WCR p < 0.05, randomization p < 0.10, M=1 robust CI excludes 0
suggestive    : beta < 0, unadjusted p < 0.05, but one of the other conditions fails
not supported : otherwise
Output: outputs/v2/study2_summary.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

OUT = "outputs/v2"


def verdict(beta, p_unadj, p_holm, p_ri, rr_excl):
    if beta < 0 and p_holm < 0.05 and p_ri < 0.10 and rr_excl:
        return "supported"
    if beta < 0 and p_unadj < 0.05:
        return "suggestive"
    return "not supported"


def main():
    h1 = json.load(open(f"{OUT}/h1_results.json"))
    h2 = json.load(open(f"{OUT}/h2_results.json"))
    pl = json.load(open(f"{OUT}/h1_placebo.json"))
    h34 = json.load(open(f"{OUT}/h3_h4_results.json"))
    p_wcr = [h1["main"]["wcr"]["p_two_sided"], h2["main"]["wcr"]["p_two_sided"]]
    holm = L.holm(p_wcr)
    S = {"decision_rule": __doc__.strip().splitlines()[2:5]}
    for name, R, ph, pri in (("H1_flood", h1, holm[0], pl["matched"]["p_one_sided"]),
                             ("H2_irrigation", h2, holm[1], h2["placebo_zones"]["p_randomization_one_sided"])):
        m = R["main"]
        rr = R["event_study"]["rambachan_roth"]
        S[name] = {
            "beta": m["beta"], "ci95_cluster": m["ci95_cluster"], "p_cluster": m["p_cluster"],
            "p_wcr": m["wcr"]["p_two_sided"], "p_wcr_holm": float(ph), "se_conley25km": m["se_conley25km"],
            "p_randomization": pri, "pretrend_joint_p": R["event_study"]["pretrend_joint_p"],
            "rr_theta_2023_24_vs_2021": rr["theta"], "rr_M1_robust_ci": rr["bounds"]["1.0"]["robust_ci"],
            "rr_M1_excludes_zero": rr["bounds"]["1.0"]["excludes_zero"],
            "n_pixels": m["n_pixels"], "pct_of_pre_mean": m.get("beta_pct_of_pre_mean"),
            "verdict": verdict(m["beta"], m["p_cluster"], ph, pri, rr["bounds"]["1.0"]["excludes_zero"]),
        }
    S["H1_flood"]["matched_treated_share"] = h1["matching"]["matched_treated"] / h1["matching"]["treated_complete_pre"]
    S["H3_reservoir_bed"] = {r["year"]: {"mean_ndvi_jul_oct": r["mean_ndvi_jul_oct"], "km2_ndvi_gt_0_3": r["area_km2_ndvi_gt_0_3"]}
                             for r in h34["H3_reservoir_bed"]["by_year"]}
    S["H4_decomposition"] = {k: v["contribution_to_oblast_relative_change"]
                             for k, v in h34["H4_decomposition_Kherson"]["categories"].items()}
    S["H4_decomposition"]["total_relative_change"] = h34["H4_decomposition_Kherson"]["sum_of_contributions"]
    with open(f"{OUT}/study2_summary.json", "w") as fh:
        json.dump(S, fh, indent=1)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
