import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📈 EXPLORE TRENDS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Interactive NDVI Time Series</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")


def load_ndvi(zone_name):
    with open(os.path.join(PROJECT_ROOT, "data", "ndvi", f"{zone_name}_ndvi_monthly.json")) as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = pd.to_datetime(entry["interval"]["from"][:7] + "-01")
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi})
    return pd.DataFrame(rows)


kherson = load_ndvi("kherson")
tulcea = load_ndvi("tulcea")

st.markdown("### Select Zones to Compare")

zones_to_show = st.multiselect(
    "Zones",
    options=["Kherson (Treatment)", "Tulcea (Control)"],
    default=["Kherson (Treatment)", "Tulcea (Control)"],
)

fig = go.Figure()

if "Kherson (Treatment)" in zones_to_show:
    fig.add_trace(go.Scatter(
        x=kherson["date"], y=kherson["ndvi"], mode="lines+markers",
        name="Kherson (Treatment)", line=dict(color=PALETTE["damage"], width=2.5)
    ))

if "Tulcea (Control)" in zones_to_show:
    fig.add_trace(go.Scatter(
        x=tulcea["date"], y=tulcea["ndvi"], mode="lines+markers",
        name="Tulcea (Control)", line=dict(color=PALETTE["accent"], width=2.5)
    ))

fig.add_vline(x=pd.Timestamp("2023-06-01").timestamp() * 1000, line_dash="dash",
              line_color="#F5F7FA", opacity=0.6)
fig.add_annotation(x=pd.Timestamp("2023-06-01"), y=1.05, yref="paper",
                    text="Dam Destroyed", showarrow=False, font=dict(color="#F5F7FA", size=11))

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Date",
    yaxis_title="NDVI",
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#F5F7FA"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    margin=dict(t=60, b=40, l=40, r=40),
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.markdown("### 🎛️ Live Difference Calculator")

col1, col2 = st.columns(2)
with col1:
    date1 = st.selectbox("Compare Month A", kherson["date"].dt.strftime("%Y-%m").tolist(), index=0)
with col2:
    date2 = st.selectbox("Compare Month B", kherson["date"].dt.strftime("%Y-%m").tolist(),
                          index=len(kherson) - 1)

k_val1 = kherson[kherson["date"].dt.strftime("%Y-%m") == date1]["ndvi"].values[0]
k_val2 = kherson[kherson["date"].dt.strftime("%Y-%m") == date2]["ndvi"].values[0]
t_val1 = tulcea[tulcea["date"].dt.strftime("%Y-%m") == date1]["ndvi"].values[0]
t_val2 = tulcea[tulcea["date"].dt.strftime("%Y-%m") == date2]["ndvi"].values[0]

k_diff = k_val2 - k_val1
t_diff = t_val2 - t_val1
did_diff = k_diff - t_diff

c1, c2, c3 = st.columns(3)
c1.metric("Kherson Change", f"{k_diff:+.4f}")
c2.metric("Tulcea Change", f"{t_diff:+.4f}")
c3.metric("Difference-in-Differences", f"{did_diff:+.4f}")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: Sentinel-2 (Copernicus Data Space Ecosystem)</p>",
    unsafe_allow_html=True,
)