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


S, R1, H1R = load("study2_summary.json"), load("r1_summary.json"), load("h1_results.json")
X1 = load("x1_review_diagnostics.json") if os.path.exists(
    os.path.join(PROJECT_ROOT, "outputs", "v2", "x1_review_diagnostics.json")) else None
h1, h2, r1h1, r1h2 = S["H1_flood"], S["H2_irrigation"], R1["H1_flood"], R1["H2_irrigation"]
h1all = H1R["robustness"]["1_no_matching"]
h3 = S["H3_reservoir_bed"]
pre_km2 = [h3[str(y)]["km2_ndvi_gt_0_3"] for y in range(2016, 2023)]

st.markdown("<h1 style='text-align: center;'>🧪 STUDY 2 — MAIN RESULTS</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Pre-registered, exposure-based "
            "pixel analysis (MODIS 250 m, 2016–2024)</h3>", unsafe_allow_html=True)
st.markdown("---")
st.info("""
**Research question.** Which physical pathway of the dam's destruction — the flood, the drained reservoir or the loss
of canal irrigation — left a detectable mark on vegetation, compared with similar land in the same war zone?

- **Treatment defined by exposure:** flooded land, the drained reservoir bed, and cropland near the reservoir's canals.
- **Comparisons inside the war zone.**
- **Fixed in advance:** every rule and the words used for the verdicts were set in `ANALYSIS_PLAN_v2.md`
  (commit 521672f, before any data download).
- **Registered revision:** `ANALYSIS_PLAN_v2_ADDENDUM_1.md` (commit 30e3840) was committed before its extra data were
  downloaded. It fixed five problems the first results exposed.

Details: **Study 2 Methods and Data** in the sidebar.
""")


def f(x, d=3):
    return f"{x:+.{d}f}"


def pp(x):
    return "< 0.001" if x < 0.001 else f"= {x:.3f}"


st.markdown(f"""
| Pathway | Pre-registered | Registered revision | What it means |
|---|---|---|---|
| **H1 flood**: flooded vs unflooded land, same river bank | all flooded pixels β = {f(h1all['beta'])} (CI {h1all['ci95_cluster'][0]:.3f} to {h1all['ci95_cluster'][1]:.3f}); matched sample (1.8% of pixels) β = {f(h1['beta'])}, wild-bootstrap p {pp(h1['p_wcr'])}, randomization p = {h1['p_randomization']:.2f} → **{h1['verdict']}** | matched β = {f(r1h1['beta'])}; all flooded pixels β = {f(r1h1['no_matching']['beta'])} → **{r1h1['verdict']}** | no detectable lasting loss of July–October greenness; wetlands declined ({f(r1h1['wetland_no_matching']['beta'])}) |
| **H2 irrigation**: irrigated vs rainfed, canal zone vs elsewhere | β = {f(h2['beta'])}; Holm p {pp(h2['p_wcr_holm'])}; randomization p = {h2['p_randomization']:.2f}; pre-trend p = {h2['pretrend_joint_p']:.1e} → **{h2['verdict']}** | β = {f(r1h2['beta'])}; vs 2021: 2023 {f(r1h2['event_study']['2023'])}, 2024 {f(r1h2['event_study']['2024'])} (n.s.); {r1h2['n_placebo_raions']} placebo districts p = {r1h2['p_randomization']:.2f} → **{r1h2['verdict']}** | the design cannot attribute the decline to the loss of canal water (see below) |
| **H3 reservoir bed** (descriptive) | NDVI > 0.3: {min(pre_km2):.0f}–{max(pre_km2):.0f} km² each year 2016–22 → {h3['2023']['km2_ndvi_gt_0_3']:,.0f} km² (2023) → {h3['2024']['km2_ndvi_gt_0_3']:,.0f} km² (2024) | same trajectory on land-only pixels | the largest change |
| **H4 Kherson decomposition** (2021→2024 vs zone O) | total {f(S['H4_decomposition']['total_relative_change'], 4)}; reservoir bed {f(S['H4_decomposition']['former reservoir bed'], 4)}; irrigated canal zone {f(S['H4_decomposition']['Kakhovka zone, irrigated cropland'], 4)}; land outside the exposure groups {f(S['H4_decomposition']['all other land'], 4)} | total {f(R1['H4']['total'], 4)} | an oblast average mixes changes of opposite sign |
""")

