"""
eco_core.py — single shared analysis engine for ECOCIDE.

Every model script in this repository (did_model.py, placebo_test.py,
event_study.py, ... ) and generate_model_results.py call the functions
below, so every number in the paper, dashboard and figures comes from one
implementation.

Estimation approach
-------------------
Each comparison is reduced to ONE monthly "gap" time series:

    gap_t = NDVI(treated zone, month t) - mean NDVI(control zone(s), month t)

and the Difference-in-Differences effect is estimated as

    gap_t = a + b * post_t (+ month-of-year effects) + e_t

For a balanced panel this gives exactly the same point estimate as the
stacked two-way regression `ndvi ~ treatment + post + did_term + C(month)`
used in earlier versions of this project. The difference is inference:
the earlier scripts applied Newey-West HAC standard errors to a stacked
dataframe (all Kherson months, then all Tulcea months), so the HAC "lags"
ran across the join between zones and ignored the fact that both zones are
observed in the same month. Running HAC on the single gap series makes the
lag structure mean what it says: `maxlags` calendar months.

Inference: Newey-West HAC, maxlags=3 unless stated, small-sample t
distribution (use_t=True) everywhere, so every p-value in the project uses
the same convention.
"""
import json
import os

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

NDVI_DIR = os.environ.get("ECO_NDVI_DIR", "data/ndvi_v3")
EVENT_DATE = pd.Timestamp("2023-06-01")  # dam destroyed 6 June 2023; monthly data
TREATED = "kherson"
CONTROLS = ["tulcea", "galati", "constanta", "braila"]
PRIMARY_CONTROL = "tulcea"
ALL_ZONES = [TREATED] + CONTROLS
HAC_LAGS = 3

ZONE_LABELS = {
    "kherson": "Kherson",
    "tulcea": "Tulcea",
    "galati": "Galați",
    "constanta": "Constanța",
    "braila": "Brăila",
}


def load_zone(zone, ndvi_dir=None):
    """Monthly mean NDVI and valid-pixel fraction for one zone."""
    ndvi_dir = ndvi_dir or NDVI_DIR
    with open(os.path.join(ndvi_dir, f"{zone}_ndvi_monthly.json")) as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        stats = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]
        n = stats.get("sampleCount")
        nd = stats.get("noDataCount", 0)
        rows.append({
            "date": pd.Timestamp(entry["interval"]["from"][:7] + "-01"),
            "ndvi": stats["mean"],
            "valid_frac": (1 - nd / n) if n else np.nan,
        })
    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def load_all(ndvi_dir=None):
    return {z: load_zone(z, ndvi_dir) for z in ALL_ZONES}


def gap_series(data, treated, controls, min_valid=None, log=False):
    """Monthly treated-minus-mean(controls) NDVI gap.

    min_valid: drop any zone-month whose valid-pixel fraction is below this
    threshold before forming the gap (a month is dropped entirely if the
    treated zone or all of its controls are missing).
    """
    frames = []
    for z in [treated] + list(controls):
        d = data[z][["date", "ndvi", "valid_frac"]].copy()
        if min_valid is not None:
            d.loc[d["valid_frac"] < min_valid, "ndvi"] = np.nan
        if log:
            d["ndvi"] = np.log(d["ndvi"])
        frames.append(d.set_index("date")["ndvi"].rename(z))
    w = pd.concat(frames, axis=1).sort_index()
    ctrl_mean = w[list(controls)].mean(axis=1, skipna=True)
    gap = (w[treated] - ctrl_mean).rename("gap")
    out = gap.dropna().reset_index()
    out["month"] = out["date"].dt.month.astype(str)
    return out


def _fit(df, formula, term, maxlags=HAC_LAGS):
    hac = smf.ols(formula, df).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags}, use_t=True)
    cls = smf.ols(formula, df).fit()
    lo, hi = hac.conf_int().loc[term]
    clo, chi = cls.conf_int().loc[term]
    return {
        "coef": float(hac.params[term]),
        "se": float(hac.bse[term]),
        "ci": [float(lo), float(hi)],
        "p": float(hac.pvalues[term]),
        "classic_ci": [float(clo), float(chi)],
        "classic_p": float(cls.pvalues[term]),
        "n_months": int(hac.nobs),
        "r2": float(hac.rsquared),
    }


