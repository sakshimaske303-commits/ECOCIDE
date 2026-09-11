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

st.error("""
**Methodology correction (read this first).** An earlier version of this project's NDVI
extraction queried Sentinel Hub using each zone's rectangular bounding box rather than its
true GADM administrative polygon, and filtered clouds only at the whole-scene level. Both
are now corrected — true polygon geometry, plus pixel-level Sentinel-2 cloud/shadow/snow
masking — and the correction **materially weakens the primary result**, from HAC p=0.022
to p=0.060 (no longer significant at the conventional 5% level), and reveals that Kherson
is no longer the most extreme unit under randomization inference (see below). Everything
on this page reflects the corrected analysis.
""")

_checks = [
    ("!", PALETTE['warning'], "Primary DiD — Marginal, p=0.060 (was p=0.022)"),
    ("✓", PALETTE['vegetation'], "Matched Non-Conflict Control Zone (Tulcea, Romania)"),
    ("✓", PALETTE['vegetation'], "HAC-Robust Standard Errors (Newey-West)"),
    ("✓", PALETTE['vegetation'], "Placebo Test #1 — Clean Pass (broad baseline)"),
    ("✓", PALETTE['vegetation'], "Placebo Test #2 — No Longer Fails Under HAC (narrowed baseline)"),
    ("✓", PALETTE['vegetation'], "Quarterly Event-Study Check"),
    ("✓", PALETTE['vegetation'], "Month Fixed Effects (seasonal controls)"),
    ("✓", PALETTE['vegetation'], "Multi-Sensor Verified Flood Data (UNOSAT, 5 sensors)"),
    ("!", PALETTE['warning'], "Multi-Control Robustness Check (4-control panel, only 2 of 4 reproduce it)"),
    ("!", PALETTE['warning'], "Placebo-in-Space — Kherson No Longer the Most Extreme Unit"),
    ("!", PALETTE['warning'], "Control-Only Spillover — 2 of 4 Controls Move Independently"),
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
        Several checks are flagged, not hidden — see the Placebo-in-Space and Control-Only
        Spillover sections below for the most consequential ones.
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
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.0747</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.060 (HAC) — Marginal, not significant at 5%</p>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['text_secondary']}; min-height: 160px;">
        <p style="color: {PALETTE['text_secondary']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Fake Treatment Date (June 2022)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">+0.0051</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.882 (HAC) — Not significant</p>
    </div>
    """, unsafe_allow_html=True)

st.success("""
**This specific check is still clean.** A near-zero coefficient AND a high p-value together show
the real-date estimate is not an artifact of a general pre-existing trend in Kherson — whatever it
is, it isn't present at an arbitrary earlier date. This holds under both classical and Newey-West
HAC standard errors. It does **not**, however, mean the real-date estimate itself is strong: at
p=0.060 it is only marginal, and the placebo-in-space and control-only spillover checks further
down this page are a more direct test of whether it can be trusted at face value.
""")

st.markdown("---")

st.markdown("### Event Study — Quarterly Treatment Effects")

image_path = os.path.join(PROJECT_ROOT, "outputs", "plots", "event_study.png")
if os.path.exists(image_path):
    st.image(image_path, use_container_width=True)
else:
    st.warning("Event study image not found.")

st.warning("""
**A genuine limitation, disclosed honestly:** Quarters immediately following the event
(Quarter 0: HAC p<0.0001; Quarter +1: HAC p=0.0005; Quarter +4: HAC p<0.0001) show significant
negative effects — all four now stronger under the corrected data than originally reported — but
one pre-event quarter (Quarter -4, summer 2022) also shows a significant effect (HAC p<0.0001),
inconsistent with a fully clean parallel-trends assumption. This is traced, as before, to Kherson
already being an active conflict zone in 2022 (including the Kherson liberation operation), meaning
the original baseline period was not a genuinely quiet pre-conflict period. See the Methodology
page for the multiple-testing correction applied to all eleven quarters tested here.
""")

st.markdown("---")

st.markdown("### Placebo Test #2 — Narrowed Baseline (No Longer Fails Under HAC)")

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['accent']}; min-height: 160px;">
        <p style="color: {PALETTE['accent']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Real Date, Narrowed Baseline</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.1497</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.0004 (HAC)</p>
    </div>
    """, unsafe_allow_html=True)
