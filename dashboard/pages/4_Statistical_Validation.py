import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📊 STATISTICAL VALIDATION</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Placebo Tests, Event Study, and Honest Limitations</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
Every result in this project was stress-tested rather than accepted at face value. This page 
documents both the validation that succeeded and the validation that revealed genuine limitations 
— reported transparently rather than selectively.
""")

_checks = [
    ("✓", PALETTE['vegetation'], "Matched Non-Conflict Control Zone (Tulcea, Romania)"),
    ("✓", PALETTE['vegetation'], "HAC-Robust Standard Errors (Newey-West)"),
    ("✓", PALETTE['vegetation'], "Placebo Test #1 — Clean Pass (broad baseline)"),
    ("!", PALETTE['warning'], "Placebo Test #2 — Genuine Failure Disclosed (narrowed baseline)"),
    ("✓", PALETTE['vegetation'], "Quarterly Event-Study Check"),
    ("✓", PALETTE['vegetation'], "Month Fixed Effects (seasonal controls)"),
    ("✓", PALETTE['vegetation'], "Multi-Sensor Verified Flood Data (UNOSAT, 5 sensors)"),
    ("!", PALETTE['warning'], "Multi-Control Robustness Check (4-control panel, 3 of 4 reproduce it)"),
]
_badges = "".join(
    f"""<span style="display:inline-flex; align-items:center; gap:6px; background:rgba(0,172,193,0.08);
        border:1px solid rgba(0,172,193,0.3); border-radius:20px; padding:6px 14px; margin:4px;
        font-size:0.82rem; color:{PALETTE['text_primary']}; font-weight:600;">
        <span style="color:{color}; font-weight:900;">{mark}</span>{label}</span>"""
    for mark, color, label in _checks
)
st.markdown(
    f"""
    <p style="color:{PALETTE['accent']}; text-transform:uppercase; letter-spacing:1.5px;
              font-weight:800; font-size:0.85rem; margin-bottom:6px;">Robustness At a Glance</p>
    <div style="display:flex; flex-wrap:wrap; margin-bottom: 6px;">{_badges}</div>
    <p style="color:{PALETTE['text_secondary']}; font-size:0.78rem; margin-top:8px;">
        One check is flagged, not hidden — see Placebo Test #2 below for exactly what failed and why.
    </p>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown("### Placebo Test #1 — Full Baseline (Clean Validation)")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['vegetation']}; min-height: 160px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Real Treatment Date (June 2023)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.0703</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.022 (HAC) — Significant</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['text_secondary']}; min-height: 160px;">
        <p style="color: {PALETTE['text_secondary']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Fake Treatment Date (June 2022)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">+0.0148</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.612 (HAC) — Not significant</p>
    </div>
    """, unsafe_allow_html=True)

st.success("""
**Clean validation.** A near-zero coefficient AND a high p-value together confirm the real result
reflects a genuine event-specific effect, not a general pre-existing trend in Kherson. This holds
under both classical and Newey-West HAC standard errors.
""")

st.markdown("---")

st.markdown("### Event Study — Quarterly Treatment Effects")

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "event_study.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Event study image not found.")

st.warning("""
**A genuine limitation, disclosed honestly:** While quarters immediately following the event
(Quarter 0: HAC p=0.005; Quarter +1: HAC p=0.023; Quarter +4: HAC p<0.0001) showed significant
negative effects, one pre-event quarter (Quarter -4, summer 2022) also showed a significant effect
(HAC p<0.001) — inconsistent with a fully clean parallel-trends assumption. Investigation traced
this to Kherson already being an active conflict zone in 2022 (including the Kherson liberation
operation), meaning the original baseline period was not a genuinely quiet pre-conflict period.
""")

st.markdown("---")

st.markdown("### Placebo Test #2 — Narrowed Baseline (Fails Under HAC)")

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['accent']}; min-height: 160px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Real Date, Narrowed Baseline</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.1384</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.0001 (HAC)</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 160px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Fake Date, Same Narrow Window</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.1382</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">Classical p = 0.169 · HAC p = 0.001 (n=10)</p>
    </div>
    """, unsafe_allow_html=True)