st.warning("""
**How to read H2.** "Suggestive" is the label the pre-registered rule produces. In substance, this design neither
shows nor rules out an effect of the lost canal water:
- the canal-zone contrast was already declining over 2016–2021, before the war;
- the year-by-year results are compared with 2021, the wettest summer of the record, and the contrast moves closely
  with summer rain, which the models do not allow for;
- the placebo districts with the largest declines lie next to the canal network and are partly irrigated by it;
- the NDVI-based "irrigated" group mostly captures summer crops.

Other work shows that irrigated area fell by about 90% (Baber et al., 2026; NASA Harvest).
""")

if X1 is not None:
    st.markdown("### Exploratory checks (after all registered results were known)")
    st.caption("From v2/analysis/x1_review_diagnostics.py. Not part of either registered plan; they change no verdict.")
    w = X1["D1_weather_jul_oct"]["zone_K"]
    d2 = X1["D2_h2_event_study_vs_zoneK_rain"]["revision"]
    yrs = sorted(w)
    st.markdown("**July–October rainfall and temperature in the canal zone (ERA5-Land)**\n\n"
                "| | " + " | ".join(yrs) + " |\n|---|" + "---|" * len(yrs) + "\n"
                "| Rain (mm) | " + " | ".join(f"{w[y]['precip_mm']:.0f}" for y in yrs) + " |\n"
                "| Temperature (°C) | " + " | ".join(f"{w[y]['temp_c']:.1f}" for y in yrs) + " |")
    st.markdown(f"Before the war, the revision's irrigated–rainfed contrast followed this rainfall closely "
                f"(r = {d2['pearson_r_2016_2021']:+.2f}, 2016–2021). The reference year "
                f"{X1['D1_weather_jul_oct']['wettest_year_zone_K']} was the wettest; "
                f"{X1['D1_weather_jul_oct']['driest_year_zone_K']} was the driest.")
    D3 = X1["D3_placebo_districts"]
    rows = sorted(D3["units"].items(), key=lambda kv: kv[1]["beta"])
    st.markdown("**Placebo districts of the revision**\n\n| District | Placebo β | Cropland in canal zone | "
                "Median distance of its comparison cropland to the canals | Adjoins the network |\n|---|---|---|---|---|\n"
                + "\n".join(f"| {k} | {v['beta']:+.3f} | {v['share_cropland_in_zone_K']:.0%} | "
                            f"{v['median_km_zoneO_to_network']:.0f} km | {'yes' if v['adjoins_network'] else 'no'} |"
                            for k, v in rows)
                + f"\n| **Real canal zone** | **{D3['beta_real']:+.3f}** | | | |")
    st.markdown(f"Randomization p: {D3['p_one_sided_all']:.2f} with all districts; "
                f"{D3['p_one_sided_not_adjoining']:.2f} without the districts that adjoin the network "
                f"({D3['n_placebos_not_adjoining']} placebos).")

st.markdown("### Exposure groups")
fig("s2_fig1_exposure_map.png", "Flooded land, reservoir bed, canal zone K, comparison zone O and placebo floodplains.")
st.markdown("### H1 and H2 event studies")
fig("s2_fig2_h1_event_study.png", "H1, pre-registered matching (left; flat pre-period expected because matching uses "
    "the pre-war values) and exploratory matching without caliper (right).")
fig("s2_fig3_h2_event_study.png", "H2, pre-registered. The reference year 2021 was the wettest summer of the record.")
fig("s2_fig7_revision_event_studies.png", "Registered revision: H1 matched, H1 unmatched, H2.")
st.markdown("### Randomization inference")
fig("s2_fig4_randomization_inference.png", "Real estimates against placebo units (pre-registered plan).")
st.markdown("### Reservoir bed and decomposition")
fig("s2_fig5_h3_reservoir_bed.png", "Former reservoir bed, 2016–2024.")
fig("s2_fig6_h4_decomposition.png", "Contributions to Kherson Oblast's 2021→2024 change. \"All other land\" means land "
    "outside the exposure definitions; it includes irrigated land more than 5 km from the mapped canals.")
st.caption("All numbers are read from outputs/v2/study2_summary.json, r1_summary.json, h1_results.json and "
           "x1_review_diagnostics.json. Study 1 (oblast vs Romania) is on the pages marked Study 1.")
