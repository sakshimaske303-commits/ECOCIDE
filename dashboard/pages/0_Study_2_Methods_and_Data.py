import json
import os
import sys

import streamlit as st

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(PROJECT_ROOT, "dashboard"))
from styles import apply_custom_style  # noqa: E402

apply_custom_style()


def load(rel):
    with open(os.path.join(PROJECT_ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


LM = load("data/v2/derived/layers_meta.json")
PM = load("data/v2/derived/panel_meta.json")
H1R = load("outputs/v2/h1_results.json")
H2R = load("outputs/v2/h2_results.json")
R2 = load("outputs/v2/r2_summary.json")
R2H1 = load("outputs/v2/r2_h1_results.json")
R2H2 = load("outputs/v2/r2_h2_results.json")
RES_KM2 = (231.656358 / 1000) ** 2
cnt = LM["counts_px"]
m = H1R["matching"]
c2 = H2R["main"]["counts"]
mm = R2H1["covariate_matching"]["matching"]
s2 = R2H2["sample"]["pixels"]
val = R2H2["validation_R1_vs_R9_pixels"]


def share(o, k):
    d = val[o]["R1 irrigated"]
    return 100 * d[k] / sum(d.values())

st.markdown("<h1 style='text-align: center;'>STUDY 2 — METHODS AND DATA</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #B0BEC5; font-weight: 700;'>Input → processing → analysis → "
            "output</h3>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
### Data
| Dataset | Used for |
|---|---|
| MODIS Terra MOD13Q1 v061, 16-day, 250 m, 2010–2024 (Microsoft Planetary Computer) | NDVI and EVI outcomes; irrigation status in the revision |
| ESA WorldCover 2021 v200, 10 m | share of each land-cover class in each pixel |
| UNOSAT FL20230606UKR | flood extent; water extent before the breach |
| ERA5-Land monthly means, 2015–2024 | July–October rainfall and temperature |
| OpenStreetMap canals | Kakhovka irrigation network |
| VIINA events and territorial control, 2022–2024 | war intensity and occupation (revision) |
| Impact Observatory annual land cover, 2017–2023 | yearly water share of each pixel (revision) |
| Irrigated fields of Baber et al. (2026), 30 m, 2019–2025 (Zenodo 22036773) | irrigation exposure in the second revision (final) |
| Copernicus DEM GLO-30 | height above the river, for flood matching in the second revision |
| Sentinel-2 L2A, August 2024 | independent check of the reservoir-bed result |
| GADM v4.1 | country, oblast and district borders |

All layers are put on one equal-area grid (EPSG:3035, 231.656 m pixels, 29.0–36.5 °E × 45.3–49.3 °N).
""")

st.markdown(f"""
### Processing
- **Outcome.** Mean July–October NDVI per pixel and year, from observations flagged good or marginal, each placed in
  the season by its own acquisition day; a pixel-year needs at least five valid observations, and a pixel needs values
  in at least seven of the nine years (2016–2024).
- **Pixel universe.** Ukraine without Crimea, at least 90% valid land cover: {cnt['universe']:,} pixels.
- **Flooded land (H1).** At least half of the pixel inside UNOSAT's 6–9 June 2023 flood composite and under 20% water:
  {PM['h1']['F_px']:,} pixels ({PM['h1']['F_px'] * RES_KM2:,.0f} km²) on the two river banks;
  {PM['h1']['F_fixed_panel']:,} in the fixed panel; {m['treated_complete_pre']:,} with all six pre-war values.
- **River banks.** The Dnipro main channel was traced as a least-cost path through pre-breach water and used to
  split the land into the right bank (back under Ukrainian control from November 2022) and the occupied left bank.
- **Reservoir bed (H3).** The largest connected body of WorldCover water between the Kakhovka and Zaporizhzhia dams:
  {cnt['reservoir'] * RES_KM2:,.0f} km².
- **Canal network and zones (H2).** {LM['kakhovka_network']['segments']:,} OpenStreetMap canal segments
  ({LM['kakhovka_network']['km']:,.0f} km) connected to the reservoir. Zone K: cropland within 5 km of them
  ({cnt['zoneK']:,} pixels). Zone O: cropland more than 30 km from the reservoir and 5 km from the network.
- **Irrigated vs rainfed.** July–August NDVI at least 0.45 in three of five years 2017–2021 (irrigated) or below 0.35
  in four of them (rainfed); in the revision, the same rule on 2010–2015.
  Pre-registered groups: zone K {c2['K_irr']:,} irrigated and {c2['K_rain']:,} rainfed; zone O {c2['O_irr']:,} and
  {c2['O_rain']:,}.

### Second registered revision (final results)
Fixed in `ANALYSIS_PLAN_v2_ADDENDUM_2.md` before its data were downloaded (checksum in `v2/DEVIATIONS.md` §6).
- **Irrigation exposure from independent maps.** Share of each pixel's 30 m cells mapped as irrigated. Irrigated:
  at least half on average in 2019–2021 and within 30 km of the canals ({s2['irrigated_canal_fed']:,} pixels).
  Never irrigated: under 5% in every year and more than 5 km from any mapped field ({s2['never_irrigated']:,} pixels).
  Only {s2['irrigated_not_canal_fed']:,} irrigated pixels lie outside the canal system, so the planned triple
  difference was not run.
- **Check of the earlier NDVI rule.** Of the pixels it called irrigated, the maps show
  {share('Kherson', 'R9 irrigated (>= 50 %)'):.0f}% as irrigated in Kherson Oblast and
  {share('Zaporizhia', 'R9 irrigated (>= 50 %)'):.0f}% in Zaporizhzhia Oblast.
- **Flood matching on terrain.** Flooded pixels matched to unflooded ones on height above the river (Copernicus DEM)
  and land-cover shares, not on past NDVI: {mm['matched_treated']:,} of {mm['treated_in']:,} flooded pixels
  ({100 * mm['share_of_flooded_matched']:.0f}%) have a match; all flooded pixels are reported as well.
""")

st.markdown("""
### Analysis
Main plan and first revision; the second revision's changes are in the last point.
- **H1 flood.** Each flooded pixel matched to three unflooded pixels 2–15 km away on the same bank and land-cover
  type, by their 2016–2021 NDVI; pixel and year-by-group fixed effects; β is the change after the breach (2023–24)
  relative to 2016–2021.
- **H2 irrigation.** Triple difference: irrigated minus rainfed cropland, canal zone minus zone O, after minus before.
- **Inference.** Standard errors clustered on 10 km blocks; wild cluster bootstrap (9,999 draws); Conley errors up to
  25 km; placebo floodplains (Southern Buh, lower Dniester, Dnipro above Zaporizhzhia) and placebo oblasts or districts;
  Holm correction; relative-magnitude sensitivity bounds.
- **Decision rule (fixed in advance).** *Supported*: β < 0, Holm-adjusted bootstrap p < 0.05, placebo p < 0.10 and the
  M̄ = 1 sensitivity interval excludes zero. *Suggestive*: β < 0 with p < 0.05 but another condition fails.
  *Not supported*: otherwise.
- **H3** is a description; **H4** splits Kherson Oblast's 2021→2024 change, relative to zone O, by area.
- **Second revision.** Year effects by oblast and by occupation; rainfall and temperature allowed to act differently on
  irrigated fields; event studies against the 2016–2018 mean; 2019–2021, the years that define the irrigation groups,
  as a placebo period; wild cluster bootstrap over districts; placebo-in-time test for the flood; H4 from 2016–2018 to
  2023–2024 with 95% intervals from a block bootstrap over 10 km blocks; Sentinel-2 check of H3.
""")

st.markdown("""
### Output
`outputs/v2/study2_summary.json` (pre-registered), `outputs/v2/r1_summary.json` (registered revision),
`outputs/v2/r2_summary.json` (second registered revision, final), `outputs/v2/x1_review_diagnostics.json`
(exploratory checks) and the figures in `outputs/v2/figures/`.
Code: `v2/analysis/run_all.py`, `run_revision.py`, `run_revision2.py`, `x1_review_diagnostics.py`. Every deviation from the plans is listed
in `v2/DEVIATIONS.md`.
""")

st.info("""
### Limitations of the first two analyses, addressed in the second revision
- The NDVI-based irrigation measure, replaced by independent 30 m irrigation maps.
- Weather entering only as separate terms and 2021, the wettest summer, as reference year.
- Comparison land partly irrigated from the same canals.
- Flood matching on past NDVI.
- Clustered p-values at too small a scale; the second revision uses district clusters and placebo tests.
""")

st.warning("""
### Limitations that remain
- **Irrigation is suggestive, not supported.** The irrigated fields were already greener in 2019–2021, the years
  used to identify them, so the placebo test fails, and almost no irrigated land lies outside the canal system.
- **War and dam overlap.** The loss after 2023 cannot be fully separated from farming collapsing in an occupied,
  shelled region.
- **Summer window.** July–October NDVI misses the switch to winter crops; the irrigation maps for 2023 onwards are
  less accurate than the earlier ones.
- **Flood matches.** 41% of flooded pixels have no terrain match and are reported separately.
- **Timing.** The revisions were written after earlier results were known; they are reported beside them.
- **Data.** UNOSAT maps are preliminary; OpenStreetMap shows today's canals; VIINA is news-based; NDVI measures
  greenness only; only two seasons after the breach.
""")
