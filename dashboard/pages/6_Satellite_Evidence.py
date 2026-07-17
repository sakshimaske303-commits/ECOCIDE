import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🛰️ SATELLITE EVIDENCE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Before / After True-Color Imagery</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Sentinel-2 true-color imagery (bands B04/B03/B02) was acquired programmatically via the 
Copernicus Data Space Ecosystem for the exact same bounding box before and after the Kakhovka 
Dam's destruction — ensuring both images share identical geographic extent for direct visual 
comparison, rather than being manually selected from differing viewports.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 12px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 900; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 1px;">BEFORE</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.9rem; font-weight: 600;">April – May 2023</p>
    </div>
    """, unsafe_allow_html=True)
    before_path = os.path.join(PROJECT_ROOT, "data", "satellite_imagery", "before_may2023_v2.png")
    if os.path.exists(before_path):
        st.image(before_path, use_container_width=True)
    else:
        st.warning("Before-image not found.")

with col2:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 12px;">
        <p style="color: {PALETTE['damage']}; font-weight: 900; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 1px;">AFTER</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.9rem; font-weight: 600;">July 2023</p>
    </div>
    """, unsafe_allow_html=True)
    after_path = os.path.join(PROJECT_ROOT, "data", "satellite_imagery", "after_july2023.png")
    if os.path.exists(after_path):
        st.image(after_path, use_container_width=True)
    else:
        st.warning("After-image not found.")

st.markdown("---")

st.markdown(f"""
<div class="forensic-card">
    <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Acquisition Details</p>
    <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
        Both images cover an identical bounding box (32.0°E–33.6°E, 46.3°N–46.9°N), acquired via 
        Sentinel-2 L2A data with cloud-coverage filtering, using Sentinel Hub's Process API for 
        full reproducibility — the same programmatic acquisition pipeline used throughout this 
        project, rather than manual satellite-imagery browsing.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: Sentinel-2 L2A, Copernicus Data Space Ecosystem</p>",
    unsafe_allow_html=True,
)