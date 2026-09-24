import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(BASE_DIR)
from styles import apply_custom_style, PALETTE
from doc_viewer import render_doc_viewer
from results import R, FLOOD, p, c, ci, sig

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
    "Satellite Evidence and Causal-Inference Testing of the Kakhovka Dam Destruction</h3>",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <style>
        .doi-badge-link {{ text-decoration:none; }}
        .doi-badge-card {{ transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease; cursor: pointer; }}
        .doi-badge-link:hover .doi-badge-card {{ transform: translateY(-3px) scale(1.02); box-shadow: 0 10px 32px rgba(0, 172, 193, 0.6); filter: brightness(1.08); }}
    </style>
    <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:16px; margin: 10px 0 18px 0;">
        <a href="https://eartharxiv.org/repository/view/14827/" target="_blank" class="doi-badge-link" style="text-decoration:none;">
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
                        <span>PREPRINT v1 ON EARTHARXIV</span>
                        <span style="opacity:0.8; font-size:0.95rem;">↗</span>
                    </div>
                    <div style="color:{PALETTE['text_primary']}; font-family:'Inter',sans-serif; font-weight:900; font-size:1.35rem; margin-top:2px;">
                        v1 — superseded results
                    </div>
                </div>
            </div>
        </a>
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
    st.metric("UNOSAT FLOOD (6–9 JUNE)", f"{FLOOD['composite_6_9_june']['flood_km2']:.0f} km²", "cumulative, multi-sensor")
with col3:
    st.metric("NDVI DiD (vs TULCEA)", c(R["main_did"]), f"HAC p = {p(R['main_did']['p'])} — {sig(R['main_did']['p'])}")
with col4:
    st.metric("PLACEBO IN SPACE", f"Rank {R['placebo_in_space']['rank_one_sided']} of 5", f"exact p = {R['placebo_in_space']['p_one_sided']:.2f}")

st.markdown("---")

st.markdown(
    f"""
    <div style="padding: 20px 26px; margin: 4px 0 20px 0; background: rgba(0, 172, 193, 0.06);
                border: 1px solid rgba(0, 172, 193, 0.3); border-left: 4px solid {PALETTE['accent']};
                border-radius: 10px;">
        <p style="color:{PALETTE['accent']}; text-transform:uppercase; letter-spacing:1.5px;
                  font-weight:800; font-size:0.85rem; margin-bottom:8px;">Why This Matters</p>
        <p style="color:{PALETTE['text_primary']}; font-size:1rem; line-height:1.6; margin:0;">
            Satellite imagery is already used in international criminal proceedings as supporting
            evidence (for example, UNOSAT imagery in the ICC's <i>Al Mahdi</i> case on the destruction of
            cultural heritage in Timbuktu), and a standalone crime of "ecocide" has been <i>proposed</i> as an
            amendment to the Rome Statute (Vanuatu, Fiji and Samoa, September 2024). Most satellite assessments
            of the Kakhovka Dam destruction describe what changed; this project asks a narrower question:
            is the post-event vegetation change in Kherson statistically distinguishable from change in
            comparable, unaffected regions — and can it be attributed to the dam? The first answer is yes;
            the second, with this design, is no. The pages below show why.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.1, 1])

with col_left:
    st.markdown("""
    ### What Is ECOCIDE?

    On **6 June 2023**, the Kakhovka Dam on Ukraine's Dnipro River was destroyed, draining a
    reservoir of about 18.2 km³ and flooding the downstream floodplain (UNOSAT mapped roughly
    620 km² cumulatively over 6–9 June). A standalone international crime of "ecocide" has been
    proposed but does not yet exist in the Rome Statute.

    This project applies a **Difference-in-Differences** design to monthly Sentinel-2 NDVI,
    comparing Kherson Oblast with four Romanian counties, and stress-tests the result with
    placebo tests, an event study, randomization inference and a control-only divergence check.
    Every number on this dashboard is read from one results file produced by the repository's code.
    """)

with col_right:
    st.markdown(
        f"""
        <div class="forensic-card">
            <p style="color:{PALETTE['accent']}; text-transform:uppercase; font-size:0.78rem;
                      letter-spacing:1.5px; font-weight:800; margin-bottom:12px;">Core Finding</p>
            <p style="color:{PALETTE['text_primary']}; font-size:0.95rem; line-height:1.7; margin:0; font-weight:500;">
                After June 2023 Kherson's NDVI fell relative to Tulcea by {c(R["main_did"])}
                (95% CI {ci(R["main_did"])}, HAC p = {p(R["main_did"]["p"])}); allowing each zone its own
                seasonal cycle gives {c(R["main_did_seasonal"])} (p = {p(R["main_did_seasonal"]["p"])}), and a
                placebo date a year earlier shows nothing. But attribution to the dam is not established:
                in an exact randomization check Kherson ranks {R["placebo_in_space"]["rank_one_sided"]} of 5
                (p = {R["placebo_in_space"]["p_one_sided"]:.2f}) because Constanța shifts by as much, pre-event
                quarters already deviate, and the oblast-wide unit mixes flooding, reservoir drainage and war effects.
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
            UNOSAT flood-extent layers (Sentinel-3, ICEYE, Sentinel-2, Sentinel-1) for 6–21 June 2023 —
            preliminary products, each with its own sensor and analysis extent.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Causal Inference</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Difference-in-Differences on the monthly Kherson-minus-control NDVI gap, Newey-West HAC
            standard errors, placebo tests, event study and randomization inference.
        </p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="forensic-card" style="min-height: 190px;">
        <p style="color: {PALETTE['damage']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Honest Validation</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.88rem; margin: 0;">
            Every check is reported with its actual result, including the ones that weaken the
            headline — they are listed on the Statistical Validation page.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Explore the Evidence")

nav_items = [
    ("Study Design", "Treatment/control zones, methodology"),
    ("Theoretical Foundations", "How a dam-break flood and reservoir drainage could affect vegetation"),
    ("Flood Analysis", "UNOSAT flood-extent layers by sensor"),
    ("Vegetation Impact", "NDVI causal analysis, DiD results"),
    ("Statistical Validation", "Placebo tests, event study, limitations"),
    ("Explore Trends", "Interactive NDVI time series, live difference calculator"),
    ("Satellite Evidence", "Before/after true-color imagery"),
    ("Interactive Maps & Plots", "Flood map plus three interactive charts"),
    ("Methodology & Data", "Data sources, corrections, limitations"),
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