import json
import pandas as pd
import statsmodels.formula.api as smf

FAKE_TREATMENT_DATE = "2022-06-01"  # one year before the real event

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

    # Use only pre-conflict data (before the real June 2023 event) to test
    # whether a fake, earlier treatment date also produces a "significant"
    # effect — if it does, the real result may just reflect a general trend
    df = df[df["date"] < "2023-06-01"]

    df["post"] = (df["date"] >= FAKE_TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)

    model = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit()
    print("PLACEBO TEST (fake treatment date: June 2022)")
    print(f"did_term coefficient: {model.params['did_term']:.4f}")
    print(f"p-value: {model.pvalues['did_term']:.4f}")


if __name__ == "__main__":
    main()