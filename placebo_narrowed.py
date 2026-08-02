import json
import pandas as pd
import statsmodels.formula.api as smf

FAKE_TREATMENT_DATE = "2023-03-01"  # arbitrary fake date within the narrowed pre-period

def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment})
    return pd.DataFrame(rows)


def main():
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)

    df = pd.concat([kherson, tulcea], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])

    # Use only the genuinely pre-conflict-event window (Jan 2023 - May
    # 2023), with a fake mid-window treatment date, to test whether an
    # arbitrary split within this specific narrowed baseline also shows
    # a spurious "effect"
    df = df[(df["date"] >= "2023-01-01") & (df["date"] < "2023-06-01")]

    df["post"] = (df["date"] >= FAKE_TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]

    # Newey-West HAC standard errors (Newey & West, 1987), maxlags=1 given
    # the very short (10-observation) narrowed window. Note: under this
    # correction the coefficient becomes statistically significant (unlike
    # under classical OLS) — a genuine validation failure for the
    # narrowed-baseline specification, not a computational artifact. See
    # Research_Paper.md Sections 4.3/4.4 for the full discussion.
    model = smf.ols("ndvi ~ treatment + post + did_term", data=df).fit(
        cov_type="HAC", cov_kwds={"maxlags": 1}
    )
    print("PLACEBO TEST (narrowed window, fake date: March 2023)")
    print(f"did_term coefficient: {model.params['did_term']:.4f}")
    print(f"p-value: {model.pvalues['did_term']:.4f}")


if __name__ == "__main__":
    main()