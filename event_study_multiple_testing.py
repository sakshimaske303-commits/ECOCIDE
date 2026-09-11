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


def bonferroni(pvals, alpha=0.05):
    m = len(pvals)
    threshold = alpha / m
    return threshold, {k: (v < threshold) for k, v in pvals.items()}


def benjamini_hochberg(pvals, alpha=0.05):
    """Benjamini & Hochberg (1995) false-discovery-rate procedure."""
    m = len(pvals)
    ordered = sorted(pvals.items(), key=lambda kv: kv[1])
    sig = {k: False for k in pvals}
    last_ok_rank = 0
    for i, (k, p) in enumerate(ordered, start=1):
        if p <= (i / m) * alpha:
            last_ok_rank = i
    for i, (k, p) in enumerate(ordered, start=1):
        sig[k] = i <= last_ok_rank
    return sig


def main():
    """
    Multiple-testing correction for the quarterly event study (Section 4.3).

    The event study tests ~11 quarterly coefficients against one reference
    quarter. At a nominal alpha=0.05 per test, the chance of at least one
    false positive across that many tests is well above 5% by construction.
    This re-reports the same HAC event-study coefficients from event_study.py
    alongside Bonferroni (conservative, family-wise) and Benjamini-Hochberg
    (1995) (less conservative, false-discovery-rate) corrected significance.
    """
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)
    df = pd.concat([kherson, tulcea], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["month_num"] = df["date"].dt.month.astype(str)

    treatment_date = pd.Timestamp("2023-06-01")
    rel_month = ((df["date"].dt.year - treatment_date.year) * 12 +
                 (df["date"].dt.month - treatment_date.month))
    df["rel_quarter"] = rel_month // 3

    quarters = sorted(df["rel_quarter"].unique())
    ref_quarter = -1
    quarters = [q for q in quarters if q != ref_quarter]

    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        df[col_name] = ((df["rel_quarter"] == q) & (df["treatment"] == 1)).astype(int)

    event_terms = " + ".join([f"evt_q{q}".replace("-", "neg") for q in quarters])
    formula = f"ndvi ~ treatment + C(month_num) + {event_terms}"
    model = smf.ols(formula, data=df).fit(cov_type="HAC", cov_kwds={"maxlags": 1})

    pvals = {}
    coefs = {}
    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        if col_name in model.params.index:
            pvals[q] = model.pvalues[col_name]
            coefs[q] = model.params[col_name]

    bonf_threshold, bonf_sig = bonferroni(pvals)
    bh_sig = benjamini_hochberg(pvals)

    print("=== EVENT STUDY: MULTIPLE-TESTING CORRECTION ===\n")
    print(f"{len(pvals)} quarterly coefficients tested against 1 reference quarter.")
    print(f"Bonferroni family-wise threshold (alpha=0.05): p < {bonf_threshold:.5f}\n")
    print(f"{'quarter':>8s} {'coef':>10s} {'raw p':>8s}  {'raw@.05':>7s}  {'bonferroni':>10s}  {'BH-FDR':>7s}")
    for q in quarters:
        raw_sig = "*" if pvals[q] < 0.05 else ""
        print(f"{q:+8d} {coefs[q]:+10.4f} {pvals[q]:8.4f}  {raw_sig:>7s}  "
              f"{'*' if bonf_sig[q] else '':>10s}  {'*' if bh_sig[q] else '':>7s}")


if __name__ == "__main__":
    main()
