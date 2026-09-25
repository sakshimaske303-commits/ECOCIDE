"""R1-summary — pre-registered decision rule (plan §7) applied to the Registered Revision 1
specifications, Holm correction over the two revised primary tests. -> outputs/v2/r1_summary.json"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
from a7_summary import verdict  # noqa: E402

OUT = "outputs/v2"


def main():
    h1 = json.load(open(f"{OUT}/r1_h1_results.json"))
    h2 = json.load(open(f"{OUT}/r1_h2_results.json"))
    pl = json.load(open(f"{OUT}/r1_h1_placebo.json"))
    h34 = json.load(open(f"{OUT}/r1_h3_h4_results.json"))
    holm = L.holm([h1["main"]["wcr"]["p_two_sided"], h2["main"]["wcr"]["p_two_sided"]])
    S = {"label": "registered revision (ANALYSIS_PLAN_v2_ADDENDUM_1.md, commit 30e3840)"}
    for name, R, ph, pri in (("H1_flood", h1, holm[0], pl["matched"]["p_one_sided"]),
                             ("H2_irrigation", h2, holm[1], h2["placebo_raions"]["p_randomization_one_sided"])):
        m, es = R["main"], R["event_study"]
        rr = es["rambachan_roth"]
        S[name] = {"beta": m["beta"], "ci95_cluster": m["ci95_cluster"], "p_cluster": m["p_cluster"],
                   "p_wcr": m["wcr"]["p_two_sided"], "p_wcr_holm": float(ph), "se_conley25km": m["se_conley25km"],
                   "p_randomization": pri, "pretrend_joint_p": es["pretrend_joint_p"],
                   "event_study": {r["year"]: r["coef"] for r in es["coefs"]},
                   "rr_theta_2023_24_vs_2021": rr["theta"], "rr_M1_robust_ci": rr["bounds"]["1.0"]["robust_ci"],
                   "n_pixels": m["n_pixels"],
                   "verdict": verdict(m["beta"], m["p_cluster"], ph, pri, rr["bounds"]["1.0"]["excludes_zero"])}
    S["H1_flood"]["no_matching"] = {k: h1["robustness"]["1_no_matching"][k] for k in ("beta", "ci95_cluster", "p_cluster")}
    S["H1_flood"]["wetland_no_matching"] = {k: h1["robustness"]["8_class_wetland_no_matching"][k] for k in ("beta", "ci95_cluster", "p_cluster")}
    S["H2_irrigation"]["n_placebo_raions"] = h2["placebo_raions"]["n_placebos"]
    S["H2_irrigation"]["classification_counts"] = h2["classification_counts"]
    S["H3_land_only"] = {r["year"]: {"land_km2": r["land_km2"], "mean_ndvi": r["mean_ndvi_jul_oct_land"]}
                         for r in h34["H3_reservoir_bed_land_only"]}
    S["H4"] = {k: v["contribution"] for k, v in h34["H4_decomposition_Kherson"]["categories"].items()}
    S["H4"]["total"] = h34["H4_decomposition_Kherson"]["sum_of_contributions"]
    json.dump(S, open(f"{OUT}/r1_summary.json", "w"), indent=1)
    print(json.dumps(S, indent=1))


if __name__ == "__main__":
    main()
