import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from styles import apply_custom_style, PALETTE

st.set_page_config(
    page_title="ECOCIDE",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🛰️ ECOCIDE</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700; margin-top: -10px;'>"
    "A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes</h3>",
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("STUDY EVENT", "Kakhovka Dam", "6 June 2023")
with col2:
    st.metric("PEAK FLOOD", "464.18 km²", "9 June 2023")
with col3:
    st.metric("NDVI EFFECT", "-0.0703", "p = 0.007")
with col4:
    st.metric("VALIDATION", "Placebo-Tested", "Confirmed")

st.markdown("---")

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is ECOCIDE?

    On **6 June 2023**, the Kakhovka Dam on Ukraine's Dnipro River was destroyed, draining an 
    18.2 km³ reservoir and flooding hundreds of square kilometers of downstream floodplain. 
    International legal bodies have begun formally considering "ecocide" — mass environmental 
    destruction — as a prosecutable international crime.

    Existing satellite assessments of this event rely on **visual, qualitative interpretation** 
    and explicitly decline to establish statistical causality. This project fills that gap: 
    applying a rigorous **Difference-in-Differences causal-inference framework**, validated 
    through placebo testing, to independently quantify conflict-attributable environmental 
    damage — separating it from pre-existing trends with statistical confidence.
    """)

with col_right:
    st.markdown(
        f"""
        <div class="forensic-card">
            <p style="color:{PALETTE['accent']}; text-transform:uppercase; font-size:0.78rem;
                      letter-spacing:1.5px; font-weight:800; margin-bottom:12px;">Core Finding</p>
            <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0; font-weight:500;">
                A causally-validated <b>NDVI decline of 0.0703</b> (p=0.007) was detected in the 
                Kherson conflict zone relative to a matched non-conflict control zone (Danube 
                Delta, Romania) — confirmed through a clean placebo test using a fake pre-event 
                date, which showed no comparable effect (p=0.741).
            </p>
        </div>
        """, unsafe_allow_html=True
    )

st.markdown("---")

st.markdown("### Methodology at a Glance")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['water']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">🌊 Flood Evidence</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Multi-sensor UNOSAT verified flood-extent polygons (ICEYE, Landsat-9, SkySat, 
            WorldView-3) tracked across 5 dates, revealing a complete rise-peak-recession cycle.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">🌿 Causal Inference</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Difference-in-Differences model comparing Kherson (treatment) against a matched 
            non-conflict control zone, with month fixed effects and quarterly event-study validation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['damage']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">🔥 Honest Validation</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Every result stress-tested with placebo dates and sensitivity analysis. Ambiguous 
            findings are disclosed transparently, not selectively reported.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the Evidence")

nav_items = [
    ("🏛️", "Study Design", "Treatment/control zones, methodology"),
    ("🌊", "Flood Analysis", "Hydrograph, verified flood extent"),
    ("🌿", "Vegetation Impact", "NDVI causal analysis, DiD results"),
    ("📊", "Statistical Validation", "Placebo tests, event study, limitations"),
    ("🛰️", "Satellite Evidence", "Before/after true-color imagery"),
    ("🗺️", "Interactive Maps", "Live geospatial exploration"),
]

cols = st.columns(3)
for i, (icon, title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="forensic-card" style="margin-bottom: 14px; min-height: 110px;">
            <p style="font-size: 1.6rem; margin: 0 0 6px 0;">{icon}</p>
            <p style="color: {PALETTE['text_primary']}; font-weight: 800; font-size: 0.95rem; margin: 0 0 4px 0;">{title}</p>
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.8rem; margin: 0; font-weight: 600;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px;" class="forensic-card">
        <p style="color: {PALETTE['text_secondary']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 700;">Developed by</p>
        <h2 style="color: {PALETTE['text_primary']}; margin: 5px 0;">SAKSHI D. MASKE</h2>
        <p style="color: {PALETTE['accent']}; font-weight: 700;">Independent Geospatial Researcher</p>
    </div>
    """,
    unsafe_allow_html=True,
)