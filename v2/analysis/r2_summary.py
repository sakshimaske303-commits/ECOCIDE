"""R2-summary — decision rule of ANALYSIS_PLAN_v2_ADDENDUM_2.md applied to the Revision 2 primary tests.
-> outputs/v2/r2_summary.json"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

OUT = "outputs/v2"


def verdict(beta, p_unadj, p_holm, third_ok, rr_excl):
    """Plan §7 with the Addendum 2 inputs: 'supported' needs beta < 0, Holm-adjusted WCR p < 0.05, the third
    condition (H1: placebo-floodplain p < 0.10; H2: placebo test p >= 0.10) and the M = 1 interval excluding 0."""
    if beta < 0 and p_holm < 0.05 and third_ok and rr_excl:
        return "supported"
    if beta < 0 and p_unadj < 0.05:
        return "suggestive"
    return "not supported"


def main():
    h1 = json.load(open(f"{OUT}/r2_h1_results.json"))
    pl = json.load(open(f"{OUT}/r2_h1_placebo.json"))
    h2 = json.load(open(f"{OUT}/r2_h2_results.json"))
    h34 = json.load(open(f"{OUT}/r2_h3_h4_results.json"))
    S = {"label": "registered revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md)"}
    m1, e1 = h1["main"], h1["main"]["event_study"]
    pkey = "matched" if h1["primary"] == "matched" else "no_matching"
    p_ri1 = pl[pkey]["p_one_sided"]
    if "beta" in h2.get("main", {}):
        m2, e2 = h2["main"], h2["event_study"]
        holm = L.holm([m1["wcr"]["p_two_sided"], m2["wcr"]["p_two_sided"]])
    else:
        m2 = None
        holm = [m1["wcr"]["p_two_sided"], None]
    rr1 = e1["rambachan_roth_ref2018"]["bounds"]["1.0"]
    S["H1_flood"] = {"beta": m1["beta"], "ci95_cluster": m1["ci95_cluster"], "p_cluster": m1["p_cluster"],
                     "p_wcr": m1["wcr"]["p_two_sided"], "p_wcr_holm": float(holm[0]), "conley": m1["conley"],
                     "primary": h1["primary"], "p_randomization": p_ri1, "n_placebos": pl[pkey]["n_placebos"],
                     "pretrend_joint_p": e1["pretrend_joint_p"], "rr_M1_robust_ci": rr1["robust_ci"],
                     "share_of_flooded_matched": h1["covariate_matching"]["matching"]["share_of_flooded_matched"],
                     "placebo_in_time": {k: h1["placebo_in_time"][k] for k in ("beta", "ci95_cluster", "p_cluster")},
                     "unmatched": {k: h1["unmatched"][k] for k in ("beta", "ci95_cluster", "p_cluster")},
                     "unmatched_p_randomization": pl["no_matching"]["p_one_sided"],
                     "verdict": verdict(m1["beta"], m1["p_cluster"], holm[0], p_ri1 < 0.10,
                                        rr1["excludes_zero"])}
    if m2 is not None:
        rr2 = e2["rambachan_roth_ref2018"]["bounds"]["1.0"]
        pt = h2["placebo_test"]
        S["H2_irrigation"] = {"beta": m2["beta"], "ci95_cluster": m2["ci95_cluster"], "p_cluster": m2["p_cluster_raion"],
                              "p_wcr": m2["wcr"]["p_two_sided"], "p_wcr_holm": float(holm[1]), "conley": m2["conley"],
                              "beta_pct_of_base_mean": m2["beta_pct_of_base_mean"],
                              "placebo_test": {"beta": pt["beta"], "p_wcr": pt["wcr"]["p_two_sided"]},
                              "pretrend_joint_p": e2["pretrend_joint_p"], "rr_M1_robust_ci": rr2["robust_ci"],
                              "sample": h2["sample"], "triple_difference": h2["triple_difference"].get("beta",
                                                                                                        h2["triple_difference"]),
                              "verdict": verdict(m2["beta"], m2["p_cluster_raion"], holm[1],
                                                 pt["wcr"]["p_two_sided"] >= 0.10, rr2["excludes_zero"])}
    else:
        S["H2_irrigation"] = {"verdict": "not run", "reason": h2["main"]}
    S["H3_check"] = h34["H3_check_R12"]
    d = h34["H4_decomposition_Kherson"]
    S["H4"] = {k: {"contribution": v["contribution"], "ci95": v["contribution_ci95"]} for k, v in d["categories"].items()}
    S["H4"]["total"] = {"contribution": d["sum_of_contributions"], "ci95": d["sum_ci95"]}
    S["H4"]["descriptive_only"] = d["descriptive_only"]
    json.dump(S, open(f"{OUT}/r2_summary.json", "w"), indent=1)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
