import streamlit as st
import streamlit.components.v1 as components
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
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

After the destruction of the Kakhovka Dam, did vegetation greenness (NDVI) in Kherson Oblast change
more than in comparable, unaffected regions over the same period — and can that difference be
statistically distinguished from ordinary variation among those regions?
""")

st.markdown("---")

st.markdown("### The Primary Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['damage']}; min-height: 240px;">
        <p style="color: {PALETTE['damage']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Treatment Zone</p>
        <h3 style="color: {PALETTE['text_primary']}; margin-bottom: 8px;">Kherson Oblast, Ukraine</h3>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.88rem; margin-bottom: 12px;">
            46.777°N, 33.370°E — Kakhovka Dam and Dnipro River floodplain
        </p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Dam destroyed <b>6 June 2023</b>. The NDVI analysis uses the whole oblast polygon
            (GADM, ≈25,500 km²); the mapped flood covered roughly 620 km² at most, and part of the
            drained reservoir also lies inside the oblast. Active conflict since February 2022.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['vegetation']}; min-height: 240px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Primary Control Zone</p>
        <h3 style="color: {PALETTE['text_primary']}; margin-bottom: 8px;">Tulcea County, Romania</h3>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.88rem; margin-bottom: 12px;">
            45.200°N, 29.500°E — Danube Delta
        </p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Chosen by hand for broadly similar landscape — river-delta wetland, steppe,
            agricultural floodplain, continental climate — outside the war zone. No formal matching
            was performed; Tulcea borders Ukraine's Odesa Oblast along the Danube.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.info("""
The primary specification compares Kherson against Tulcea. Three more Romanian counties along the
same Danube/Black Sea corridor — **Galați, Brăila, and Constanța** — form a four-county control
panel used as a robustness check, testing whether the result depends on the specific choice of a
single control. See **Statistical Validation** for what came back.
""")

st.markdown("---")

st.markdown("### Study Area Overview")
interactive_map_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "study_area_overview.html")
if os.path.exists(interactive_map_path):
    with open(interactive_map_path, "r", encoding="utf-8") as f:
        components.html(f.read(), height=560)
    st.markdown(
        "<p class='caption-text' style='text-align:center;'>Hover a zone for its name and role. Toggle layers top-right.</p>",
        unsafe_allow_html=True,
    )
else:
    image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "study_area_overview.png")
    if os.path.exists(image_path):
        st.image(image_path, width="stretch")
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
similar river-delta landscape — was selected instead.
""")

st.markdown("---")

st.markdown("### Methodology at a Glance")

st.markdown("""
1. **Boundary Acquisition** — Administrative boundaries for both zones sourced from GADM v4.1.

2. **Monthly NDVI** — Sentinel-2 L2A, Sentinel Hub Statistical API, each zone's GADM polygon,
   pixel-level cloud/shadow/cirrus/snow masking, January 2022 – November 2024.

3. **Flood Extent** — UNOSAT FL20230606UKR layers (Sentinel-3, ICEYE, Sentinel-2, Sentinel-1),
   6–21 June 2023; preliminary products, reported descriptively.

4. **Difference-in-Differences** — the monthly Kherson-minus-control NDVI gap before vs after
   June 2023, Newey-West HAC standard errors; a second version allows zone-specific seasonality.

5. **Placebo Tests** — fake treatment dates (June 2022; March 2023 in the narrowed window).

6. **Quarterly Event Study** — the gap quarter by quarter, with multiple-testing correction.

7. **Four-County Panel, Placebo in Space, Control-Only Divergence** — whether the result depends on
   the control chosen, and whether Kherson stands out from the controls themselves.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Kakhovka Dam study</p>",
    unsafe_allow_html=True,
)