with col4:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 160px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Fake Date, Same Narrow Window</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.1098</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">Classical p = 0.323 · HAC p = 0.069 (n=10)</p>
    </div>
    """, unsafe_allow_html=True)

st.success("""
**One check that improved, not worsened, under the correction.** An earlier version of this
dashboard reported this placebo as a genuine validation failure: under Newey-West HAC standard
errors, the fake-date coefficient came back statistically significant (p=0.001), nearly matching
the real result's magnitude. Under the corrected polygon+SCL NDVI extraction, that same placebo
is no longer significant under HAC (p=0.069). This specific concern is therefore less severe than
previously reported — though the small sample (n=10) means this comparison should not be
over-read in either direction, and the narrowed-baseline specification remains a secondary,
illustrative check, not the project's primary finding. That role belongs to the primary
two-zone specification above (-0.0747, HAC p=0.060), which is the specification most affected by
this revision — see the Placebo-in-Space section below for why.
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
under Newey-West HAC, on the corrected polygon+SCL NDVI. The main DiD's HAC interval now straddles
zero by a small margin, unlike the original bounding-box estimate; the narrowed-baseline DiD stays
clearly bounded away from zero either way. The broad-baseline placebo interval straddles zero
under both specifications (clean validation). The narrowed-baseline placebo interval, which
excluded zero under HAC in an earlier version of this analysis, now straddles zero under HAC too —
the visual signature of the improvement discussed above.
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
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 160px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Pooled: All 4 Controls (HAC)</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">-0.0661</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">p = 0.059 (HAC) · p = 0.034 (cluster-robust) — marginal</p>
    </div>
    """, unsafe_allow_html=True)
with col6:
    st.markdown(f"""
    <div class="forensic-card" style="border-left: 4px solid {PALETTE['warning']}; min-height: 160px;">
        <p style="color: {PALETTE['warning']}; font-weight: 800; font-size: 0.85rem; text-transform: uppercase; margin-bottom: 10px;">Per-Control Check</p>
        <p style="color: {PALETTE['text_primary']}; font-size: 1.6rem; font-weight: 900; margin-bottom: 4px;">2 of 4</p>
        <p style="color: {PALETTE['text_secondary']}; font-size: 0.85rem; margin: 0;">Galați, Brăila confirm — Tulcea now marginal, Constanța does not</p>
    </div>
    """, unsafe_allow_html=True)

st.warning("""
**Two honest complications, both worse under the corrected data than originally reported.**
First, Constanța — the most purely Black Sea coastal, most urbanized of the four control
counties — does not reproduce the effect (coefficient +0.0186, p = 0.602, sign flipped from the
pooled direction), and Tulcea, the primary specification's own control, is now itself only
marginal (p = 0.060); only Galați and Brăila individually hold up clearly. The Control-Only
Spillover section below traces Constanța's null result to a concrete cause, not just an open
ecological question. Second, cluster-robust inference at only 5 clusters (one treatment, four
control) is thinner than the 30-40+ clusters standard guidance wants — on the pooled DiD model
this is a real but survivable caveat, but extending the same panel to a quarterly event study
pushes it past the point of being usable at all: several coefficients come back with numerically
degenerate standard errors (~1e-16), an artifact of too many parameters for too few clusters. HAC
is reported for that model instead, and shows the treatment-quarter effect still not significant
(p = 0.278) when pooled across four heterogeneous controls, while the one-year-later effect
still is (p = 0.0001).
""")

st.markdown("---")

st.markdown("### Placebo-in-Space — The Randomization-Inference Check")

st.markdown("""
The per-control check above always holds Kherson fixed as the treated unit. A more searching
question, with only five geographic units on the table: if one of the four Romanian counties,
rather than Kherson, had been assigned "treated" status at the real June 2023 cutoff, would it
have shown an effect just as large? Cluster-robust or HAC p-values computed from five clusters
cannot rule this out on their own (Conley & Taber, 2011) — an exact randomization test can.
""")

_pis_rows = [
    ("Kherson (real treated unit)", "-0.0661", "0.059", True),
    ("Brăila", "+0.0935", "0.015", False),
    ("Constanța", "-0.0893", "0.048", False),
    ("Galați", "+0.0345", "0.291", False),
    ("Tulcea", "+0.0273", "0.448", False),
]
_pis_html = "".join(
    f"""<tr style="{'background:rgba(255,193,7,0.08);' if real else ''}">
        <td style="padding:8px 14px; font-weight:{'800' if real else '500'};">{name}</td>
        <td style="padding:8px 14px; text-align:right;">{coef}</td>
        <td style="padding:8px 14px; text-align:right;">{p}</td>
    </tr>"""
    for name, coef, p, real in _pis_rows
)
st.markdown(
    f"""
    <table style="width:100%; border-collapse:collapse; color:{PALETTE['text_primary']}; font-size:0.9rem;">
        <thead><tr style="border-bottom:2px solid {PALETTE['accent']};">
            <th style="text-align:left; padding:8px 14px;">Zone assigned "treated"</th>
            <th style="text-align:right; padding:8px 14px;">did_term</th>
            <th style="text-align:right; padding:8px 14px;">HAC p</th>
        </tr></thead>
        <tbody>{_pis_html}</tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

