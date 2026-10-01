import json
import os
import sys

import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
from styles import apply_custom_style  # noqa: E402

apply_custom_style()


def load(name):
    with open(os.path.join(PROJECT_ROOT, "outputs", "v2", name), encoding="utf-8") as f:
        return json.load(f)


def fig(name, caption):
    path = os.path.join(PROJECT_ROOT, "outputs", "v2", "figures", name)
    if os.path.exists(path):
        st.image(path, width="stretch")
        st.caption(caption)


S, R1 = load("study2_summary.json"), load("r1_summary.json")
h1, h2, r1h1, r1h2 = S["H1_flood"], S["H2_irrigation"], R1["H1_flood"], R1["H2_irrigation"]

st.markdown("<h1 style='text-align: center;'>🧪 STUDY 2 — MAIN RESULTS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Pre-registered, exposure-based "
            "pixel analysis (MODIS 250 m, 2016–2024)</h3>", unsafe_allow_html=True)
st.markdown("---")
st.info("""
**Design.**
- **Treatment defined by exposure:** flooded land, the drained reservoir bed, and canal-irrigated cropland.
- **Comparisons inside the war zone.**
- **Fixed in advance:** every rule and the words used for the verdicts were set in `ANALYSIS_PLAN_v2.md`
  (commit 521672f, before any data download).
- **Registered revision:** `ANALYSIS_PLAN_v2_ADDENDUM_1.md` (commit 30e3840) was committed before its extra data were
  downloaded. It fixed five problems the first results exposed.
""")


def f(x, d=3):
    return f"{x:+.{d}f}"


def pp(x):
    return "< 0.001" if x < 0.001 else f"{x:.3f}"


st.markdown(f"""
| Hypothesis | Pre-registered | Registered revision |
|---|---|---|
| **H1 flood**: flooded vs matched unflooded land | β = {f(h1['beta'])} (CI {h1['ci95_cluster'][0]:.3f} to {h1['ci95_cluster'][1]:.3f}); wild-bootstrap p = {pp(h1['p_wcr'])}; randomization p = {h1['p_randomization']:.2f} → **{h1['verdict']}** | β = {f(r1h1['beta'])}; randomization p = {r1h1['p_randomization']:.2f} → **{r1h1['verdict']}** |
| **H2 irrigation**: irrigated vs rainfed, canal zone vs elsewhere | β = {f(h2['beta'])}; Holm p = {pp(h2['p_wcr_holm'])}; randomization p = {h2['p_randomization']:.2f}; pre-trend p = {h2['pretrend_joint_p']:.1e} → **{h2['verdict']}** | β = {f(r1h2['beta'])}; after the breach vs 2021: 2023 {f(r1h2['event_study']['2023'])}, 2024 {f(r1h2['event_study']['2024'])} (n.s.); {r1h2['n_placebo_raions']} placebo districts p = {r1h2['p_randomization']:.2f} → **{r1h2['verdict']}** |
| **H3 reservoir bed** | NDVI > 0.3: {S['H3_reservoir_bed']['2021']['km2_ndvi_gt_0_3']:.0f} km² (2021) → {S['H3_reservoir_bed']['2024']['km2_ndvi_gt_0_3']:,.0f} km² (2024) | same trajectory on land-only pixels |
| **H4 Kherson decomposition** (2021→2024 vs zone O) | total {f(S['H4_decomposition']['total_relative_change'], 4)}; other land {f(S['H4_decomposition']['all other land'], 4)} | total {f(R1['H4']['total'], 4)} |
""")

st.warning("""
**How to read H2.**
- The pre-registered β is large, but the canal-zone contrast was already higher in 2016–2020 than in 2021.
- In the revision the divergence happens between 2020 and 2021, before the invasion, and does not deepen after
  the breach.
- "Suggestive" is the label the pre-registered rule produces. The evidence does not show a post-breach
  irrigation effect.
""")

st.markdown("### Exposure groups")
fig("s2_fig1_exposure_map.png", "Flooded land, reservoir bed, canal zone K, comparison zone O and placebo floodplains.")
st.markdown("### H1 and H2 event studies")
fig("s2_fig2_h1_event_study.png", "H1, pre-registered (left) and exploratory without caliper (right).")
fig("s2_fig3_h2_event_study.png", "H2, pre-registered.")
fig("s2_fig7_revision_event_studies.png", "Registered revision: H1 matched, H1 unmatched, H2.")
st.markdown("### Randomization inference")
fig("s2_fig4_randomization_inference.png", "Real estimates against placebo units.")
st.markdown("### Reservoir bed and decomposition")
fig("s2_fig5_h3_reservoir_bed.png", "Former reservoir bed, 2016–2024.")
fig("s2_fig6_h4_decomposition.png", "Contributions to Kherson Oblast's 2021→2024 change.")
st.caption("All numbers are read from outputs/v2/study2_summary.json and outputs/v2/r1_summary.json. "
           "Study 1 (oblast vs Romania) is on the other pages.")
