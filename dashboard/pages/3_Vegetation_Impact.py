import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
from results import R, p, c, ci, sig
from styles import apply_custom_style, PALETTE

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>🌿 VEGETATION IMPACT</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Difference-in-Differences Analysis</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.markdown("""
NDVI was compared between Kherson (treatment) and Tulcea (primary control) with a
Difference-in-Differences model on the monthly Kherson-minus-Tulcea NDVI gap (before vs after
June 2023), using Newey-West HAC standard errors.
""")

st.markdown("---")

st.markdown("### NDVI: Treatment vs. Control Over Time")

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "ndvi_comparison.png")
if os.path.exists(image_path):
    st.image(image_path, width="stretch")
else:
    st.warning("NDVI comparison image not found.")

st.markdown("---")

st.markdown("### The Result")

m, ms, n = R["main_did"], R["main_did_seasonal"], R["narrowed_did"]
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 200px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Primary result</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 2rem; font-weight: 900; margin-bottom: 4px;">{c(m)}</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin-bottom: 12px;">95% CI {ci(m)} · HAC p = {p(m['p'])} · {sig(m['p'])}</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.85rem; margin: 0;">
            Kherson's NDVI fell relative to Tulcea after June 2023. The estimate is
            {100*m['pct_of_pre_mean']:.0f}% of Kherson's pre-period mean NDVI — a scale reference,
            not a measured loss of vegetation — and it does not by itself show that the dam caused it.
        </p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['accent']}; min-height: 200px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">With zone-specific seasonality</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 2rem; font-weight: 900; margin-bottom: 4px;">{c(ms)}</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin-bottom: 12px;">95% CI {ci(ms)} · HAC p = {p(ms['p'])}</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 0.85rem; margin: 0;">
            Tulcea's seasonal swing is larger than Kherson's, and the post period contains more
            summer–autumn months than the pre period. Letting each zone keep its own seasonal
            cycle removes {100*(1-ms['coef']/m['coef']):.0f}% of the estimate; the rest remains.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.info(f"""
A narrowed baseline (Jan 2023 onward) gives a larger estimate ({c(n)}, p = {p(n['p'])}), but its own
placebo test on the same five pre-event months is also significant (p = {p(R['placebo_narrowed']['p'])}),
so it is not treated as evidence. Against the four-county panel the pooled estimate is
{c(R['pooled_did'])} (p = {p(R['pooled_did']['p'])}). See **Statistical Validation** for all checks.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Source: Sentinel-2 (Copernicus Data Space Ecosystem)</p>",
    unsafe_allow_html=True,
)