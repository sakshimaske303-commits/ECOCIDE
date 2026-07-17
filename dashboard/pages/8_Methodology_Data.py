import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📖 METHODOLOGY & DATA</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Full Transparency and Reproducibility</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("### Data Sources")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **NDVI (Vegetation Index)** — Sentinel-2, Sentinel Hub Statistical API
    - **True-Color Imagery** — Sentinel-2 L2A, Sentinel Hub Process API
    - **Boundaries** — GADM v4.1
    """)
with col2:
    st.markdown("""
    - **Flood Extent** — UNOSAT (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS)
    - **Reservoir Data** — Documented public sources (pre-breach capacity)
    """)

st.markdown("---")

st.markdown("### The Validation Journey")

with st.expander("**Full Baseline Overrepresented Seasonality — R² Jumped from 0.05 to 0.75**"):
    st.markdown("""
    The initial DiD model without seasonal controls explained only 5% of NDVI variance, since 
    monthly NDVI naturally cycles with seasons regardless of any treatment effect. Adding month 
    fixed effects improved model fit to 75% without changing the underlying coefficient — 
    confirming the seasonal confound was inflating uncertainty, not creating a false effect.
    """)

with st.expander("**Monthly Event Study Failed — Model Was Rank-Deficient**"):
    st.markdown("""
    An attempt at monthly-resolution event-study validation, matching prior work's approach, 
    failed technically: with only 70 observations and roughly 68 required parameters, the model 
    could not estimate standard errors (all returned as NaN). The fix was reducing to quarterly 
    bins, which preserved the event-study logic while keeping the model estimable.
    """)

with st.expander("**A Significant Pre-Event Quarter Revealed a Confounded Baseline**"):
    st.markdown("""
    The quarterly event study revealed a significant effect in a pre-treatment quarter (summer 
    2022) — a genuine threat to the parallel-trends assumption. Investigation traced this to 
    active conflict already underway in Kherson well before the dam's destruction (including the 
    Kherson liberation operation, August–November 2022), meaning the original baseline period was 
    not a genuinely quiet pre-conflict period.
    """)

with st.expander("**A Narrowed Baseline's Placebo Test Was Ambiguous, Not Clean**"):
    st.markdown("""
    Narrowing the pre-period to exclude the confounded 2022 baseline produced a larger, more 
    significant effect — but its own placebo test (a fake date within the narrow window) produced 
    a coefficient nearly identical in magnitude to the real result, though not statistically 
    significant, due to low statistical power from only 10 observations. This is disclosed as an 
    unresolved limitation rather than treated as confirmatory.
    """)

with st.expander("**Downstream Flood Signal Was Lost to Cloud-Contaminated Optical Data**"):
    st.markdown("""
    Independent NDWI-based flood detection from Sentinel-2 optical imagery produced erratic, 
    physically implausible week-to-week swings, traced to cloud-contaminated composite pixels 
    changing which parts of the scene were sampled each week. This was resolved by substituting 
    UNOSAT's verified, multi-sensor, radar-inclusive flood-extent product for the specific 
    event dates — the same category of solution already used in existing published literature 
    on this event.
    """)

st.markdown("---")

st.markdown("### Honest Limitations")

st.warning("""
**Reservoir water-loss could not be tested causally** — no comparable control-zone equivalent 
exists for a large upstream reservoir collapse, so this is reported descriptively alongside the 
statistically validated NDVI findings, not as an independently causally-tested result.
""")

st.error("""
**The narrowed-baseline DiD result (-0.1384) carries an unresolved validation limitation** — its 
placebo test could not cleanly distinguish a genuine effect from statistical noise due to limited 
sample size. The broader-baseline result (-0.0703, cleanly placebo-validated) is treated as the 
project's primary finding.
""")

st.markdown("---")

st.markdown(f"""
<div class="forensic-card" style="margin-bottom: 16px;">
    <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 8px;">GitHub Repository</p>
    <p style="color: {PALETTE['text_primary']}; font-size: 0.9rem; margin: 0;">
        <a href="https://github.com/sakshimaske303-commits/ECOCIDE" target="_blank" style="color: {PALETTE['accent']};">github.com/sakshimaske303-commits/ECOCIDE</a>
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="forensic-card" style="text-align: center; padding: 25px;">
    <p style="color: {PALETTE['text_secondary']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 700;">Project Author</p>
    <h2 style="color: {PALETTE['text_primary']}; margin: 5px 0;">SAKSHI D. MASKE</h2>
    <p style="color: {PALETTE['accent']}; font-weight: 700;">Independent Geospatial Researcher</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — A Satellite-Based Evidentiary Framework</p>",
    unsafe_allow_html=True,
)