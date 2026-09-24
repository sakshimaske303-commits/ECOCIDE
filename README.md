# ECOCIDE — Satellite Evidence and Causal-Inference Testing of the Kakhovka Dam Destruction

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint%20v1%20(superseded%20results)-B7410E.svg)](https://eartharxiv.org/repository/view/14827/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21757974.svg)](https://doi.org/10.5281/zenodo.21757974)

**Can a Difference-in-Differences design separate the vegetation impact of the Kakhovka Dam's destruction (6 June 2023) from background change in comparable, unaffected regions?** Kherson's vegetation did decline significantly relative to its controls after June 2023 — but the design cannot attribute that decline to the dam.

> **Version note.** EarthArXiv preprint v1 (5 September 2026) and Zenodo v1.0.0 report an earlier analysis (bounding-box NDVI, stacked-panel standard errors) with a significant result (−0.0703, p = 0.022). That result is superseded. The numbers below come from the third, corrected NDVI extraction (`data/ndvi_v3`) and the code in this repository.

## Study 2 (main result): pre-registered, exposure-based pixel analysis

Study 2 replaces the oblast-versus-Romania design with 231 m MODIS pixels (2016–2024), treatment defined by physical exposure, and comparisons inside the war zone. Every choice was fixed in [`ANALYSIS_PLAN_v2.md`](./ANALYSIS_PLAN_v2.md) before the analysis; departures are logged in [`v2/DEVIATIONS.md`](./v2/DEVIATIONS.md). Paper: [`ECO_Research_Paper_v2.md`](./ECO_Research_Paper_v2.md). Reproduce: `python v2/analysis/run_all.py` (after the download steps in [`v2/README_v2.md`](./v2/README_v2.md)).

| Hypothesis | Estimate (July–October NDVI) | Pre-registered verdict |
|---|---|---|
| H1 flood: flooded vs matched unflooded land, same bank | +0.006 (95% CI −0.014 to 0.026); wild-bootstrap p = 0.60; placebo floodplains p = 0.63 | **not supported** (wetlands: −0.04) |
| H2 irrigation loss: irrigated vs rainfed, canal zone vs elsewhere | −0.074 (−0.088 to −0.060); wild-bootstrap p < 0.001; placebo zones p = 0.14 (minimum attainable); strong pre-trends | **suggestive** |
| H3 former reservoir bed (descriptive) | area with NDVI > 0.3: ~95 km² (2016–22) → 906 km² (2023) → 1,574 km² (2024) | — |
| H4 decomposition of Kherson's 2021→24 change vs zone O (−0.029) | other land −0.024, irrigated canal zone −0.013, flood −0.0004, reservoir bed +0.010 | — |

All Study 2 numbers: `outputs/v2/study2_summary.json`; figures: `outputs/v2/figures/`. The Study 1 results below are kept as the administrative-unit analysis that motivated Study 2.

## Live dashboard

**[ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app](https://ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app/)** — every number on it is read from `outputs/model_results.json`.

## Documents

| Document | Contents |
|---|---|
| [`ECO_Research_Paper.md`](./ECO_Research_Paper.md) | Full paper: literature, data, methods, results, limitations |
| [`ECO_Executive_Summary.md`](./ECO_Executive_Summary.md) | Two-page summary |
| [`ECO_RESULTS_RECONCILIATION.md`](./ECO_RESULTS_RECONCILIATION.md) | Every headline number, old vs current, and which script produces it |
| [`ECO_Development_Log.md`](./ECO_Development_Log.md) | Chronological research diary (historical entries describe the state at that time) |
| [`ECOCIDE_Maps_and_Plots.pdf`](./ECOCIDE_Maps_and_Plots.pdf) | All figures with captions |

## Key findings (current code and data)

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

Taken together: Kherson's NDVI declined relative to comparable unaffected regions after June 2023, robustly to seasonality and specification, most strongly in the 2024 growing season. The design does not attribute that decline to the dam: one control county shifts by as much, pre-event quarters already deviate, and the oblast-wide unit mixes flooding, reservoir drainage and war effects.

**Flood extent (descriptive).** UNOSAT's FL20230606UKR layers map the downstream flood with different sensors: 122.5 km² (6 June, Sentinel-3), 520.8 km² (7 June, ICEYE), 260.9 km² (8 June, Sentinel-2), 464.2 km² (9 June, Sentinel-3), 179.9 km² (13 June, Sentinel-2, 55% of the analysis area cloud-obscured), 21.2 km² (21 June, Sentinel-1); UNOSAT's cumulative 6–9 June composite is 617 km². These are separate preliminary observations, not one continuous series.

## Reproduce

```bash
git clone https://github.com/sakshimaske303-commits/ECOCIDE.git
cd ECOCIDE
pip install -r requirements.txt
python generate_model_results.py      # all statistics -> outputs/model_results.json (reads data/ndvi_v3)
python flood_progression.py           # UNOSAT areas  -> outputs/flood_extent_table.csv
python build_all_figures.py           # every static + interactive figure and the figure PDF
cd dashboard && streamlit run app.py
```

Individual scripts (`did_model.py`, `placebo_test.py`, `event_study.py`, `placebo_in_space_test.py`, …) print the same numbers; all use the shared engine in `eco_core.py`.

**NDVI versions.** `data/ndvi_v3` (current, `download_ndvi_polygon_v3.py`): polygon, common 0.002° grid, cloud/shadow/cirrus/snow/water masked, per-pixel monthly median. `data/ndvi` = `data/ndvi_v2` (`download_ndvi_polygon.py`): polygon, default 256 × 256 sampling grid, water not masked, single scene per month. `data/ndvi_old_bbox`: original bounding-box extraction. Any version can be analysed with `ECO_NDVI_DIR=<folder> python generate_model_results.py`. Re-extraction needs Sentinel Hub credentials in `.env` (see `.env.example`).

## Repository structure

```text
ECOCIDE/
├── eco_core.py                  # shared estimation engine (gap-series DiD, HAC, event study)
├── eco_flood.py / eco_style.py  # UNOSAT layer definitions / figure style
├── generate_model_results.py    # runs every model -> outputs/model_results.json
├── build_all_figures.py         # regenerates all figures
├── did_model*.py, placebo*.py, event_study*.py, placebo_in_space_test.py,
│   control_only_spillover_check.py, specification_robustness_check.py,
│   low_coverage_month_check.py  # individual checks (thin wrappers on eco_core)
├── map*.py, build_*.py          # figures, interactive plots, folium map, figure PDF
├── download_*.py                # data acquisition (Sentinel Hub)
├── data/                        # boundaries, NDVI (ndvi_v3 current; ndvi, ndvi_v2, ndvi_old_bbox earlier), UNOSAT zip
├── outputs/                     # model_results.json, flood table, plots, maps
└── dashboard/                   # Streamlit app (reads outputs/model_results.json)
```

## Data sources

| Dataset | Provider |
|---|---|
| NDVI, true-colour imagery | Copernicus Sentinel-2 L2A via Sentinel Hub (Copernicus Data Space Ecosystem) |
| Flood extent | UNITAR/UNOSAT, FL20230606UKR (Sentinel-1, Sentinel-2, Sentinel-3, ICEYE layers; preliminary) |
| Administrative boundaries | GADM v4.1 |

## Author and licence

Sakshi D. Maske, independent geospatial researcher. Licensed under [CC BY 4.0](./LICENSE).
