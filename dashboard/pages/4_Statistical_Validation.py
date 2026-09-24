import streamlit as st
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
from styles import apply_custom_style, PALETTE
from results import R, NAMES, p, c, ci, sig

apply_custom_style()

st.markdown("<h1 style='text-align: center;'>📊 STATISTICAL VALIDATION</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Every Check, With Its Actual Result</h3>",
    unsafe_allow_html=True,
)
st.markdown("---")

st.error(f"""
**Read this first — the analysis was corrected three times.**
1. *Geometry:* NDVI was first extracted over bounding boxes; it now uses each zone's GADM polygon.
2. *Inference:* HAC standard errors were first applied to a stacked table of both zones; all models
   now run on the monthly treated-minus-control gap, where the lags are calendar months.
3. *Extraction:* the second version sampled zones on a coarse default grid, kept water pixels and used
   one scene per month; the current data use a common ~150–220 m grid, mask water, and take each
   pixel's median over all clear acquisitions in the month.

Current primary estimate: {c(R['main_did'])} (95% CI {ci(R['main_did'])}, HAC p = {p(R['main_did']['p'])})
— **{sig(R['main_did']['p'])}**. The checks below show why that still does not attribute the decline to the dam.
""")

m = R["main_did"]
checks = [
    ("✓" if m["p"] < 0.05 else "!", PALETTE["vegetation"] if m["p"] < 0.05 else PALETTE["warning"], f"Primary DiD — {sig(m['p'])} (p = {p(m['p'])})"),
    ("✓" if R["main_did_seasonal"]["p"] < 0.05 else "!", PALETTE["vegetation"] if R["main_did_seasonal"]["p"] < 0.05 else PALETTE["warning"], f"Zone-specific seasonality — {c(R['main_did_seasonal'])} (p = {p(R['main_did_seasonal']['p'])})"),
    ("✓", PALETTE["vegetation"], f"Placebo, fake date Jun 2022 — clean (p = {p(R['placebo_broad']['p'])})"),
    ("!", PALETTE["warning"], f"Narrowed-baseline placebo — significant (p = {p(R['placebo_narrowed']['p'])})"),
    ("!", PALETTE["warning"], "Event study — significant pre-event quarters"),
    ("!", PALETTE["warning"], f"Placebo in space — Kherson rank {R['placebo_in_space']['rank_one_sided']}/5"),
    ("!", PALETTE["warning"], "Control-only check — controls not all stable (Constanța moves like Kherson)"),
]
badges = "".join(
    f"""<span style="display:inline-flex; align-items:center; gap:6px; background:rgba(0,172,193,0.08);
        border:1px solid rgba(0,172,193,0.3); border-radius:20px; padding:6px 14px; margin:4px;
        font-size:0.82rem; color:{PALETTE['text_primary']}; font-weight:600;">
        <span style="color:{col}; font-weight:900;">{mark}</span>{label}</span>"""
    for mark, col, label in checks
)
st.markdown(f"<div style='display:flex; flex-wrap:wrap; margin-bottom: 6px;'>{badges}</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Primary Estimate and Placebo Tests")
image = os.path.join(PROJECT_ROOT, "outputs", "plots", "robustness_check.png")
if os.path.exists(image):
    st.image(image, width="stretch")
st.markdown(f"""
| Model | Estimate | 95% CI (HAC) | HAC p | Classical p |
|---|---|---|---|---|
| Primary DiD, Jan 2022 – Nov 2024 | {c(R['main_did'])} | {ci(R['main_did'])} | {p(R['main_did']['p'])} | {p(R['main_did']['classic_p'])} |
| + zone-specific seasonality | {c(R['main_did_seasonal'])} | {ci(R['main_did_seasonal'])} | {p(R['main_did_seasonal']['p'])} | {p(R['main_did_seasonal']['classic_p'])} |
| Placebo, fake date Jun 2022 | {c(R['placebo_broad'])} | {ci(R['placebo_broad'])} | {p(R['placebo_broad']['p'])} | {p(R['placebo_broad']['classic_p'])} |
| Narrowed baseline, Jan 2023 – Nov 2024 | {c(R['narrowed_did'])} | {ci(R['narrowed_did'])} | {p(R['narrowed_did']['p'])} | {p(R['narrowed_did']['classic_p'])} |
| Narrowed placebo, fake date Mar 2023 (5 months) | {c(R['placebo_narrowed'])} | {ci(R['placebo_narrowed'])} | {p(R['placebo_narrowed']['p'])} | {p(R['placebo_narrowed']['classic_p'])} |
""")
st.info("""
The June 2022 placebo is clean, but the narrowed-baseline placebo is significant, so the larger
narrowed-baseline estimate cannot be separated from ordinary short-window movement in the gap.
With only five months, that placebo is fragile in either direction.
""")

st.markdown("---")
st.markdown("### Event Study — Quarterly Gap")
image = os.path.join(PROJECT_ROOT, "outputs", "plots", "event_study.png")
if os.path.exists(image):
    st.image(image, width="stretch")
