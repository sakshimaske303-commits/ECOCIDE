import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../dashboard
ROOT_DIR = os.path.dirname(BASE_DIR)                                     # repo root
sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE

st.set_page_config(page_title="Fluvial Geomorphology — ECOCIDE", page_icon="🌊", layout="wide")
apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌊 ANATOMY OF A DAM-BREAK FLOOD</h1>", unsafe_allow_html=True)
st.markdown(
    f"<h3 style='text-align: center; color: {PALETTE['accent']}; font-weight: 400;'>"
    "The Fluvial Geomorphology and Coastal Oceanography Behind ECOCIDE's Evidence</h3>",
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
        st.image(IMG_PATH, use_container_width=True)
    else:
        st.warning("Diagram not found at outputs/plots/imgg1.png")
    st.markdown(
        f"<p style='text-align:center; color:{PALETTE['text_secondary']}; font-size:0.85rem; margin-top:6px;'>"
        "Schematic diagram — illustrative only</p>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div style="background: {PALETTE['bg_card']}; border: 1px solid rgba(0,172,193,0.3);
                    border-radius: 10px; padding: 14px 20px; margin-top: 6px;">
            <p style="color:{PALETTE['text_secondary']}; font-size:0.85rem; font-style:italic; margin:0; text-align:center;">
                Every process, label, and physical relationship shown here comes from my own
                understanding of fluvial and coastal process, laid out as a schematic to make the
                mechanism easier to follow alongside the statistical results.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ============================================================
# SECTION 1 — DAM-BREAK HYDRAULICS
# ============================================================
st.markdown("### A Reservoir Release Is a Geomorphic Event, Not Just a Hydrological One")

st.markdown("""
When the Kakhovka Dam failed on 6 June 2023, it did not simply "release water" — it released an
18.2 km³ reservoir as a **dam-break flood wave**, a discharge event orders of magnitude beyond the
Dnipro's normal flow, propagating downstream as a steep-fronted surge. The physics of how that
wave evolves as it travels is governed by unsteady open-channel flow (the shallow-water/Saint-Venant
equations, in essence a statement of mass and momentum conservation for a flood pulse moving down
a channel) — the wave attenuates and broadens as it travels, but even hundreds of kilometers
downstream it still arrives as a genuinely anomalous discharge spike, which is exactly what
UNOSAT's multi-date flood-extent polygons (used in ECOCIDE's Flood Analysis page) trace: a
rise–peak–recession cycle rather than a static flooded footprint.
""")

st.markdown("---")

# ============================================================
# SECTION 2 — GEOMORPHIC WORK OF THE FLOOD
# ============================================================
st.markdown("### The Flood as a Geomorphic Agent: Erosion, Transport, Deposition")

st.markdown("""
A flood of this magnitude does real **geomorphic work** on the landscape it passes through. Near
the breach, the discharge wave drives intense **bank erosion** and channel widening as flow
velocities and shear stress on the channel bed spike far above normal. That eroded material,
along with sediment already resting on the reservoir floor, becomes suspended load carried
downstream — the "sediment resuspension" stage in the diagram above. Where the flood spreads
beyond the main channel onto the floodplain, velocities drop and the river deposits that sediment
as new, often coarser-grained layers on top of the pre-existing floodplain surface: **floodplain
reworking**. This is the same category of process — just executed catastrophically over days
rather than gradually over centuries — through which rivers ordinarily build floodplains and
deltas in the first place.
""")

st.markdown("---")

# ============================================================
# SECTION 3 — WHERE RIVER MEETS SEA
# ============================================================
st.markdown("### Where the River Meets the Sea: A Buoyant Freshwater Plume")

st.markdown("""
The flood's final geomorphic stage is oceanographic rather than fluvial: at the Dnipro's mouth,
the surge of freshwater is significantly less dense than the surrounding Black Sea saltwater, so
it spreads out as a **buoyant surface plume** rather than mixing in immediately — the salinity
gradient depicted in the diagram, from low salinity at the river mouth to full marine salinity
offshore. This kind of density-stratified freshwater intrusion is a well-studied estuarine and
coastal-oceanography phenomenon, and it matters directly for ECOCIDE's own evidence: a large,
sudden freshwater and sediment pulse into a coastal wetland system is a plausible physical
mechanism for real vegetation stress — via osmotic disruption, turbidity-driven light reduction,
and sediment burial — independent of, and additional to, direct inundation. This gives the
project's causally-validated **NDVI decline (−0.0703, p = 0.022)** in the Kherson conflict zone a
concrete physical pathway, not just a statistical association.
""")

st.markdown("---")

st.markdown(
    f"<p class='caption-text' style='text-align:center;'>ECOCIDE — The Geomorphology and Oceanography Behind the Evidence</p>",
    unsafe_allow_html=True,
)