st.error("""
**The single most consequential finding of this correction.** Ranked one-sided (most-negative
first), Kherson is 2nd of 5 (exact randomization p = 0.40); ranked two-sided (largest absolute
effect first), Kherson is 3rd of 5 (exact p = 0.60). Both are materially worse than the
originally-reported rank of 1st of 5 (exact p = 0.20 — already the best score obtainable with
only five units). Brăila and Constanța, with no dam ever having failed near them, show effects
comparable to or larger than Kherson's own under the identical procedure. With only five
clusters, randomization inference cannot distinguish Kherson's post-event decline from these two
counties' own idiosyncratic movement over the same window. The section below investigates what
is actually happening in Brăila and Constanța directly.
""")

st.markdown("---")

st.markdown("### Control-Only Spillover Check — Excluding Kherson Entirely")

st.markdown("""
This design assumes the treatment (the dam's destruction) has no effect on the control zones. The
~350km distance and international border were originally the only argument for that assumption.
This test checks it directly: with Kherson removed from the panel entirely, each of the four
Romanian counties is assigned "treated" status in turn against the other three, at the same real
June 2023 cutoff. If regional war effects had spilled into the controls, at least one comparison
should show a shift even with Kherson absent.
""")

_spill_rows = [
    ("Tulcea", "+0.0116", "0.742", False),
    ("Galați", "+0.0192", "0.567", False),
    ("Brăila", "+0.0821", "0.027", True),
    ("Constanța", "-0.1129", "0.020", True),
]
_spill_html = "".join(
    f"""<tr style="{'background:rgba(255,82,82,0.08);' if sig else ''}">
        <td style="padding:8px 14px; font-weight:{'800' if sig else '500'};">{name}</td>
        <td style="padding:8px 14px; text-align:right;">{coef}</td>
        <td style="padding:8px 14px; text-align:right;">{p}</td>
        <td style="padding:8px 14px; text-align:right;">{'⚠️ significant' if sig else 'clean'}</td>
    </tr>"""
    for name, coef, p, sig in _spill_rows
)
st.markdown(
    f"""
    <table style="width:100%; border-collapse:collapse; color:{PALETTE['text_primary']}; font-size:0.9rem;">
        <thead><tr style="border-bottom:2px solid {PALETTE['accent']};">
            <th style="text-align:left; padding:8px 14px;">Control county (vs. other 3)</th>
            <th style="text-align:right; padding:8px 14px;">did_term</th>
            <th style="text-align:right; padding:8px 14px;">HAC p</th>
            <th style="text-align:right; padding:8px 14px;">Result</th>
        </tr></thead>
        <tbody>{_spill_html}</tbody>
    </table>
    """,
    unsafe_allow_html=True,
)

st.error("""
**Two of four controls move independently — up from one in the original analysis.** Tulcea and
Galați come back clean, with no detectable shift relative to the other controls. But both Brăila
(p=0.027) and Constanța (p=0.020) show a significant shift relative to the other three — Brăila
was only borderline before (p=0.069), and Constanța's already-significant result is now more so.
This gives the placebo-in-space finding above a concrete mechanism: Brăila and Constanța are not
random noise from the randomization draw, they are counties that genuinely moved on their own,
independent of Kherson, around the same window, for reasons this design does not identify
(disrupted Black Sea shipping and regional agricultural-market effects are plausible candidates,
but this test establishes that a shift happened, not why). Because the primary specification uses
Tulcea — the one control that passes this check cleanly — the primary two-zone result is not
directly compromised by this, but the four-county pooled panel and the placebo-in-space ranking
both are, more so than this project originally disclosed.
""")

st.markdown("---")
st.markdown(
    "<p class='caption-text' style='text-align:center;'>ECOCIDE — Every result stress-tested, every limitation disclosed</p>",
    unsafe_allow_html=True,
)