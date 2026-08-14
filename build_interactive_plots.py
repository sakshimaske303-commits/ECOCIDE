"""Interactive Plotly versions of the three headline ECOCIDE statistical
charts. Event study recomputes the same OLS event-study regression the
static figure uses (same data, same formula); the other two reuse the
coefficients already reported in the static-figure scripts directly."""

import json
import os

import pandas as pd
import statsmodels.formula.api as smf
import plotly.graph_objects as go

OUT = "outputs/plots/interactive"
os.makedirs(OUT, exist_ok=True)

DARK_LAYOUT = dict(
    template="plotly_dark",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="#0a1628",
    font=dict(family="Inter, sans-serif", color="#F5F7FA"),
    margin=dict(t=90, b=60, l=220, r=60),
)

SIG_COLOR = "#e63946"
NONSIG_COLOR = "#6c757d"
ACCENT = "#00b4d8"


# ============================================================
# 1. EVENT STUDY — quarterly treatment effect on NDVI
# ============================================================
def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment})
    return pd.DataFrame(rows)


def build_event_study():
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)
    df = pd.concat([kherson, tulcea], ignore_index=True)
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
    model = smf.ols(formula, data=df).fit(cov_type="HAC", cov_kwds={"maxlags": 1})

    plot_quarters, coefs, ci_lower, ci_upper, colors, pvals = [], [], [], [], [], []
    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        if col_name in model.params.index:
            coef = model.params[col_name]
            ci = model.conf_int().loc[col_name]
            pval = model.pvalues[col_name]
            plot_quarters.append(q)
            coefs.append(coef)
            ci_lower.append(coef - ci[0])
            ci_upper.append(ci[1] - coef)
            colors.append(SIG_COLOR if pval < 0.05 else NONSIG_COLOR)
            pvals.append(pval)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=plot_quarters, y=coefs, mode="markers", marker=dict(size=12, color=colors, line=dict(color="white", width=1)),
        error_y=dict(type="data", symmetric=False, array=ci_upper, arrayminus=ci_lower, color=ACCENT, thickness=1.5, width=6),
        customdata=pvals,
        hovertemplate="Quarter %{x:+d}<br>Coef: %{y:+.4f}<br>p = %{customdata:.4f}<extra></extra>",
        showlegend=False,
    ))
    fig.add_hline(y=0, line_color="rgba(255,255,255,0.5)")
    fig.add_vline(x=0, line_color=ACCENT, line_dash="dash", annotation_text="Dam Destroyed (Quarter 0)", annotation_font_color=ACCENT)

    fig.update_layout(
        title="Event Study: Quarterly Treatment Effect on NDVI<br><sub>Relative to Kakhovka Dam Destruction (June 2023)</sub>",
        xaxis_title="Quarters relative to dam destruction", yaxis_title="Treatment effect on NDVI",
        height=560, **{**DARK_LAYOUT, "margin": dict(t=90, b=50, l=70, r=30)},
    )
    fig.write_html(f"{OUT}/event_study.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/event_study.html")


