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
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment, "zone": zone_name})
    return pd.DataFrame(rows)


def main():
    kherson = load_ndvi("kherson", is_treatment=1)
    controls = pd.concat(
        [load_ndvi(zone, is_treatment=0) for zone in CONTROL_ZONES], ignore_index=True
    )

    df = pd.concat([kherson, controls], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["post"] = (df["date"] >= TREATMENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)

    # With five geographic units (one treatment, four control), clustering by
    # zone is mathematically defined — though still thin. Standard guidance
    # wants 30-40+ clusters for the asymptotic cluster-robust theory to be
    # trustworthy, and few-cluster settings are known to understate standard
    # errors — so this is reported as a useful cross-check, not a substitute
    # for a properly powered multi-unit panel. Newey-West HAC is kept as a
    # parallel specification for direct comparability with the primary
    # single-control specification. statsmodels does flag this model's
    # cluster covariance as rank-deficient (rank 4 of 14 constraints) given
    # only 5 clusters against 14 parameters here — did_term itself still
    # comes out with a sane, non-degenerate standard error, but the
    # coefficient-by-coefficient reliability of the rest of the cluster-robust
    # table is genuinely thinner than the HAC specification next to it.
    model_cluster = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(
        cov_type="cluster", cov_kwds={"groups": df["zone"]}
    )
    model_hac = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=df).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )

    print("=== Multi-control panel: cluster-robust SEs (clustered by zone) ===")
    print(model_cluster.summary())
    print("\n=== Same panel: Newey-West HAC SEs, for comparison with the primary spec ===")
    print(model_hac.summary())

    df.to_csv("data/did_panel_ndvi_multi_control.csv", index=False)

    # Per-control-zone check: does the treatment effect hold up against each
    # control individually, or is it an artifact of pooling four of them?
    print("\n=== Per-control-zone check (treatment vs. each control alone) ===")
    for zone in CONTROL_ZONES:
        pair = df[df["zone"].isin(["kherson", zone])]
        m = smf.ols("ndvi ~ treatment + post + did_term + C(month)", data=pair).fit(
            cov_type="HAC", cov_kwds={"maxlags": 3}
        )
        coef = m.params["did_term"]
        pval = m.pvalues["did_term"]
        print(f"  kherson vs {zone:12s}: did_term={coef:+.4f}  p={pval:.4f}")


if __name__ == "__main__":
    main()
