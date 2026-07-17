import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🏛️ STUDY DESIGN</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Treatment Zone, Control Zone, and Causal Framework</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
### The Research Question

Does the destruction of the Kakhovka Dam produce a statistically significant, quantifiable 
increase in environmental degradation beyond what a comparable non-conflict region would have 
experienced over the same period — isolated from pre-existing conflict trends and seasonal 
vegetation cycles?
""")

st.markdown("---")

st.markdown("### The Two Zones")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['damage']}; min-height: 240px;">
        <p style="color: {PALETTE['damage']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">🎯 Treatment Zone</p>
        <h3 style="color: {PALETTE['text_primary']}; margin-bottom: 8px;">Kherson Oblast, Ukraine</h3>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.88rem; margin-bottom: 12px;">
            46.777°N, 33.370°E — Kakhovka Dam and Dnipro River floodplain
        </p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Dam destroyed <b>6 June 2023</b>. Flood-affected analysis zone spans approximately 
            10,800 km² (dam to river mouth, per UNOSAT). Region under active conflict since 
            February 2022.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['vegetation']}; min-height: 240px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">✅ Control Zone</p>
        <h3 style="color: {PALETTE['text_primary']}; margin-bottom: 8px;">Tulcea County, Romania</h3>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.88rem; margin-bottom: 12px;">
            45.200°N, 29.500°E — Danube Delta
        </p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Selected for a comparable pre-conflict ecological baseline — river-delta wetland, 
            steppe, agricultural floodplain, similar continental climate — while being genuinely 
            <b>non-combatant</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Study Area Overview")
image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "study_area_overview.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Study area overview image not found.")

st.markdown("---")

st.markdown("### Why This Control Zone")

st.info("""
A within-Ukraine non-frontline control zone (e.g., Dnipropetrovsk Oblast) was initially considered, 
but rejected — the frontline has moved closer to this region over time, and war-adjacent economic 
and demographic effects (supply disruption, displacement) could contaminate a control zone even 
without direct conflict in that specific area. The Ukrainian side of the Danube Delta itself 
(Odesa Oblast) was also ruled out, since it has been affected by war-related strikes on Danube 
port infrastructure. Tulcea County, Romania — a genuinely non-combatant NATO/EU member with a 
matching river-delta ecology — was selected instead.
""")

st.markdown("---")

st.markdown("### Methodology at a Glance")

st.markdown("""
1. **Boundary Acquisition** — Administrative boundaries for both zones sourced from GADM v4.1.

2. **Multi-Temporal NDVI** — Monthly vegetation index data (Sentinel-2) acquired for both zones, 
   spanning January 2022 through November 2024.

3. **Verified Flood Extent** — UNOSAT multi-sensor flood-extent polygons (ICEYE, Landsat-9, 
   SkySat, WorldView-3, MODIS) across 5 dates in June 2023.

4. **Difference-in-Differences Model** — Statistical comparison of treatment-zone versus 
   control-zone NDVI change, with month fixed effects to control for seasonal cycles.

5. **Placebo Validation** — Fake treatment dates tested to confirm the real effect is genuine, 
   not a general pre-existing trend.

6. **Quarterly Event Study** — Testing whether the effect is genuinely concentrated around the 
   June 2023 event, disclosed transparently including any limitations found.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — A Satellite-Based Evidentiary Framework</p>",
    unsafe_allow_html=True,
)