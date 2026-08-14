import streamlit as st
import streamlit.components.v1 as components
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🗺️ INTERACTIVE MAPS &amp; PLOTS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Explore Verified Flood Extent and Headline Charts Live</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Interactive map of verified UNOSAT flood-extent polygons across three dates (6 June, 9 June,
21 June 2023), built in QGIS, plus the three headline statistical charts as hoverable,
toggleable plots instead of flat images.
""")

st.markdown("---")

MAP_SERVER_BASE = "https://sakshimaske303-commits.github.io/ECOCIDE/dashboard/static"
map_url = f"{MAP_SERVER_BASE}/kherson_flood_extent_webmap/index.html"

components.iframe(src=map_url, height=600, scrolling=True)

st.markdown(f"""
<div class="forensic-card" style="margin-top: 12px;">
    <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">Map Legend</p>
    <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
        🟢 Mint outline — Kherson Oblast boundary &nbsp;|&nbsp;
        🟠 Orange — Flood extent, 6 June &nbsp;|&nbsp;
        🔴 Red — Flood extent, 9 June (peak) &nbsp;|&nbsp;
        🔵 Cyan — Flood extent, 21 June (recession)
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: #B0BEC5;'>Interactive Plots</h3>", unsafe_allow_html=True)

PLOTS = {
    "Event Study — Quarterly Treatment Effect on NDVI": "outputs/plots/interactive/event_study.html",
    "Multi-Control Robustness Check": "outputs/plots/interactive/control_panel_comparison.html",
    "Classical vs. HAC Standard Errors": "outputs/plots/interactive/robustness_check.html",
}

plot_choice = st.selectbox("Select a chart", list(PLOTS.keys()))
plot_path = os.path.join(PROJECT_ROOT, PLOTS[plot_choice])
if os.path.exists(plot_path):
    with open(plot_path, "r", encoding="utf-8") as f:
        plot_html = f.read()
    components.html(plot_html, height=600, scrolling=True)
else:
    st.warning("Chart file not found.")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Map built in QGIS, exported via QGIS2Web; plots built with Plotly</p>",
    unsafe_allow_html=True,
)