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
Sentinel-2 true-colour mosaics (B04/B03/B02) for the same bounding box before and after the
dam's destruction, acquired through the Sentinel Hub Process API. The frame covers the downstream
floodplain from the dam to the estuary and only the south-western tip of the former reservoir
(top right). These images give geographic context; they are not used as statistical evidence.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 12px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 900; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 1px;">BEFORE</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.9rem; font-weight: 600;">1 April – 31 May 2023 mosaic</p>
    </div>
    """, unsafe_allow_html=True)
    before_path = os.path.join(PROJECT_ROOT, "outputs", "maps", "before_may2023_final.png")
    if os.path.exists(before_path):
        st.image(before_path, width="stretch")
    else:
        st.warning("Before-image not found.")

with col2:
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 12px;">
        <p style="color: {PALETTE['damage']}; font-weight: 900; font-size: 1.3rem; text-transform: uppercase; letter-spacing: 1px;">AFTER</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.9rem; font-weight: 600;">1–31 July 2023 mosaic</p>
    </div>
    """, unsafe_allow_html=True)
    after_path = os.path.join(PROJECT_ROOT, "outputs", "maps", "after_july_2023_final.png")
    if os.path.exists(after_path):
        st.image(after_path, width="stretch")
    else:
        st.warning("After-image not found.")

st.markdown("---")

st.markdown(f"""
<div class="forensic-card">
    <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Acquisition Details</p>
    <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
        Bounding box 32.0°E–33.6°E, 46.3°N–46.9°N; Sentinel-2 L2A, least-cloud mosaicking
        (scene cloud cover ≤40% before, ≤20% after), Sentinel Hub Process API
        (<code>download_true_color_images.py</code>, <code>redownload_before.py</code>). Shown as the
        georeferenced QGIS layouts so the frame keeps its true shape. Scattered clouds remain in the
        July mosaic.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: Sentinel-2 L2A, Copernicus Data Space Ecosystem</p>",
    unsafe_allow_html=True,
)