# ============================================================
# 2. CONTROL PANEL COMPARISON — DiD vs. each control individually
# ============================================================
def build_control_panel_comparison():
    ROWS = [
        {"label": "Kherson vs. Tulcea (primary specification)", "coef": -0.0703, "ci": (-0.1304, -0.0102), "p": 0.0219, "null": False},
        {"label": "Kherson vs. Galați", "coef": -0.0695, "ci": (-0.1308, -0.0082), "p": 0.0262, "null": False},
        {"label": "Kherson vs. Brăila", "coef": -0.0937, "ci": (-0.1461, -0.0413), "p": 0.0005, "null": False},
        {"label": "Kherson vs. Constanța", "coef": -0.0064, "ci": (-0.0580, 0.0452), "p": 0.8076, "null": True},
        {"label": "Pooled: all 4 controls (HAC)", "coef": -0.0600, "ci": (-0.1138, -0.0062), "p": 0.0289, "null": False, "pooled": True},
    ]
    labels = [r["label"] for r in ROWS][::-1]
    coefs = [r["coef"] for r in ROWS][::-1]
    los = [r["coef"] - r["ci"][0] for r in ROWS][::-1]
    his = [r["ci"][1] - r["coef"] for r in ROWS][::-1]
    colors = ["#00b4d8" if r.get("pooled") else ("#8a8a8a" if r["null"] else "#6c757d") for r in ROWS][::-1]
    pvals = [r["p"] for r in ROWS][::-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=coefs, y=labels, mode="markers",
        marker=dict(size=[14 if "Pooled" in l else 11 for l in labels], color=colors, line=dict(color="white", width=1)),
        error_x=dict(type="data", symmetric=False, array=his, arrayminus=los, color="rgba(255,255,255,0.4)", thickness=1.5, width=6),
        customdata=pvals,
        hovertemplate="%{y}<br>DiD coef: %{x:+.4f}<br>p = %{customdata:.4f}<extra></extra>",
        showlegend=False,
    ))
    fig.add_vline(x=0, line_color="#e63946", line_dash="dash")
    fig.update_layout(
        title="Multi-Control Robustness Check: Does the Effect Hold Against Each Control?<br>"
              "<sub>Kherson vs. each of 4 Danube/Black Sea control counties individually, plus the pooled panel</sub>",
        xaxis_title="did_term coefficient (95% CI, HAC standard errors)",
        height=520, **DARK_LAYOUT,
    )
    fig.write_html(f"{OUT}/control_panel_comparison.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/control_panel_comparison.html")


# ============================================================
# 3. ROBUSTNESS CHECK — classical OLS vs. Newey-West HAC
# ============================================================
def build_robustness_check():
    MODELS = [
        {"label": "Main DiD (broad baseline)", "coef": -0.0703, "classic_ci": (-0.1206, -0.0200), "hac_ci": (-0.1304, -0.0102), "classic_p": 0.007, "hac_p": 0.022},
        {"label": "Narrowed-baseline DiD", "coef": -0.1384, "classic_ci": (-0.2216, -0.0552), "hac_ci": (-0.2093, -0.0676), "classic_p": 0.0019, "hac_p": 0.0001},
        {"label": "Placebo (broad baseline)", "coef": 0.0148, "classic_ci": (-0.0778, 0.1075), "hac_ci": (-0.0425, 0.0722), "classic_p": 0.7411, "hac_p": 0.6124},
        {"label": "Placebo (narrowed baseline)", "coef": -0.1382, "classic_ci": (-0.3544, 0.0779), "hac_ci": (-0.2213, -0.0552), "classic_p": 0.1687, "hac_p": 0.0011},
    ]
    labels = [m["label"] for m in MODELS][::-1]

    fig = go.Figure()
    for spec_key, ci_key, p_key, color, name in [
        ("coef", "classic_ci", "classic_p", "#6c757d", "Classical OLS"),
        ("coef", "hac_ci", "hac_p", "#00b4d8", "Newey-West HAC"),
    ]:
        coefs = [m["coef"] for m in MODELS][::-1]
        los = [m[spec_key] - m[ci_key][0] for m in MODELS][::-1]
        his = [m[ci_key][1] - m[spec_key] for m in MODELS][::-1]
        pvals = [m[p_key] for m in MODELS][::-1]
        fig.add_trace(go.Scatter(
            x=coefs, y=labels, mode="markers", name=name,
            marker=dict(size=11, color=color, line=dict(color="white", width=1)),
            error_x=dict(type="data", symmetric=False, array=his, arrayminus=los, color=color, thickness=1.5, width=6),
            customdata=pvals,
            hovertemplate=f"%{{y}}<br>{name}<br>Coef: %{{x:+.4f}}<br>p = %{{customdata:.4f}}<extra></extra>",
        ))

    fig.add_vline(x=0, line_color="#e63946", line_dash="dash")
    fig.update_layout(
        title="Robustness: Classical vs. HAC Standard Errors<br>"
              "<sub>Point estimates and 95% confidence intervals across all four causal-inference models</sub>",
        xaxis_title="did_term coefficient (95% CI)",
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5),
        height=520, **DARK_LAYOUT,
    )
    fig.write_html(f"{OUT}/robustness_check.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/robustness_check.html")


if __name__ == "__main__":
    build_event_study()
    build_control_panel_comparison()
    build_robustness_check()
