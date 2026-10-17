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


S, R1, H1R, R2 = load("study2_summary.json"), load("r1_summary.json"), load("h1_results.json"), load("r2_summary.json")
X1 = load("x1_review_diagnostics.json") if os.path.exists(
    os.path.join(PROJECT_ROOT, "outputs", "v2", "x1_review_diagnostics.json")) else None
h1, h2, r1h1, r1h2 = S["H1_flood"], S["H2_irrigation"], R1["H1_flood"], R1["H2_irrigation"]
h1all = H1R["robustness"]["1_no_matching"]
r2h1, r2h2, r2h4 = R2["H1_flood"], R2["H2_irrigation"], R2["H4"]
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
- **Second registered revision:** `ANALYSIS_PLAN_v2_ADDENDUM_2.md` (approved 16 Oct 2026; checksum in
  `v2/DEVIATIONS.md`) was committed before its data were downloaded: independent 30 m irrigation maps
  (Baber et al., 2026), flood matching on terrain, weather allowed to change the irrigation contrast.

Details: **Study 2 Methods and Data** in the sidebar.
""")


def f(x, d=3):
    return f"{x:+.{d}f}"


def pp(x):
    return "< 0.001" if x < 0.001 else f"= {x:.3f}"


st.markdown(f"""
| Pathway | Pre-registered | Registered revision | Second registered revision | What it means |
|---|---|---|---|---|
| **H1 flood**: flooded vs unflooded land, same river bank | all flooded pixels β = {f(h1all['beta'])} (CI {h1all['ci95_cluster'][0]:.3f} to {h1all['ci95_cluster'][1]:.3f}); matched sample (1.8% of pixels) β = {f(h1['beta'])}, wild-bootstrap p {pp(h1['p_wcr'])}, randomization p = {h1['p_randomization']:.2f} → **{h1['verdict']}** | matched β = {f(r1h1['beta'])}; all flooded pixels β = {f(r1h1['no_matching']['beta'])} → **{r1h1['verdict']}** | matched on terrain ({r2h1['share_of_flooded_matched']:.0%} of flooded pixels) β = {f(r2h1['beta'])} (CI {r2h1['ci95_cluster'][0]:.3f} to {r2h1['ci95_cluster'][1]:.3f}), placebo p = {r2h1['p_randomization']:.2f}; placebo-in-time {f(r2h1['placebo_in_time']['beta'])} → **{r2h1['verdict']}** | no detectable lasting loss of July–October greenness; wetlands declined ({f(r1h1['wetland_no_matching']['beta'])}) |
| **H2 irrigation** | irrigated (NDVI proxy) vs rainfed, canal zone vs elsewhere: β = {f(h2['beta'])}; Holm p {pp(h2['p_wcr_holm'])}; randomization p = {h2['p_randomization']:.2f} → **{h2['verdict']}** | β = {f(r1h2['beta'])}; vs 2021: 2023 {f(r1h2['event_study']['2023'])}, 2024 {f(r1h2['event_study']['2024'])}; placebo districts p = {r1h2['p_randomization']:.2f} → **{r1h2['verdict']}** | irrigated (Baber maps) vs never-irrigated cropland: β = {f(r2h2['beta'])} (CI {r2h2['ci95_cluster'][0]:.3f} to {r2h2['ci95_cluster'][1]:.3f}; {r2h2['beta_pct_of_base_mean']:.0f}% of the 2016–18 level); placebo test {f(r2h2['placebo_test']['beta'])} fails → **{r2h2['verdict']}** | a large loss on formerly irrigated fields from the breach on; not separable from other war effects |
| **H3 reservoir bed** (descriptive) | NDVI > 0.3: {min(pre_km2):.0f}–{max(pre_km2):.0f} km² each year 2016–22 → {h3['2023']['km2_ndvi_gt_0_3']:,.0f} km² (2023) → {h3['2024']['km2_ndvi_gt_0_3']:,.0f} km² (2024) | same trajectory on land-only pixels | Sentinel-2 check: {R2['H3_check']['sentinel2_km2_ndvi_gt_0_3']:.0f} vs MODIS {R2['H3_check']['modis_km2_ndvi_gt_0_3']:.0f} km² on the same {R2['H3_check']['same_pixels_km2']:.0f} km² | the largest change |
| **H4 Kherson decomposition** | 2021→2024: total {f(S['H4_decomposition']['total_relative_change'], 4)}; reservoir bed {f(S['H4_decomposition']['former reservoir bed'], 4)} | total {f(R1['H4']['total'], 4)} | 2016–18→2023–24: total {f(r2h4['total']['contribution'])} (CI {r2h4['total']['ci95'][0]:.3f} to {r2h4['total']['ci95'][1]:.3f}); irrigated cropland {f(r2h4['R9 irrigated cropland']['contribution'])} | irrigated fields, 4% of the area, carry much of the decline |
""")

st.warning("""
**How to read H2.** The first two analyses could not test the irrigation pathway: their NDVI-based "irrigated" group
mostly captured summer crops, weather could not change the contrast, and part of the comparison land was irrigated.
The second revision uses independent irrigation maps (Baber et al., 2026). Formerly irrigated fields then lost about
a third of their summer greenness after the breach. The pre-registered rule still says **suggestive**: the fields were
already greener in 2019–2021, the years used to identify them, so the placebo test fails, and there is no irrigated
land outside the canal system to compare with.
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
st.markdown("### Second registered revision")
fig("s2_fig8_r2_flood.png", "H1, matched on terrain and land cover (red) and not matched (grey), relative to 2016–2018.")
fig("s2_fig9_r2_irrigation.png", "H2 with the Baber et al. irrigation maps, relative to 2016–2018, with canal-zone rainfall.")
fig("s2_fig10_r2_h4.png", "H4, 2016–2018 → 2023–2024, with 95% block-bootstrap intervals.")
st.markdown("### Randomization inference")
fig("s2_fig4_randomization_inference.png", "Real estimates against placebo units (pre-registered plan).")
st.markdown("### Reservoir bed and decomposition")
fig("s2_fig5_h3_reservoir_bed.png", "Former reservoir bed, 2016–2024.")
fig("s2_fig6_h4_decomposition.png", "Contributions to Kherson Oblast's 2021→2024 change. \"All other land\" means land "
    "outside the exposure definitions; it includes irrigated land more than 5 km from the mapped canals.")
st.caption("All numbers are read from outputs/v2/study2_summary.json, r1_summary.json, r2_summary.json, "
           "h1_results.json and x1_review_diagnostics.json. Study 1 (oblast vs Romania) is on the pages marked Study 1.")
