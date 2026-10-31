# ECOCIDE — What Did the Destruction of the Kakhovka Dam Do to Vegetation?

*Separating flood, reservoir and irrigation effects with satellite data*

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint%20v1%20(superseded%20results)-B7410E.svg)](https://eartharxiv.org/repository/view/14827/)

**Research question.** Which physical pathway of the Kakhovka Dam's destruction (6 June 2023) — the flood below the dam, the draining of the reservoir, or the loss of water for the irrigation canals — left a detectable mark on vegetation, when exposed land is compared with similar land in the same war zone?

The main analysis is **Study 2**: a pre-registered, pixel-level analysis of MODIS NDVI. **Study 1**, an earlier comparison of the whole of Kherson Oblast with Romanian counties, is kept as the background study that motivated it.

> **Version note.** EarthArXiv preprint v1 (5 September 2026) reports an earlier version of Study 1 (bounding-box NDVI, stacked-panel standard errors) with a significant result (−0.0703, p = 0.022). That result is superseded.

## Study 2 (main result): pre-registered, exposure-based pixel analysis

Study 2 uses 231 m MODIS pixels (2016–2024), defines treatment by physical exposure, and makes all comparisons inside the war zone. Every choice was fixed in [`ANALYSIS_PLAN_v2.md`](./docs/preregistration/ANALYSIS_PLAN_v2.md) before any data were downloaded, and in two registered revisions, each written before its extra data were downloaded ([`ADDENDUM_1`](./docs/preregistration/ANALYSIS_PLAN_v2_ADDENDUM_1.md), [`ADDENDUM_2`](./docs/preregistration/ANALYSIS_PLAN_v2_ADDENDUM_2.md)); departures are logged in [`v2/DEVIATIONS.md`](./v2/DEVIATIONS.md). Paper: [`ECO_Research_Paper_v2.md`](./docs/ECO_Research_Paper_v2.md).

| Pathway | Final result (registered revision 2, July–October NDVI) | Verdict | Earlier analyses |
|---|---|---|---|
| H1 flood: flooded vs unflooded land, same river bank | matched on terrain and land cover (59% of flooded pixels): −0.004 (95% CI −0.021 to 0.013), placebo floodplains p = 0.42; all flooded pixels +0.012 (−0.003 to 0.028) | **not supported** | plan: +0.010 / +0.006; revision 1: +0.012 / +0.055; wetlands −0.04 to −0.06 |
| H2 irrigation loss: irrigated (Baber et al. 2026 maps) vs never-irrigated cropland | −0.179 (−0.211 to −0.147), a third of the 2016–2018 level, starting with the breach; placebo test fails (+0.050 in 2019–2021) | **suggestive** | NDVI-proxy groups: −0.074 and −0.053, not attributable |
| H3 former reservoir bed (descriptive) | area with NDVI > 0.3: 86–100 km² each year 2016–2022 → 906 km² (2023) → 1,574 km² (2024); Sentinel-2 within 18% of MODIS | — | — |
| H4 Kherson Oblast, 2016–18 → 2023–24 vs comparison area | −0.020 (−0.025 to −0.015); irrigated cropland (4% of area) −0.008; never-irrigated cropland 0.000; flood 0.000 | — | 2021→2024: −0.029, reservoir bed +0.010 |

The NDVI-based irrigation proxy used in the plan and revision 1 agreed with the independent maps on only 16% of its "irrigated" pixels in Kherson Oblast. All numbers: `outputs/v2/study2_summary.json`, `r1_summary.json`, `r2_summary.json`; figures: `outputs/v2/figures/`.

## Live dashboard

**[ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app](https://ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app/)** — numbers are read from `outputs/v2/study2_summary.json`, `r1_summary.json`, `r2_summary.json` and `x1_review_diagnostics.json` (Study 2) and `outputs/model_results.json` (Study 1).

## Documents

| Document | Contents |
|---|---|
| [`ECO_Research_Paper_v2.md`](./docs/ECO_Research_Paper_v2.md) · [PDF](./docs/ECO_Research_Paper_v2.pdf) | **Main paper (Study 2)**: question, data, methods, results, limitations |
| [`ECO_Executive_Summary.md`](./docs/ECO_Executive_Summary.md) · [PDF](./docs/ECO_Executive_Summary.pdf) | Two-page summary of Study 2 |
| [`ANALYSIS_PLAN_v2.md`](./docs/preregistration/ANALYSIS_PLAN_v2.md), [`ADDENDUM_1`](./docs/preregistration/ANALYSIS_PLAN_v2_ADDENDUM_1.md), [`ADDENDUM_2`](./docs/preregistration/ANALYSIS_PLAN_v2_ADDENDUM_2.md), [`v2/DEVIATIONS.md`](./v2/DEVIATIONS.md) | Pre-registered plan, two registered revisions, and every deviation |
| [`RESEARCH_COMPLETION_PLAN.md`](./docs/preregistration/RESEARCH_COMPLETION_PLAN.md) | The bounded plan for the second revision and its stopping rules |
| [`ECO_Research_Paper.md`](./docs/ECO_Research_Paper.md) · [PDF](./docs/ECO_Research_Paper.pdf) | Study 1 paper (background study: Kherson Oblast vs Romanian counties) |
| [`ECO_RESULTS_RECONCILIATION.md`](./docs/ECO_RESULTS_RECONCILIATION.md) | Every headline number, old vs current, and which script produces it |
| [`ECO_Development_Log.md`](./docs/ECO_Development_Log.md) · [PDF](./docs/ECO_Development_Log.pdf) | Chronological research diary (historical entries describe the state at that time) |
| [`ECO_Declarations.pdf`](./docs/ECO_Declarations.pdf) | Declarations: authorship, funding, pre-registration and deviations, data and licences, earlier versions, use of AI tools |

## Study 1 (background): Kherson Oblast vs Romanian counties

Monthly Sentinel-2 NDVI, January 2022 – November 2024, over each zone's GADM polygon on a common 0.002° grid, with cloud, shadow, cirrus, snow and water masked and each pixel's monthly median over all clear acquisitions (`data/ndvi_v3`). Effects are estimated on the monthly treated-minus-control NDVI gap, with Newey-West HAC standard errors (maxlags = 3, t-distribution).

| Check | Result |
|---|---|
| Primary DiD, Kherson vs Tulcea | −0.108, 95% CI [−0.209, −0.007], p = 0.037 |
| Same, zone-specific seasonality | −0.069, 95% CI [−0.116, −0.023], p = 0.005 |
| Placebo, fake date June 2022 | +0.012, p = 0.802 — clean |
| Narrowed baseline (from Jan 2023) | −0.186, p = 0.001, but its own placebo is also significant (p = 0.004) |
| Kherson vs mean of four Romanian controls | −0.071, p = 0.022 (−0.060, p = 0.004 with seasonality) |
| Per control: Tulcea / Galați / Brăila / Constanța | −0.108 (p = 0.037) / −0.077 (0.007) / −0.101 (0.003) / +0.001 (0.98) |
| Placebo in space (5 units) | Kherson ranks 2/5 (exact p = 0.40); Constanța shifts by as much (−0.073 vs −0.071) |
| Event study | 4 of 5 pre-event quarters deviate; the summer–autumn gap deepens from 2022/2023 to 2024 |
| HAC lags 1–6 / log NDVI | p = 0.010–0.042 / −25%, p = 0.030 |

Kherson's NDVI declined relative to comparable unaffected regions after June 2023, robustly to seasonality and specification. The design does not attribute that decline to the dam: one control county shifts by as much, pre-event quarters already deviate, and the oblast-wide unit mixes flooding, reservoir drainage, irrigation loss and war effects. Study 2 was designed to separate them.

**Flood extent (descriptive).** UNOSAT's FL20230606UKR layers map the downstream flood with different sensors: 122.5 km² (6 June, Sentinel-3), 520.8 km² (7 June, ICEYE), 260.9 km² (8 June, Sentinel-2), 464.2 km² (9 June, Sentinel-3), 179.9 km² (13 June, Sentinel-2, 55% of the analysis area cloud-obscured), 21.2 km² (21 June, Sentinel-1); UNOSAT's cumulative 6–9 June composite is 617 km². These are separate preliminary observations, not one continuous series.

## Reproduce

```bash
git clone https://github.com/sakshimaske303-commits/ECOCIDE.git
cd ECOCIDE
pip install -r requirements.txt

# Boundaries (GADM may not be redistributed, so they are downloaded, not stored here)
python src/download_gadm.py
python src/extract_boundaries.py && python src/extract_control_zone_boundaries.py && python src/export_zone_geometries.py

# Study 2 (main): first the downloads in v2/README_v2.md, then
pip install -r v2/requirements_v2.txt
python v2/analysis/run_all.py                 # pre-registered analysis -> outputs/v2/study2_summary.json
python v2/analysis/run_revision.py            # registered revision     -> outputs/v2/r1_summary.json
python v2/analysis/x1_review_diagnostics.py   # exploratory checks      -> outputs/v2/x1_review_diagnostics.json
# Registered Revision 2: downloads v2/09-11, then (see v2/README_v2.md)
python v2/analysis/run_revision2.py           # -> outputs/v2/r2_summary.json
python tests/test_v2lib.py                    # checks of the estimation engine
python tests/test_r2lib.py                    # checks of the Revision 2 helpers and the addendum checksum

# Study 1 (background)
python src/generate_model_results.py  # all statistics -> outputs/model_results.json (reads data/ndvi_v3)
python src/flood_progression.py       # UNOSAT areas  -> outputs/flood_extent_table.csv
python src/build_all_figures.py       # every Study 1 figure -> outputs/plots

cd dashboard && streamlit run app.py
```

All commands run from the repository root. Individual Study 1 scripts in `src/` (`did_model.py`, `placebo_test.py`, `event_study.py`, `placebo_in_space_test.py`, …) print the same numbers; all use the shared engine `src/eco_core.py`.

**Study 1 NDVI versions.** `data/ndvi_v3` (current, `src/download_ndvi_polygon_v3.py`): polygon, common 0.002° grid, cloud/shadow/cirrus/snow/water masked, per-pixel monthly median. `data/ndvi_v2` (`src/download_ndvi_polygon.py`): polygon, default 256 × 256 sampling grid, water not masked, single scene per month. `data/ndvi_old_bbox`: original bounding-box extraction. Any version can be analysed with `ECO_NDVI_DIR=<folder> python src/generate_model_results.py`. Re-extraction needs Sentinel Hub credentials in `.env` (see `.env.example`).

## Repository structure

```text
ECOCIDE/
├── docs/                        # papers, executive summary, development log, declarations, results reconciliation
│   └── preregistration/         # analysis plan, two registered revisions, completion plan
├── v2/                          # Study 2
│   ├── 00–11_*.py               # data download and preparation (MODIS, WorldCover, ERA5-Land, OSM, IO land cover, VIINA, irrigation maps, DEM, Sentinel-2)
│   ├── grid.py                  # common EPSG:3035 231.656 m grid
│   ├── DEVIATIONS.md, README_v2.md
│   └── analysis/                # a1–a8 (plan), r1_* (revision 1), r2_* (revision 2), x1 (exploratory checks), v2lib.py (engine)
├── tests/                       # checks of the Study 2 engine and the Revision 2 helpers
├── src/                         # Study 1 and shared scripts (see src/README.md)
│   ├── eco_core.py              # Study 1 estimation engine (gap-series DiD, HAC, event study)
│   ├── eco_flood.py, eco_style.py   # UNOSAT layer definitions, figure style (also used by Study 2 figures)
│   ├── generate_model_results.py    # runs every Study 1 model -> outputs/model_results.json
│   ├── did_model*.py, placebo*.py, event_study*.py, …   # individual Study 1 checks (thin wrappers on eco_core)
│   ├── map*.py, build_*.py      # Study 1 figures, interactive plots, flood web map, figure PDF
│   └── download_*.py, extract_*.py   # GADM boundaries and Study 1 Sentinel-2 downloads
├── data/                        # boundaries, Study 1 NDVI, UNOSAT zip, small Study 2 inputs (large ones are regenerated)
├── outputs/                     # model_results.json, flood table, plots, maps; outputs/v2 for Study 2
├── dashboard/                   # Streamlit app
└── archive/                     # early NDWI/SAR exploration and one-off checks, not used in any result (see archive/README.md)
```

## Data sources

| Dataset | Provider |
|---|---|
| NDVI and EVI, 250 m, 2010–2024 (Study 2) | MODIS Terra MOD13Q1 v061 (NASA LP DAAC), via Microsoft Planetary Computer |
| Land cover | ESA WorldCover 2021 v200; Impact Observatory annual land cover 2017–2023 |
| Weather | ERA5-Land monthly means (Copernicus Climate Data Store) |
| Irrigated fields, 30 m, 2019–2025 (Study 2, second revision) | Baber et al. (2026), Zenodo record 22036773, CC BY 4.0 |
| Elevation (Study 2, second revision) | Copernicus DEM GLO-30, via Microsoft Planetary Computer |
| Sentinel-2 check of the reservoir bed (Study 2, second revision) | Copernicus Sentinel-2 L2A, August 2024, via Microsoft Planetary Computer |
| Irrigation canals | © OpenStreetMap contributors, Open Database License (ODbL 1.0); the extract in `data/v2` is a derived database under the same licence |
| War events and territorial control | VIINA (Zhukov, 2023) |
| Flood extent | UNITAR/UNOSAT, FL20230606UKR (Sentinel-1, Sentinel-2, Sentinel-3, ICEYE layers; preliminary) |
| NDVI and true-colour imagery (Study 1) | Copernicus Sentinel-2 L2A via Sentinel Hub (Copernicus Data Space Ecosystem) |
| Administrative boundaries | GADM v4.1 (academic and non-commercial use; not redistributed here — `src/download_gadm.py`) |

## Declarations

Read the full statement in [`ECO_Declarations.pdf`](./docs/ECO_Declarations.pdf) (source: [`ECO_Declarations.md`](./docs/ECO_Declarations.md)). In short:

- **Who did the work:** one author, who planned, coded, ran, checked and wrote up every part of it.
- **Money and interests:** no external funding, no competing interests.
- **Ethics:** satellite and public data only; no participants or personal data.
- **Pre-registration:** the main plan was public before any data were downloaded; both revisions were written before their extra data were collected, and every departure is in `v2/DEVIATIONS.md`.
- **AI tools:** Alongside the external reviews of the project, I also used Claude (Anthropic), an AI assistant, for smaller and more routine tasks. I gave it the paper, summaries, README and dashboard text to compare against the JSON result files of the main plan and both revisions, so that a flood estimate, an irrigation coefficient or a verdict quoted in one place matched the others. I sometimes turned to it when a download or estimation script stopped with an error I could not trace, and I used it for the layout of the project web pages. The writing is mine: I asked it to point out passages that were unclear or too technical, places where something seemed missing, and punctuation, and I chose which of those suggestions to take. It had no part in writing the analysis plans, choosing the exposed and comparison groups, setting the decision rule or naming any result. It did not fetch or process the satellite data, and it did not run the models. Every suggestion was checked by me before I used it, and I am responsible for all of the content.

## Author and licence

Sakshi D. Maske, independent geospatial researcher. Code: [MIT](./LICENSE). Text, papers, figures and derived results: [CC BY 4.0](./LICENSE-CC-BY-4.0). Third-party data keep the licences listed above.
