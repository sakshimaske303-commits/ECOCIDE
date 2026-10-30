"""Interactive Plotly versions of the headline statistical charts.
All numbers are read from outputs/model_results.json (run
generate_model_results.py first); nothing is hard-coded here."""
import json
import os

import plotly.graph_objects as go

OUT = "outputs/plots/interactive"
os.makedirs(OUT, exist_ok=True)

LAYOUT = dict(template="plotly_white", font=dict(family="Inter, sans-serif"),
              margin=dict(t=90, b=60, l=230, r=60))
SIG, NS, HAC, CLS, POOL = "#C0392B", "#7F7F7F", "#1F77B4", "#7F7F7F", "#117A65"
LABEL = {"kherson": "Kherson", "tulcea": "Tulcea", "galati": "Galați", "braila": "Brăila", "constanta": "Constanța"}

with open("outputs/model_results.json", encoding="utf-8") as f:
    R = json.load(f)


def err(m):
    return m["ci"][1] - m["coef"], m["coef"] - m["ci"][0]


def build_event_study():
    rows = R["event_study"]["quarters"]
    fig = go.Figure(go.Scatter(
        x=[r["quarter"] for r in rows], y=[r["coef"] for r in rows], mode="markers",
        marker=dict(size=11, color=[SIG if r["p"] < 0.05 else NS for r in rows]),
        error_y=dict(type="data", symmetric=False, array=[err(r)[0] for r in rows],
                     arrayminus=[err(r)[1] for r in rows], color="#555555"),
        customdata=[[r["months"], r["p"], "yes" if r["bonferroni"] else "no"] for r in rows],
        hovertemplate="Quarter %{x:+d} (%{customdata[0]})<br>Gap vs reference: %{y:+.4f}"
                      "<br>HAC p = %{customdata[1]:.4f}<br>Survives Bonferroni: %{customdata[2]}<extra></extra>",
        showlegend=False))
    fig.add_hline(y=0, line_color="#333333")
    fig.add_vline(x=-0.5, line_dash="dash", annotation_text="June 2023")
    fig.update_layout(title="Quarterly event study, Kherson − Tulcea NDVI gap<br><sub>Reference quarter Mar–May 2023; "
                            "95% CIs, Newey-West HAC (maxlags=3)</sub>",
                      xaxis_title="Quarter relative to June 2023", yaxis_title="Gap relative to reference",
                      height=540, **{**LAYOUT, "margin": dict(t=90, b=60, l=70, r=30)})
    fig.write_html(f"{OUT}/event_study.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/event_study.html")


def build_control_panel_comparison():
    rows = [(f"Kherson vs {LABEL[z]}" + (" (primary)" if z == "tulcea" else ""), R["per_control"][z], NS)
            for z in ["tulcea", "galati", "braila", "constanta"]]
    rows.append(("Kherson vs mean of all 4 controls", R["pooled_did"], POOL))
    rows = rows[::-1]
    fig = go.Figure(go.Scatter(
        x=[m["coef"] for _, m, _ in rows], y=[l for l, _, _ in rows], mode="markers",
        marker=dict(size=12, color=[c for _, _, c in rows]),
        error_x=dict(type="data", symmetric=False, array=[err(m)[0] for _, m, _ in rows],
                     arrayminus=[err(m)[1] for _, m, _ in rows], color="#555555"),
        customdata=[m["p"] for _, m, _ in rows],
        hovertemplate="%{y}<br>DiD: %{x:+.4f}<br>HAC p = %{customdata:.3f}<extra></extra>", showlegend=False))
    fig.add_vline(x=0, line_dash="dash")
    fig.update_layout(title="Kherson against each control county and the pooled panel<br><sub>95% CIs, Newey-West HAC</sub>",
                      xaxis_title="DiD coefficient (NDVI units)", height=480, **LAYOUT)
    fig.write_html(f"{OUT}/control_panel_comparison.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/control_panel_comparison.html")


def build_robustness_check():
    models = [("main_did", "Primary DiD"), ("placebo_broad", "Placebo, fake date Jun 2022"),
              ("narrowed_did", "Narrowed-baseline DiD"), ("placebo_narrowed", "Narrowed placebo, fake Mar 2023")][::-1]
    fig = go.Figure()
    for key_ci, key_p, color, name in [("classic_ci", "classic_p", CLS, "Classical OLS"), ("ci", "p", HAC, "Newey-West HAC")]:
        fig.add_trace(go.Scatter(
            x=[R[k]["coef"] for k, _ in models], y=[l for _, l in models], mode="markers", name=name,
            marker=dict(size=11, color=color),
            error_x=dict(type="data", symmetric=False,
                         array=[R[k][key_ci][1] - R[k]["coef"] for k, _ in models],
                         arrayminus=[R[k]["coef"] - R[k][key_ci][0] for k, _ in models], color=color),
            customdata=[R[k][key_p] for k, _ in models],
            hovertemplate=f"%{{y}}<br>{name}<br>Coef: %{{x:+.4f}}<br>p = %{{customdata:.3f}}<extra></extra>"))
    fig.add_vline(x=0, line_dash="dash")
    fig.update_layout(title="Classical vs HAC confidence intervals<br><sub>Primary and narrowed-baseline models with their placebo tests</sub>",
                      xaxis_title="DiD coefficient (NDVI units)", legend=dict(orientation="h", y=1.08, x=0.5, xanchor="center"),
                      height=500, **LAYOUT)
    fig.write_html(f"{OUT}/robustness_check.html", include_plotlyjs="cdn")
    print("Saved:", f"{OUT}/robustness_check.html")


if __name__ == "__main__":
    build_event_study()
    build_control_panel_comparison()
    build_robustness_check()
