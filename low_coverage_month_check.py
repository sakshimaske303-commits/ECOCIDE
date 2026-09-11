import json
import pandas as pd
import statsmodels.formula.api as smf

TREATMENT_DATE = "2023-06-01"
VALID_FRACTION_THRESHOLD = 0.50


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        stats = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]
        ndvi = stats["mean"]
        sample_count = stats.get("sampleCount")
        no_data_count = stats.get("noDataCount", 0)
        valid_frac = (1 - no_data_count / sample_count) if sample_count else None
        rows.append({
            "date": date, "ndvi": ndvi, "treatment": is_treatment,
            "zone": zone_name, "valid_frac": valid_frac,
        })
    return pd.DataFrame(rows)


def main():
    """
    Sensitivity to low-coverage months (Section 4.10).

    Scene-level cloud filtering (maxCloudCoverage<=40, Section 3.2) screens
    images before aggregation, but does not guarantee every resulting
    monthly mean rests on an adequate sample of valid pixels. This flags
    every zone-month below a 50% valid-pixel-fraction threshold (using the
    sampleCount/noDataCount fields already present in the raw Sentinel Hub
    output) and re-estimates the primary spec with any such months dropped.
    """
    zones = ["kherson", "tulcea", "galati", "constanta", "braila"]
    all_df = pd.concat(
        [load_ndvi(z, is_treatment=1 if z == "kherson" else 0) for z in zones],
        ignore_index=True,
    )

    print("=== LOW-COVERAGE MONTHS (valid-pixel fraction < 50%) ===\n")
    low = all_df[all_df["valid_frac"] < VALID_FRACTION_THRESHOLD]
    if low.empty:
        print("  None found.")
    else:
        for _, row in low.iterrows():
            print(f"  {row['zone']:12s} {row['date']}  valid_frac={row['valid_frac']:.3f}")

    # Re-estimate primary spec (Kherson vs Tulcea) with low-coverage months dropped
    df = all_df[all_df["zone"].isin(["kherson", "tulcea"])].copy()
    df["date_dt"] = pd.to_datetime(df["date"])
    df["post"] = (df["date_dt"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date_dt"].dt.month.astype(str)

    model_a = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )

    df_b = df[~(df["valid_frac"] < VALID_FRACTION_THRESHOLD)]
    model_b = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df_b).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )

    print(f"\n=== MODEL A (all months, n={len(df)}) ===")
    print(f"  did_term = {model_a.params['did_term']:+.4f}  HAC p = {model_a.pvalues['did_term']:.4f}")
    print(f"\n=== MODEL B (low-coverage months dropped, n={len(df_b)}) ===")
    print(f"  did_term = {model_b.params['did_term']:+.4f}  HAC p = {model_b.pvalues['did_term']:.4f}")


if __name__ == "__main__":
    main()