def did(data, treated=TREATED, controls=(PRIMARY_CONTROL,), event_date=EVENT_DATE,
        start=None, end=None, month_fe=False, maxlags=HAC_LAGS, min_valid=None, log=False):
    """DiD effect on the monthly gap series (see module docstring)."""
    g = gap_series(data, treated, controls, min_valid=min_valid, log=log)
    if start is not None:
        g = g[g["date"] >= pd.Timestamp(start)]
    if end is not None:
        g = g[g["date"] < pd.Timestamp(end)]
    g = g.copy()
    g["post"] = (g["date"] >= pd.Timestamp(event_date)).astype(int)
    formula = "gap ~ post + C(month)" if month_fe else "gap ~ post"
    res = _fit(g, formula, "post", maxlags)
    res["months_dropped"] = int(35 - len(g)) if (start is None and end is None) else None
    return res


def event_study(data, treated=TREATED, controls=(PRIMARY_CONTROL,), ref_quarter=-1,
                maxlags=HAC_LAGS, month_fe=False):
    """Quarterly event study on the gap series. Quarter q covers relative
    months 3q..3q+2 (quarter 0 = Jun-Aug 2023). Reference quarter = -1
    (Mar-May 2023)."""
    g = gap_series(data, treated, controls).copy()
    rel = (g["date"].dt.year - EVENT_DATE.year) * 12 + (g["date"].dt.month - EVENT_DATE.month)
    g["rq"] = rel // 3
    quarters = [q for q in sorted(g["rq"].unique()) if q != ref_quarter]
    names = {}
    for q in quarters:
        c = f"q{q}".replace("-", "m")
        g[c] = (g["rq"] == q).astype(int)
        names[q] = c
    formula = "gap ~ " + " + ".join(names.values()) + (" + C(month)" if month_fe else "")
    hac = smf.ols(formula, g).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags}, use_t=True)
    rows = []
    for q in quarters:
        c = names[q]
        lo, hi = hac.conf_int().loc[c]
        in_bin = g.loc[g["rq"] == q, "date"]
        first, last = in_bin.min(), in_bin.max()
        rows.append({
            "quarter": int(q),
            "months": f"{first:%b %Y}–{last:%b %Y}" if first != last else f"{first:%b %Y}",
            "n_months": int(len(in_bin)),
            "coef": float(hac.params[c]),
            "ci": [float(lo), float(hi)],
            "p": float(hac.pvalues[c]),
        })
    return rows


def bonferroni_bh(pvals, alpha=0.05):
    m = len(pvals)
    bonf = [p < alpha / m for p in pvals]
    order = np.argsort(pvals)
    last = 0
    for rank, idx in enumerate(order, start=1):
        if pvals[idx] <= rank / m * alpha:
            last = rank
    bh = [False] * m
    for rank, idx in enumerate(order, start=1):
        bh[idx] = rank <= last
    return alpha / m, bonf, bh


def legacy_stacked_did(data, controls=(PRIMARY_CONTROL,), maxlags=HAC_LAGS):
    """The specification used in earlier versions (stacked OLS, HAC on row
    order, normal distribution). Kept ONLY so the change in reported
    p-values can be documented; not used for any current result."""
    rows = []
    for z in [TREATED] + list(controls):
        d = data[z].copy()
        d["treatment"] = int(z == TREATED)
        rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    df["post"] = (df["date"] >= EVENT_DATE).astype(int)
    df["did_term"] = df["treatment"] * df["post"]
    df["month"] = df["date"].dt.month.astype(str)
    m = smf.ols("ndvi ~ treatment + post + did_term + C(month)", df).fit(
        cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return {"coef": float(m.params["did_term"]), "p": float(m.pvalues["did_term"])}


def fmt(r, digits=4):
    return (f"coef={r['coef']:+.{digits}f}  95% CI [{r['ci'][0]:+.3f}, {r['ci'][1]:+.3f}]  "
            f"HAC p={r['p']:.3f}  (classical p={r['classic_p']:.3f}, n={r['n_months']} months)")