st.error("""
**Reported honestly as a validation failure, not merely ambiguous.** Under classical standard
errors this placebo's p-value looked non-significant (p=0.169), which read as ambiguous — the
fake-date coefficient was nearly identical in magnitude to the real result, a meaningfully weaker
form of validation than a near-zero placebo coefficient, but not a clean failure. Under the
methodologically correct Newey-West HAC standard errors — the appropriate correction for this
serially correlated, ten-observation window — that same placebo coefficient becomes statistically
significant (p=0.001). That is a genuine validation failure: this narrowed-baseline specification
does not survive proper robustness testing. It is retained on this dashboard only to illustrate
the pre-treatment-quarter problem it was built to investigate, not as independent evidence. The
broader-baseline result (-0.0703, HAC p=0.022), whose own placebo test remains clean under HAC, is
the project's sole primary finding.
""")

st.markdown("---")

st.markdown("### Robustness Summary — All Four Models, Both Standard-Error Specifications")

robustness_image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "robustness_check.png")
if os.path.exists(robustness_image_path):
    st.image(robustness_image_path, use_container_width=True)
else:
    st.warning("Robustness check image not found.")

st.markdown("""
Every model in this project is shown here twice — once under classical OLS standard errors, once
under Newey-West HAC. The main and narrowed-baseline DiD estimates stay clearly bounded away from
zero either way. The broad-baseline placebo interval straddles zero under both specifications
(clean validation). The narrowed-baseline placebo interval straddles zero classically but excludes
zero under HAC — the visual signature of the validation failure discussed above.
""")

st.markdown("---")

st.markdown("### Multi-Control Robustness Check — Testing Against a Four-County Panel")

czi_image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "control_panel_comparison.png")
if os.path.exists(czi_image_path):
    st.image(czi_image_path, use_container_width=True)
else:
    st.warning("Control panel comparison image not found.")

st.markdown("""
The single treatment-control-pair design above carries a known limitation — with only Tulcea as a
control, cluster-robust inference is undefined and Newey-West HAC has to carry the whole burden of
correcting for serial correlation. As a robustness check, the same causal model is also run against
a four-county Romanian panel along the same Danube/Black Sea corridor (Tulcea, Galați, Brăila,
Constanța) to test that limitation directly.
""")

col5, col6 = st.columns(2)
with col5:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['vegetation']}; min-height: 160px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Pooled: All 4 Controls (HAC)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.0600</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.029 (HAC) · p = 0.002 (cluster-robust) — holds</p>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 160px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Per-Control Check</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">3 of 4</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">Tulcea, Galați, Brăila confirm — Constanța does not</p>
    </div>
    """, unsafe_allow_html=True)

st.warning("""
**Two honest complications, disclosed rather than smoothed over.** First, Constanța — the most
purely Black Sea coastal, most urbanized of the four control counties — does not reproduce the
effect (coefficient -0.0064, p = 0.808), while Tulcea, Galați, and Brăila each do individually. A
land-cover difference is a plausible explanation but not a confirmed one; it is left as an open
question rather than asserted as fact. Second, cluster-robust inference at only 5 clusters (one
treatment, four control) is thinner than the 30-40+ clusters standard guidance wants — on the
pooled DiD model this is a real but survivable caveat, but extending the same panel to a quarterly
event study pushes it past the point of being usable at all: several coefficients come back with
numerically degenerate standard errors (~1e-16), an artifact of too many parameters for too few
clusters. HAC is reported for that model instead, and shows the exact treatment-quarter effect no
longer significant (p = 0.972) when pooled across four heterogeneous controls, while the
one-year-later effect still is (p = 0.011).
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Every result stress-tested, every limitation disclosed</p>",
    unsafe_allow_html=True,
)