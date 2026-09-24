import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
from results import FLOOD
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 FLOOD ANALYSIS</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>UNOSAT Flood-Extent Observations</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Flood extent comes from UNOSAT's FL20230606UKR product package (UNITAR/UNOSAT, 2023). Each
layer is a separate observation from one sensor with its own analysis extent, and UNOSAT labels
these analyses preliminary and not yet validated in the field. Areas below are computed from the
layers themselves by `flood_progression.py` (equal-area projection).
""")

st.markdown("---")

st.markdown("### Flood-Extent Observations by Sensor")

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "flood_hydrograph.png")
if os.path.exists(image_path):
    st.image(image_path, width="stretch")
else:
    st.warning("Flood hydrograph image not found.")

rows = FLOOD["layers"]
cols = st.columns(len(rows))
for col, r in zip(cols, rows):
    note = r["sensor"]
    if r["cloud_km2"] > 1000:
        note += f" · {r['cloud_km2']/r['analysis_extent_km2']:.0%} cloud-obscured"
    with col:
        st.markdown(f"""
        <div class="forensic-card" style="text-align: center; min-height: 150px;">
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.75rem; text-transform: uppercase; margin-bottom: 6px;">{r['date'][8:]} Jun</p>
            <p style="color: {PALETTE['water']}; font-weight: 900; font-size: 1.3rem; margin-bottom: 6px;">{r['flood_km2']:.1f}</p>
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.7rem; margin: 0;">km² — {note}</p>
        </div>
        """, unsafe_allow_html=True)

st.info(f"""
The largest single-sensor figure is ICEYE radar on 7 June ({rows[1]['flood_km2']:.1f} km², within a
{rows[1]['analysis_extent_km2']:,.0f} km² analysis area); the coarse-resolution Sentinel-3 layer for 9 June
maps {rows[3]['flood_km2']:.1f} km². UNOSAT's cumulative 6–9 June composite of all sensors is
{FLOOD['composite_6_9_june']['flood_km2']:.0f} km². Because sensors and extents differ, these points show the
flood's rise and recession only qualitatively.
""")

st.markdown("---")

st.markdown("### Geospatial Flood Extent")

image_path2 = os.path.join(PROJECT_ROOT, "outputs", "plots", "flood_extent_map.png")
if os.path.exists(image_path2):
    st.image(image_path2, width="stretch")
else:
    st.warning("Flood extent map not found.")

st.markdown("---")

st.warning("""
**Reservoir context (documented values, not computed here):** the Kakhovka reservoir held about
18.2 km³ over roughly 2,155 km² before the breach. These figures indicate physical scale only; no
control-zone comparison exists for a reservoir collapse, so they are not a tested result.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: UNOSAT FL20230606UKR (preliminary, not field-validated)</p>",
    unsafe_allow_html=True,
)