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

# ============================================================
# PROOF-OF-WORK POPOVERS — tiny, pulsing "📸" buttons next to the
# exact data source / script they back up. Click to reveal the
# screenshot inline; nothing pushes the page layout around. Drop
# the PNGs into outputs/proof_screenshots/ (see filenames below)
# and these activate automatically — until then each falls back to
# a quiet "not added yet" note instead of breaking the page.
# ============================================================
st.markdown(f"""
<style>
    div[data-testid="stPopover"] button {{
        animation: proof-blink 1.8s ease-in-out infinite;
        border: 3px solid {PALETTE['accent']} !important;
        width: 32px !important;
        height: 32px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        min-height: unset !important;
        min-width: unset !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    div[data-testid="stPopover"] button p {{
        margin: 0 !important;
        font-size: 0.95rem !important;
        line-height: 1 !important;
    }}
    @keyframes proof-blink {{
        0%, 100% {{ box-shadow: 0 0 0px rgba(0, 172, 193, 0); }}
        50% {{ box-shadow: 0 0 12px rgba(0, 172, 193, 0.85); }}
    }}
</style>
""", unsafe_allow_html=True)

PROOF_DIR = os.path.join(PROJECT_ROOT, "outputs", "proof_screenshots")

def proof_popover(filename, caption):
    path = os.path.join(PROOF_DIR, filename)
    with st.popover("📸"):
        if os.path.exists(path):
            st.image(path, caption=caption, use_container_width=True)
        else:
            st.caption(f"Screenshot not added yet — save it as `outputs/proof_screenshots/{filename}`.")

st.markdown("### Data Sources")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    - **NDVI (Vegetation Index)** — Sentinel-2, Sentinel Hub Statistical API
    - **True-Color Imagery** — Sentinel-2 L2A, Sentinel Hub Process API
    - **Boundaries** — GADM v4.1
    """)
with col2:
    r1a, r1b = st.columns([0.88, 0.12])
    with r1a:
        st.markdown("- **Flood Extent** — UNOSAT (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS)")
    with r1b:
        proof_popover("01_kherson_flood_extent_qgis.png", "UNOSAT flood extent layers (ST1/ST3) for Kherson Oblast in QGIS, before/after Sentinel-2 imagery loaded alongside — the flood-extent product substituted in after cloud-contaminated optical NDWI detection failed.")
    st.markdown("- **Reservoir Data** — Documented public sources (pre-breach capacity)")

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

esa, esb = st.columns([0.94, 0.06])
with esa:
    with st.expander("**A Significant Pre-Event Quarter Revealed a Confounded Baseline**"):
        st.markdown("""
        The quarterly event study revealed a significant effect in a pre-treatment quarter (summer
        2022) — a genuine threat to the parallel-trends assumption. Investigation traced this to
        active conflict already underway in Kherson well before the dam's destruction (including the
        Kherson liberation operation, August–November 2022), meaning the original baseline period was
        not a genuinely quiet pre-conflict period.
        """)
with esb:
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    proof_popover("02_event_study_vscode.png", "event_study.py open in VS Code — the quarterly event study that revealed the significant pre-treatment quarter and the confounded 2022 baseline.")

pna, pnb = st.columns([0.94, 0.06])
with pna:
    with st.expander("**A Narrowed Baseline's Placebo Test Fails Under the Correct Standard Errors**"):
        st.markdown("""
        Narrowing the pre-period to exclude the confounded 2022 baseline produced a larger, more
        significant effect — but its own placebo test (a fake date within the narrow window) produced
        a coefficient nearly identical in magnitude to the real result. Under classical standard errors
        this looked merely ambiguous (p=0.169, not significant); under the methodologically correct
        Newey-West HAC standard errors — appropriate given serial correlation in this ten-observation
        window — that placebo coefficient is statistically significant (p=0.001). This is a genuine
        validation failure for the narrowed-baseline specification, disclosed as such rather than
        downplayed as merely underpowered.
        """)
with pnb:
    st.markdown("<div style='margin-top: 0.5rem;'></div>", unsafe_allow_html=True)
    proof_popover("03_placebo_narrowed_vscode.png", "placebo_narrowed.py open in VS Code — the placebo test that looked ambiguous under classical SEs (p=0.169) but fails under the correct Newey-West HAC SEs (p=0.001).")

with st.expander("**Standard Errors: Why HAC, Not Clustering**"):
    st.markdown("""
    The primary specification compares only two geographic units — one treatment zone (Kherson),
    one control zone (Tulcea) — observed monthly over time. Cluster-robust standard errors, the
    usual correction in panel designs with many independent units, are degenerate with only two
    clusters, so Newey-West HAC standard errors (Newey & West, 1987) are used instead, correcting
    for serial correlation within each zone's own time series. All models were re-estimated with
    HAC alongside classical OLS; the comparison is reported in full in ECO_Research_Paper.md.

    As a robustness check, the same causal model is also run against the full four-county control
    panel (Tulcea, Galați, Brăila, Constanța — see **Statistical Validation**), which has enough
    independent units (5 clusters) to support cluster-robust standard errors alongside HAC for the
    pooled DiD estimate — though barely, since 5 is the bare minimum at which cluster-robust
    inference is even defined. The quarterly event study on that same panel has too many parameters
    relative to its 5 clusters — cluster-robust becomes numerically rank-deficient there, so HAC is
    reported for that specific model instead, with the cluster-robust output kept only for the record.
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

era, erb = st.columns([0.94, 0.06])
with era:
    st.error("""
    **The narrowed-baseline DiD result (-0.1384) fails its own placebo test under HAC correction** —
    the methodologically correct standard errors, given serial correlation in this short window. It is
    retained here only to illustrate the pre-treatment-quarter problem, not as independent evidence.
    The broader-baseline result (-0.0703, HAC p=0.022, cleanly placebo-validated under HAC) is treated
    as the project's sole primary finding.
    """)
with erb:
    proof_popover("04_did_model_vscode.png", "did_model.py open in VS Code — the core difference-in-differences model that produces the project's primary finding (-0.0703, HAC p=0.022).")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — A Satellite-Based Evidentiary Framework</p>",
    unsafe_allow_html=True,
)