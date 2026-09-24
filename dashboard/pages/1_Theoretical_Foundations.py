import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                                     # repo root
sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE

st.set_page_config(page_title="Theoretical Foundations — ECOCIDE", page_icon="🌊", layout="wide")
apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 ANATOMY OF A DAM-BREAK FLOOD</h1>", unsafe_allow_html=True)
st.markdown(
    f"<h3 style='text-align: center; color: {PALETTE['accent']}; font-weight: 400;'>"
    "How a Dam-Break Flood and Reservoir Drainage Can Change Vegetation</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# DIAGRAM
# ============================================================
IMG_PATH = os.path.join(ROOT_DIR, "outputs", "plots", "imgg1.png")
col_a, col_b, col_c = st.columns([0.2, 5.9, 0.2])
with col_b:
    if os.path.exists(IMG_PATH):
        st.image(IMG_PATH, width="stretch")
    else:
        st.warning("Diagram not found at outputs/plots/imgg1.png")
    st.markdown(
        f"<p style='text-align:center; color:{PALETTE['text_secondary']}; font-size:0.85rem; margin-top:6px;'>"
        "AI was used to help generate this image, but the concept and every detail in it are mine.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================
# SECTION 1 — DAM-BREAK HYDRAULICS
# ============================================================
st.markdown("### Two Opposite Processes Inside One Treatment Zone")

st.markdown("""
The dam's failure on 6 June 2023 set off two different landscape changes, and both fall inside the
Kherson Oblast polygon used for the NDVI analysis:

- **Downstream, the floodplain was inundated.** A dam-break wave travels as an unsteady flood pulse
  (described by the shallow-water / Saint-Venant equations). Along the roughly 90 km of the lower
  Dnipro between the dam and the Dnipro–Buh estuary, it covered land for days to weeks — UNOSAT mapped
  about 620 km² cumulatively over 6–9 June — then receded. Submergence, sediment deposition and
  debris can suppress vegetation in the flooded strip.
- **Upstream, the reservoir drained.** Several hundred square kilometres of former reservoir inside
  the oblast turned from open water into exposed bed that re-vegetated quickly. Water is masked in
  the NDVI series, so this bed enters the oblast mean as new, increasingly green land.
""")

st.markdown("---")

st.markdown("### Why This Matters for the Statistics")

st.markdown("""
The flood covered only about 2% of the oblast. Even a complete loss of vegetation on every flooded
pixel would move the oblast-wide mean NDVI by roughly 0.02, while reservoir drainage pushes the mean
in the opposite direction by adding newly vegetated land. A mechanism that could produce an oblast-wide decline would have to act
far beyond the flooded strip — for example through the loss of irrigation water from the reservoir,
or through conflict effects unrelated to the dam. The NDVI analysis cannot separate these pathways,
which is why its statistically significant oblast-wide decline is reported as an association, not
as a measured flood impact. The decline is largest in the 2024 growing season, which fits slower,
larger-scale pathways better than the flood itself.
""")

st.markdown("---")

st.markdown("### At the River Mouth")

st.markdown("""
Where the Dnipro enters the estuary and the Black Sea, the flood released a large pulse of fresh
water, sediment and pollutants that spread as a buoyant surface plume. Fresh water is not itself an
osmotic stressor for floodplain plants; the documented concerns are for the brackish estuarine and
marine ecosystems (salinity drop, turbidity, contamination), which NDVI over land does not measure.
""")

st.markdown("---")

st.markdown(
    f"<p class='caption-text' style='text-align:center;'>ECOCIDE — Physical context for the evidence</p>",
    unsafe_allow_html=True,
)
