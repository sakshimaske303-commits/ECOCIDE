import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                                     # repo root
sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE

st.set_page_config(page_title="Theoretical Foundations — ECOCIDE", page_icon="🌊", layout="wide")
apply_custom_style()

st.markdown("<h1 style='text-align: center;'>ANATOMY OF A DAM-BREAK FLOOD</h1>", unsafe_allow_html=True)
st.markdown(
    f"<h3 style='text-align: center; color: {PALETTE['accent']}; font-weight: 400;'>"
    "Three Ways the Dam's Destruction Could Change Vegetation</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ============================================================
# SECTION 1 — DAM-BREAK HYDRAULICS
# ============================================================
st.markdown("### Three Pathways, With Opposite Effects")

st.markdown("""
The dam's failure on 6 June 2023 set off three different landscape changes inside an active war zone:

- **Downstream, the floodplain was inundated.** A dam-break wave travels as an unsteady flood pulse
  (described by the shallow-water / Saint-Venant equations). Along the roughly 90 km of the lower
  Dnipro between the dam and the Dnipro–Buh estuary, it covered land for days to weeks — UNOSAT mapped
  about 620 km² cumulatively over 6–9 June — then receded. Submergence, sediment deposition and
  debris can suppress vegetation in the flooded strip.
- **Upstream, the reservoir drained.** Several hundred square kilometres of former reservoir inside
  the oblast turned from open water into exposed bed that re-vegetated quickly. Water is masked in
  the NDVI series, so this bed enters the oblast mean as new, increasingly green land.
- **The irrigation canals lost their water source.** The reservoir fed the canals that irrigated much of the
  southern steppe. Without them, summer crops that depended on irrigation could no longer be grown in the same way.
""")

st.markdown("---")

st.markdown("### Why This Matters for the Statistics")

st.markdown("""
The flood covered only about 2% of Kherson Oblast. Even a complete loss of vegetation on every flooded
pixel would move the oblast-wide mean NDVI by roughly 0.02, while reservoir drainage pushes the mean
in the opposite direction by adding newly vegetated land. An oblast-wide average (Study 1) therefore mixes
the three pathways with each other and with the war's other effects, and cannot say which one caused a change.

This is why Study 2 defines each pathway by its physical footprint — the flooded land, the drained bed and the
cropland near the canals — and compares each with similar land in the same war zone. See the **Study 2** pages.
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