q = R["event_study"]["quarters"]
pre_sig = [r for r in q if r["quarter"] < 0 and r["p"] < 0.05]
post_sig = [r for r in q if r["quarter"] >= 0 and r["p"] < 0.05]
st.warning(f"""
**Parallel trends do not hold cleanly.** {len(pre_sig)} of the 5 pre-event quarters differ significantly
from the reference quarter ({', '.join(r['months'] for r in pre_sig)}), including Jun–Aug 2022 at
{q[2]['coef']:+.3f}. Part of the post-event pattern is therefore seasonal. What seasonality cannot explain
is the comparison of the same season across years: the Jun–Aug gap was {q[2]['coef']:+.3f} in 2022,
{q[5]['coef']:+.3f} in 2023 and {q[9]['coef']:+.3f} in 2024, and the Sep–Nov gap {q[3]['coef']:+.3f},
{q[6]['coef']:+.3f} and {q[10]['coef']:+.3f}. The decline deepens in the second post-event season rather than
appearing as a single step in June 2023. Bonferroni threshold across 11 quarters: p < {R['event_study']['bonferroni_threshold']:.5f}.
""")


st.markdown("---")
st.markdown("### Four-County Panel")
image = os.path.join(PROJECT_ROOT, "outputs", "plots", "control_panel_comparison.png")
if os.path.exists(image):
    st.image(image, width="stretch")
pc = R["per_control"]
st.markdown(f"""
| Comparison | Estimate | 95% CI | HAC p |
|---|---|---|---|
""" + "\n".join(f"| Kherson vs {NAMES[z]} | {c(pc[z])} | {ci(pc[z])} | {p(pc[z]['p'])} |" for z in ["tulcea", "galati", "braila", "constanta"])
    + f"\n| Kherson vs mean of all four | {c(R['pooled_did'])} | {ci(R['pooled_did'])} | {p(R['pooled_did']['p'])} |"
    + f"\n| Pooled + zone-specific seasonality | {c(R['pooled_did_seasonal'])} | {ci(R['pooled_did_seasonal'])} | {p(R['pooled_did_seasonal']['p'])} |"
    + f"\n| Pooled placebo, fake date Jun 2022 | {c(R['pooled_placebo'])} | {ci(R['pooled_placebo'])} | {p(R['pooled_placebo']['p'])} |")
st.info("""
Kherson declines against Tulcea, Galați and Brăila and against their mean; against Constanța there is
no difference. Cluster-robust standard errors are not reported: with five
units they are unreliable (Cameron & Miller, 2015).
""")

st.markdown("---")
st.markdown("### Placebo in Space — Randomization Inference")
image = os.path.join(PROJECT_ROOT, "outputs", "plots", "placebo_in_space.png")
if os.path.exists(image):
    st.image(image, width="stretch")
pis = R["placebo_in_space"]
st.error(f"""
Each of the five units was assigned "treated" status in turn against the other four at the real
June 2023 date (Conley & Taber, 2011). Kherson ranks {pis['rank_one_sided']} of 5 one-sided (exact
p = {pis['p_one_sided']:.2f}) and {pis['rank_two_sided']} of 5 two-sided (p = {pis['p_two_sided']:.2f}).
With five units the smallest possible exact p-value is 0.20, so this check can only show whether
Kherson stands out — and it does not: Constanța shifts by as much.
""")

st.markdown("---")
st.markdown("### Control-Only Divergence Check (Kherson excluded)")
cd = R["control_divergence"]
st.markdown("| County vs the other three | Estimate | 95% CI | HAC p |\n|---|---|---|---|\n" +
            "\n".join(f"| {NAMES[z]} | {c(cd[z])} | {ci(cd[z])} | {p(cd[z]['p'])} |" for z in ["tulcea", "galati", "braila", "constanta"]))
st.warning("""
The control counties are not all stable: Constanța moves in the same direction as Kherson and Brăila
moves slightly the other way. This check shows that shifts happened, not why (regional spillover,
shipping, agricultural markets, weather or land use are all possible).
""")


st.markdown("---")
st.markdown("### Specification Checks")
lag = R["lag_sensitivity"]
lc = R["low_coverage"]
st.markdown(f"""
- **HAC lag length 1–6:** p ranges from {min(v['p'] for v in lag.values()):.3f} to {max(v['p'] for v in lag.values()):.3f}.
- **log(NDVI):** {c(R['log_ndvi'], 3)} log points ≈ {100*R['log_ndvi']['pct_change']:.0f}% (p = {p(R['log_ndvi']['p'])}).
- **Dropping low-coverage zone-months:** <15% valid → {c(lc['0.15']['main'])} (p = {p(lc['0.15']['main']['p'])});
  <25% valid → {c(lc['0.25']['main'])} (p = {p(lc['0.25']['main']['p'])}).
""")

st.markdown("---")
st.markdown(
    f"<p class='caption-text' style='text-align:center;'>All numbers read from outputs/model_results.json "
    f"(generated {R['meta']['generated_utc']}, data: {R['meta']['ndvi_dir']})</p>",
    unsafe_allow_html=True,
)
