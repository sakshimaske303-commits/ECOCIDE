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
Interactive map of three UNOSAT flood-extent layers (6 June and 9 June: Sentinel-3; 21 June:
Sentinel-1), built in Python with folium, plus three statistical charts whose numbers are read from
the project's results file.
""")

st.markdown("---")

MAP_SERVER_BASE = "https://sakshimaske303-commits.github.io/ECOCIDE/dashboard/static"
map_url = f"{MAP_SERVER_BASE}/kherson_flood_extent_webmap/index.html"

components.iframe(src=map_url, height=600, scrolling=True)

st.markdown(f"""
<div class="forensic-card" style="margin-top: 12px;">
    <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">Map Legend</p>
    <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
        Mint outline — Kherson Oblast boundary &nbsp;|&nbsp;
        Orange — 6 June (Sentinel-3) &nbsp;|&nbsp;
        Red — 9 June (Sentinel-3) &nbsp;|&nbsp;
        Cyan — 21 June (Sentinel-1). Layers differ in sensor and analysis extent.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<h3 style='text-align: center; color: #B0BEC5;'>Interactive Plots</h3>", unsafe_allow_html=True)

PLOTS = {
    "Event Study — Quarterly Treatment Effect on NDVI": "outputs/plots/interactive/event_study.html",
    "Kherson vs Each Control and Pooled": "outputs/plots/interactive/control_panel_comparison.html",
    "Primary and Placebo Estimates (Classical vs HAC)": "outputs/plots/interactive/robustness_check.html",
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
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Map built directly in Python (folium); plots built with Plotly</p>",
    unsafe_allow_html=True,
)