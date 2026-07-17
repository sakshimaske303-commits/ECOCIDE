import json
import pandas as pd
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


def main():
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)

    df = pd.concat([kherson, tulcea], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["post"] = (df["date"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    # Month fixed effects control for seasonal vegetation cycles,
    # which otherwise dominate NDVI variance and mask the treatment effect
    df["month"] = df["date"].dt.month.astype(str)

    model = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit()
    print(model.summary())

    df.to_csv("data/did_panel_ndvi.csv", index=False)


if __name__ == "__main__":
    main()