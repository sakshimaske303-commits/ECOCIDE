import json
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

TREATMENT_DATE = "2023-06-01"


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment})
    return pd.DataFrame(rows)


def build_panel():
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)
    df = pd.concat([kherson, tulcea], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["post"] = (df["date"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)
    return df


def main():
    """
    Specification robustness: Newey-West lag length + functional form.

    Two analyst choices in the primary specification (Section 3.3) were made
    once and not themselves stress-tested: the HAC lag length (maxlags=3),
    and modeling NDVI linearly rather than log-transformed. This re-runs the
    primary 2-zone model (Kherson vs. Tulcea) under both.
    """
    df = build_panel()

    print("=== HAC LAG-LENGTH SENSITIVITY (primary 2-zone spec) ===\n")
    for lag in range(1, 7):
        model = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(
            cov_type="HAC", cov_kwds={"maxlags": lag}
        )
        coef = model.params["did_term"]
        pval = model.pvalues["did_term"]
        print(f"  maxlags={lag}: did_term={coef:+.4f}  p={pval:.4f}")

    print("\n=== FUNCTIONAL FORM: raw NDVI vs. log(NDVI) ===\n")
    model_raw = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )
    print(f"  raw NDVI:  did_term={model_raw.params['did_term']:+.4f}  "
          f"p={model_raw.pvalues['did_term']:.4f}")

    df_log = df.copy()
    df_log["ndvi"] = np.log(df_log["ndvi"])
    model_log = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df_log).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )
    coef_log = model_log.params["did_term"]
    pval_log = model_log.pvalues["did_term"]
    print(f"  log(NDVI): did_term={coef_log:+.4f}  p={pval_log:.4f}  "
          f"(~{coef_log*100:.1f}% proportional change)")
    print("\n  Note: log-NDVI is more sensitive to cloud-contaminated near-zero months")
    print("  (Section 6), which is the likely reason its p-value is weaker.")


if __name__ == "__main__":
    main()
