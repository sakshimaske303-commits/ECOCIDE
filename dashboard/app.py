import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE
from doc_viewer import render_doc_viewer

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

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(0, 172, 193, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; margin: 10px 0 18px 0;">
        <a href="https://doi.org/10.5281/zenodo.21757974" target="_blank" class="doi-badge-link" style="text-decoration:none;">
            <div class="doi-badge-card" style="
                display:flex; align-items:center; gap:18px;
                background: linear-gradient(145deg, {PALETTE['bg_card']}, {PALETTE['bg_main']});
                border: 2px solid {PALETTE['accent']};
                border-radius: 14px;
                padding: 16px 32px;
                box-shadow: 0 4px 20px rgba(0, 172, 193, 0.35);
            ">
                <div style="text-align:left;">
                    <div style="color:{PALETTE['accent']}; font-family:'Inter',sans-serif; font-weight:800; font-size:1.05rem; letter-spacing:0.4px; display:flex; align-items:center; gap:8px;">
                        <span>ARCHIVED &amp; CITABLE ON ZENODO</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_primary']}; font-family:'Inter',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        DOI: 10.5281/zenodo.21757974
                    </div>
                </div>
            </div>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("STUDY EVENT", "Kakhovka Dam", "6 June 2023")
with col2:
    st.metric("PEAK FLOOD", "464.18 km²", "9 June 2023")
with col3:
    st.metric("NDVI EFFECT", "-0.0703", "p = 0.022 (HAC)")
with col4:
    st.metric("VALIDATION", "Placebo-Tested", "Confirmed")

st.markdown("---")

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(0, 172, 193, 0.06);
                border: 1px solid rgba(0, 172, 193, 0.3); border-left: 4px solid {PALETTE['accent']};
                border-radius: 10px;">
        <p style="color:{PALETTE['accent']}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:800; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{PALETTE['text_primary']}; font-size:1rem; line-height:1.6; margin:0;">
            International courts have already accepted satellite evidence in war-crimes prosecutions —
            the ICC's <i>Al Mahdi</i> case was built on satellite imagery of cultural-heritage destruction
            — and legal bodies are now considering "ecocide" itself as a prosecutable international crime.
            But most satellite-based damage assessments of this specific event stop at visual, qualitative
            interpretation — they show <i>what</i> happened, not whether it is statistically distinguishable
            from a pre-existing trend. ECOCIDE closes that evidentiary gap: a causally-validated,
            placebo-tested estimate of conflict-attributable environmental damage, held to the same
            open-source-investigation discipline used by organizations like Bellingcat and Human Rights
            Watch — and honest enough to disclose exactly where its own validation didn't hold up.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
                A causally-validated <b>NDVI decline of 0.0703</b> (95% CI [-0.130, -0.010],
                HAC-robust p=0.022) was detected in the Kherson conflict zone relative to a
                matched non-conflict control zone (Danube Delta, Romania) — confirmed through a
                clean placebo test using a fake pre-event date, which showed no comparable effect
                (p=0.612).
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
        <p style="color: {PALETTE['water']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Flood Evidence</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Multi-sensor UNOSAT verified flood-extent polygons (ICEYE, Landsat-9, SkySat, 
            WorldView-3) tracked across 5 dates, revealing a complete rise-peak-recession cycle.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Causal Inference</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Difference-in-Differences model comparing Kherson (treatment) against a matched 
            non-conflict control zone, with month fixed effects and quarterly event-study validation.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['damage']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Honest Validation</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Every result stress-tested with placebo dates and sensitivity analysis. Ambiguous 
            findings are disclosed transparently, not selectively reported.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the Evidence")

nav_items = [
    ("Study Design", "Treatment/control zones, methodology"),
    ("Theoretical Foundations", "The flood physics and coastal oceanography behind the evidence"),
    ("Flood Analysis", "Hydrograph, verified flood extent"),
    ("Vegetation Impact", "NDVI causal analysis, DiD results"),
    ("Statistical Validation", "Placebo tests, event study, limitations"),
    ("Explore Trends", "Interactive NDVI time series, live difference calculator"),
    ("Satellite Evidence", "Before/after true-color imagery"),
    ("Interactive Maps & Plots", "Live geospatial exploration plus the three headline charts"),
    ("Methodology & Data", "Full transparency, data sources, honest limitations"),
]

cols = st.columns(3)
for i, (title, desc) in enumerate(nav_items):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="forensic-card" style="margin-bottom: 14px; min-height: 110px;">
            <p style="color: {PALETTE['text_primary']}; font-weight: 800; font-size: 0.95rem; margin: 0 0 4px 0;">{title}</p>
            <p style="color: {PALETTE['text_secondary']}; font-size: 0.8rem; margin: 0; font-weight: 600;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# FULL PROJECT DOCUMENTATION
# ============================================================
st.markdown(
    f"""
    <p style="text-align:center; color:{PALETTE['accent']}; text-transform:uppercase;
              letter-spacing:1.5px; font-weight:800; font-size:0.95rem; margin-bottom:14px;">
        Full Project Documentation
    </p>
    """,
    unsafe_allow_html=True,
)

_all_docs = [
    {"label": "Executive Summary", "filename": "ECO_Executive_Summary.pdf"},
    {"label": "Research Paper", "filename": "ECO_Research_Paper.pdf"},
    {"label": "Project Report", "filename": "ECO_Project_Report.pdf"},
    {"label": "Development Log", "filename": "ECO_Development_Log.pdf"},
]
_docs = [d for d in _all_docs if os.path.exists(os.path.join(BASE_DIR, "static", d["filename"]))]
_missing = [d for d in _all_docs if d not in _docs]

if _docs:
    render_doc_viewer(
        docs=_docs,
        colors={
            "navy_dark": PALETTE["bg_main"],
            "navy_med": PALETTE["bg_card"],
            "magenta": PALETTE["warning"],
            "teal": PALETTE["accent"],
            "text_light": PALETTE["text_primary"],
        },
    )
for d in _missing:
    st.warning(f"{d['filename']} not found.")

st.markdown("---")

st.markdown(
    f"""
    <div style="text-align: center; padding: 25px;" class="forensic-card">
        <p style="color: {PALETTE['text_secondary']}; text-transform: uppercase; letter-spacing: 2px; font-size: 0.8rem; font-weight: 700;">Developed by</p>
        <h2 style="color: {PALETTE['text_primary']}; margin: 5px 0;">SAKSHI D. MASKE</h2>
        <p style="color: {PALETTE['accent']}; font-weight: 700; margin-bottom: 18px;">Independent Geospatial Researcher</p>
        <a href="https://github.com/sakshimaske303-commits/ECOCIDE" target="_blank" style="display:inline-block; background-color:#2A2F36; border: 1px solid {PALETTE['accent']}; padding:12px 26px; border-radius:8px; text-decoration:none;">
            <span style="color:{PALETTE['text_primary']} !important; font-weight:700; font-size:1rem;">View Full Project on GitHub</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)