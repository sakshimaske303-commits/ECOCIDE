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
RES_KM2 = (231.656358 / 1000) ** 2
cnt = LM["counts_px"]
m = H1R["matching"]
c2 = H2R["main"]["counts"]

st.markdown("<h1 style='text-align: center;'>🧭 STUDY 2 — METHODS AND DATA</h1>", unsafe_allow_html=True)
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
""")

st.markdown("""
### Analysis
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
""")

st.markdown("""
### Output
`outputs/v2/study2_summary.json` (pre-registered), `outputs/v2/r1_summary.json` (registered revision),
`outputs/v2/x1_review_diagnostics.json` (exploratory checks) and the figures in `outputs/v2/figures/`.
Code: `v2/analysis/run_all.py`, `run_revision.py`, `x1_review_diagnostics.py`. Every deviation from the plans is listed
in `v2/DEVIATIONS.md`.
""")

st.warning("""
### Main limitations
- **Irrigation measure.** "Irrigated" is defined from NDVI and mostly captures summer crops.
- **Weather and reference year.** Weather enters the models only as separate terms; the reference year 2021 was the
  wettest summer of the record.
- **Exposed comparison land.** Irrigated land more than 5 km from the mapped canals counts as comparison land.
- **Small matched flood samples.** Matched on pre-war NDVI, so their flat pre-trends are expected and regression to
  the mean is possible.
- **Scale of inference.** The canal zone and the flood are each one connected area; the placebo tests are a better
  guide than the very small clustered p-values.
- **Data.** UNOSAT maps are preliminary; OpenStreetMap shows today's canals; VIINA is news-based; NDVI measures
  greenness only; only two seasons after the breach.
""")
