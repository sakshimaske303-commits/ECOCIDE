import json
import pandas as pd
import statsmodels.formula.api as smf

TREATMENT_DATE = "2023-06-01"
ZONES = ["kherson", "tulcea", "galati", "constanta", "braila"]


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment, "zone": zone_name})
    return pd.DataFrame(rows)


def run_did(treated_zone, control_zones):
    treated = load_ndvi(treated_zone, is_treatment=1)
    controls = pd.concat(
        [load_ndvi(z, is_treatment=0) for z in control_zones], ignore_index=True
    )
    df = pd.concat([treated, controls], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["post"] = (df["date"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)

    model = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )
    return model.params["did_term"], model.pvalues["did_term"]


def main():
    """
    Placebo-in-space / randomization-inference check.

    Section 4.5 asks whether the Kherson effect survives against each control
    zone individually (Kherson always held fixed as 'treated'). This script
    asks the complementary question: if one of the four Romanian counties —
    rather than Kherson — were assigned the real post-June-2023 'treatment'
    status, would it show an effect just as large? With only 5 geographic
    units in the panel, cluster/HAC-based p-values alone cannot rule this out
    (Conley & Taber, 2011); an exact randomization test can.

    Each of the 5 zones is assigned 'treated' status in turn, against the
    other 4 as its control panel, using the SAME real post-June-2023 cutoff
    (this is a placebo IN SPACE — who gets treated — not in time).
    """
    results = []
    for zone in ZONES:
        controls = [z for z in ZONES if z != zone]
        coef, pval = run_did(zone, controls)
        results.append((zone, coef, pval))

    print("=== PLACEBO-IN-SPACE TEST (each zone assigned 'treated' in turn) ===\n")
    for zone, coef, pval in results:
        tag = "  <- real treated unit" if zone == "kherson" else ""
        print(f"  {zone:12s} did_term={coef:+.4f}  HAC p={pval:.4f}{tag}")

    n = len(results)
    one_sided_rank = sorted(results, key=lambda r: r[1]).index(
        next(r for r in results if r[0] == "kherson")
    ) + 1
    two_sided_rank = sorted(results, key=lambda r: -abs(r[1])).index(
        next(r for r in results if r[0] == "kherson")
    ) + 1

    print(f"\nKherson's rank among {n} possible unit-assignments:")
    print(f"  One-sided (most-negative-first): rank {one_sided_rank} of {n} "
          f"-> exact randomization p = {one_sided_rank/n:.2f}")
    print(f"  Two-sided (largest |effect| first): rank {two_sided_rank} of {n} "
          f"-> exact randomization p = {two_sided_rank/n:.2f}")
    print(f"\n  (With only {n} units, {1/n:.2f} is the smallest randomization "
          f"p-value ANY unit could ever obtain.)")


if __name__ == "__main__":
    main()
