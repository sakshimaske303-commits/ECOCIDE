import json
import pandas as pd
import statsmodels.formula.api as smf

TREATMENT_DATE = "2023-06-01"
PRE_PERIOD_START = "2023-01-01"  # narrowed: only immediate pre-dam-destruction baseline

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

    # Narrowed window: Jan 2023 - Nov 2024, isolating the marginal effect
    # of the dam's destruction specifically, rather than the broader,
    # already-ongoing conflict baseline present since Feb 2022
    df = df[df["date"] >= PRE_PERIOD_START]

    df["post"] = (df["date"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)

    model = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit()
    print(model.summary())

    df.to_csv("data/did_panel_ndvi_narrowed.csv", index=False)


if __name__ == "__main__":
    main()