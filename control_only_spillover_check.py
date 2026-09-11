import json
import pandas as pd
import statsmodels.formula.api as smf

TREATMENT_DATE = "2023-06-01"
CONTROL_ZONES = ["tulcea", "galati", "constanta", "braila"]


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment})
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
    Spillover check among control zones (Kherson excluded entirely).

    Section 6 argues 'no spatial spillover into the controls' only on distance
    grounds (~350km, international border). This tests it directly: with
    Kherson removed from the panel altogether, each of the 4 Romanian
    counties is in turn assigned 'treated' status against the OTHER THREE,
    using the real June 2023 cutoff. If the war's regional effects spilled
    into the controls, at least one of these 4 control-only comparisons
    should show a shift even with Kherson absent.
    """
    print("=== CONTROL-ONLY SPILLOVER CHECK (Kherson excluded) ===\n")
    for zone in CONTROL_ZONES:
        others = [z for z in CONTROL_ZONES if z != zone]
        coef, pval = run_did(zone, others)
        sig = "  <-- SIGNIFICANT" if pval < 0.05 else ""
        print(f"  {zone:12s} vs other 3 controls: did_term={coef:+.4f}  HAC p={pval:.4f}{sig}")


if __name__ == "__main__":
    main()
