import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌿 VEGETATION IMPACT</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Difference-in-Differences Causal Analysis</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
NDVI (vegetation index) was compared between Kherson (treatment) and Tulcea (control) using a 
Difference-in-Differences model with month fixed effects, isolating the conflict-attributable 
effect from seasonal cycles and baseline differences between zones.
""")

st.markdown("---")

st.markdown("### NDVI: Treatment vs. Control Over Time")

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "ndvi_comparison.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("NDVI comparison image not found.")

st.markdown("---")

st.markdown("### The Causal Result")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['damage']}; min-height: 200px;">
        <p style="color: {PALETTE['damage']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Primary Result</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 2rem; font-weight: 900; margin-bottom: 4px;">-0.0747</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin-bottom: 12px;">p = 0.060 (HAC) · R² = 0.703 · not significant at 5%</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.85rem; margin: 0;">
            A directionally consistent NDVI decline in Kherson relative to Tulcea following the
            conflict event, controlling for baseline differences and seasonality — but one that no
            longer clears the conventional significance threshold under this specification's own
            preferred (HAC) standard errors. See Statistical Validation for why.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['accent']}; min-height: 200px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Sensitivity Analysis</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 2rem; font-weight: 900; margin-bottom: 4px;">-0.1497</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin-bottom: 12px;">p = 0.0004 (HAC) · Narrowed baseline</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.85rem; margin: 0;">
            A larger effect emerges when excluding the confounded 2022 baseline period. Its own
            placebo test no longer fails under HAC correction (p=0.069, an improvement over an
            earlier version of this analysis), but the window is still short (n=10) and this stays
            a secondary, illustrative check rather than the primary result.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.info("""
This page shows the primary specification's result (Kherson vs. Tulcea). The same model also runs
as a robustness check across a four-county control panel — Tulcea, Galați, Brăila, Constanța —
with a similarly-weakened pooled effect at -0.0661 (HAC p=0.059), and two of the four controls
(Galați, Brăila) reproducing it individually. See **Statistical Validation** for the full
multi-control results, including why Kherson is no longer the most extreme unit under
randomization inference.
""")

st.markdown("---")

st.markdown("### Why the Model Needed Seasonal Controls")

st.markdown("""
An initial model without seasonal controls produced a weak, non-significant result (R²=0.054, 
p=0.117) — NDVI follows strong, well-documented seasonal cycles that, left uncontrolled, dominate 
residual variance and mask genuine treatment effects. Adding month fixed effects improved model
fit dramatically (R²=0.703) without changing the underlying coefficient — confirming the seasonal
confound was inflating uncertainty around a real effect, not creating a false one.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: Sentinel-2 (Copernicus Data Space Ecosystem)</p>",
    unsafe_allow_html=True,
)