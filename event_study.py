import json
import pandas as pd
import statsmodels.formula.api as smf

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
    df["month_num"] = df["date"].dt.month.astype(str)

    treatment_date = pd.Timestamp("2023-06-01")
    rel_month = ((df["date"].dt.year - treatment_date.year) * 12 +
                 (df["date"].dt.month - treatment_date.month))

    # Bin into quarters relative to the event, rather than individual
    # months, to keep the number of parameters well below the number of
    # observations (70) and avoid the rank-deficiency seen with full
    # monthly resolution
    df["rel_quarter"] = (rel_month // 3)

    quarters = sorted(df["rel_quarter"].unique())
    ref_quarter = -1  # quarter immediately before treatment as reference
    quarters = [q for q in quarters if q != ref_quarter]

    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        df[col_name] = ((df["rel_quarter"] == q) & (df["treatment"] == 1)).astype(int)

    event_terms = " + ".join([f"evt_q{q}".replace("-", "neg") for q in quarters])
    formula = f"ndvi ~ treatment + C(month_num) + {event_terms}"

    model = smf.ols(formula, data=df).fit()

    print("Event study coefficients (quarterly bins relative to June 2023):\n")
    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        if col_name in model.params.index:
            coef = model.params[col_name]
            pval = model.pvalues[col_name]
            sig = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else ""
            print(f"  Quarter {q:+3d}: coef={coef:+.4f}  p={pval:.4f} {sig}")


if __name__ == "__main__":
    main()