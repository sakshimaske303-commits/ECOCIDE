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

st.markdown("---")

st.markdown("### Placebo Test #1 — Full Baseline (Clean Validation)")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['vegetation']}; min-height: 160px;">
        <p style="color: {PALETTE['vegetation']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Real Treatment Date (June 2023)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.0703</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.007 — Highly significant</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['text_secondary']}; min-height: 160px;">
        <p style="color: {PALETTE['text_secondary']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Fake Treatment Date (June 2022)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">+0.0148</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.741 — Not significant</p>
    </div>
    """, unsafe_allow_html=True)

st.success("""
**Clean validation.** A near-zero coefficient AND a high p-value together confirm the real result 
reflects a genuine event-specific effect, not a general pre-existing trend in Kherson.
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
(Quarter 0: p=0.035; Quarter +4: p=0.0001) showed significant negative effects, one pre-event 
quarter (Quarter -4, summer 2022) also showed a significant effect (p=0.007) — inconsistent with 
a fully clean parallel-trends assumption. Investigation traced this to Kherson already being an 
active conflict zone in 2022 (including the Kherson liberation operation), meaning the original 
baseline period was not a genuinely quiet pre-conflict period.
""")

st.markdown("---")

st.markdown("### Placebo Test #2 — Narrowed Baseline (Ambiguous)")

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['accent']}; min-height: 160px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Real Date, Narrowed Baseline</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.1384</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.002</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 160px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Fake Date, Same Narrow Window</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.1382</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.169 (underpowered, n=10)</p>
    </div>
    """, unsafe_allow_html=True)

st.error("""
**Reported honestly as ambiguous, not confirmatory.** The fake-date placebo's coefficient is 
nearly identical in magnitude to the real result — a meaningfully weaker form of validation than 
a near-zero placebo coefficient, even though its p-value is not significant. With only 10 
observations in this narrowed window, low statistical power means this test cannot reliably 
distinguish a genuine null effect from an underpowered test of a real effect. This is why the 
broader-baseline result (-0.0703, p=0.007) is treated as the project's primary finding, with the 
narrowed result reported as a sensitivity analysis rather than a replacement.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Every result stress-tested, every limitation disclosed</p>",
    unsafe_allow_html=True,
)