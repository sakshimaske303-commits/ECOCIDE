import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 FLOOD ANALYSIS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Verified Multi-Sensor Flood Progression</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Flood extent was sourced from UNOSAT (United Nations Satellite Centre), combining verified 
observations from five independent satellite sensors — ICEYE (radar), Landsat-9, SkySat, 
WorldView-3, and MODIS Aqua/Terra — rather than derived independently from a single sensor's 
raw bands, following the same approach used in the existing published literature on this event.
""")

st.markdown("---")

st.markdown("### Flood Progression Timeline")

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "flood_hydrograph.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Flood hydrograph image not found.")

col1, col2, col3, col4, col5 = st.columns(5)
flood_data = [
    (col1, "6 Jun", "122.50", "Initial breach"),
    (col2, "8 Jun", "260.92", "Expanding"),
    (col3, "9 Jun", "464.18", "Peak flood"),
    (col4, "13 Jun", "179.92", "Receding"),
    (col5, "21 Jun", "21.17", "Near-recovered"),
]

for col, date, area, note in flood_data:
    with col:
        st.markdown(f"""
        <div class="forensic-card" style="text-align: center; min-height: 140px;">
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 6px;">{date}</p>
            <p style="color: {PALETTE['water']}; font-weight: 900; font-size: 1.4rem; margin-bottom: 6px;">{area}</p>
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.7rem; margin: 0;">km² — {note}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Geospatial Flood Extent")

image_path2 = os.path.join(PROJECT_ROOT, "outputs", "plots", "flood_extent_map.png")
if os.path.exists(image_path2):
    st.image(image_path2, use_container_width=True)
else:
    st.warning("Flood extent map not found.")

st.markdown("---")

st.warning("""
**Reservoir Water-Loss — A Genuine Data Limitation:** No statistical control-zone comparison was 
possible for reservoir water loss specifically, since Tulcea's Danube Delta has no equivalent 
upstream reservoir infrastructure. The Kakhovka reservoir's pre-breach extent (approximately 
2,155 km², 18.2 km³ water volume) is reported descriptively as supporting evidence of physical 
scale, not as an independently causally-tested finding.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: UNOSAT Multi-Sensor Flood Mapping</p>",
    unsafe_allow_html=True,
)