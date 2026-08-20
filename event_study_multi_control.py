import json
import pandas as pd
import statsmodels.formula.api as smf

CONTROL_ZONES = ["tulcea", "galati", "constanta", "braila"]


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment, "zone": zone_name})
    return pd.DataFrame(rows)


def main():
    kherson = load_ndvi("kherson", is_treatment=1)
    controls = pd.concat(
        [load_ndvi(zone, is_treatment=0) for zone in CONTROL_ZONES], ignore_index=True
    )
    df = pd.concat([kherson, controls], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["month_num"] = df["date"].dt.month.astype(str)

    treatment_date = pd.Timestamp("2023-06-01")
    rel_month = ((df["date"].dt.year - treatment_date.year) * 12 +
                 (df["date"].dt.month - treatment_date.month))
    df["rel_quarter"] = (rel_month // 3)

    quarters = sorted(df["rel_quarter"].unique())
    ref_quarter = -1
    quarters = [q for q in quarters if q != ref_quarter]

    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        df[col_name] = ((df["rel_quarter"] == q) & (df["treatment"] == 1)).astype(int)

    event_terms = " + ".join([f"evt_q{q}".replace("-", "neg") for q in quarters])
    formula = f"ndvi ~ treatment + C(month_num) + {event_terms}"

    # Cluster-robust is worse here than in the pooled DiD: 5 clusters vs ~24 params ->
    # rank-deficient (rank 4), some SEs come out ~1e-16 (not real). Shown for the record; HAC is the actual spec.
    model_cluster = smf.ols(formula, data=df).fit(cov_type="cluster", cov_kwds={"groups": df["zone"]})
    model_hac = smf.ols(formula, data=df).fit(cov_type="HAC", cov_kwds={"maxlags": 1})

    print("Multi-control event study — cluster-robust (NOT reliable at this parameter count, shown for the record):\n")
    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        if col_name in model_cluster.params.index:
            coef = model_cluster.params[col_name]
            se = model_cluster.bse[col_name]
            print(f"  Quarter {q:+3d}: coef={coef:+.4f}  se={se:.2e}")

    print("\nMulti-control event study — HAC (the specification actually reported):\n")
    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        if col_name in model_hac.params.index:
            coef = model_hac.params[col_name]
            pval = model_hac.pvalues[col_name]
            sig = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else ""
            print(f"  Quarter {q:+3d}: coef={coef:+.4f}  p={pval:.4f} {sig}")


if __name__ == "__main__":
    main()
