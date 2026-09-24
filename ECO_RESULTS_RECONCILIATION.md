# ECOCIDE — Results Reconciliation (current-state manifest)

Every headline number in the paper, README, executive summary, CITATION.cff and dashboard is produced by `generate_model_results.py` and stored in `outputs/model_results.json`. The dashboard reads that file directly; the documents quote it. If the data change, re-run `generate_model_results.py` and `build_all_figures.py`, then update the documents from the JSON.

## Four versions of the analysis

| Version | NDVI extraction | Inference | Where it appears |
|---|---|---|---|
| A — original | Bounding box, scene-level cloud filter (`data/ndvi_old_bbox`) | Stacked OLS, HAC on row order, normal dist. | EarthArXiv preprint v1, Zenodo v1.0.0 |
| B — Phase 2 | GADM polygon + pixel SCL mask, default 256 × 256 grid, water kept, single scene (`data/ndvi` = `data/ndvi_v2`) | Stacked OLS, HAC on row order, t dist. (external script) | Repo drafts, 11–23 Sept 2026 |
| C — inference fix | Same data as B | Monthly gap series, HAC maxlags 3, t dist. (`eco_core.py`) | Repo, 24 Sept 2026 (morning) |
| **D — current** | **Polygon, common 0.002° grid, cloud/shadow/cirrus/snow/water masked, per-pixel monthly median (`data/ndvi_v3`)** | **Same as C** | **Everything in this repo now** |

## Headline numbers

| Quantity | A | B | C | **D (current)** | JSON key |
|---|---|---|---|---|---|
| Primary DiD, Kherson vs Tulcea | −0.0703, p = 0.022 | −0.0747, p = 0.060 | −0.0747, p = 0.162 | **−0.1082, CI [−0.209, −0.007], p = 0.037** | `main_did` |
| + zone-specific seasonality | — | — | −0.0324, p = 0.160 | **−0.0694, p = 0.005** | `main_did_seasonal` |
| Placebo, fake date Jun 2022 | +0.0148, p = 0.612 | +0.0051, p = 0.882 | +0.0051, p = 0.914 | **+0.0116, p = 0.802** | `placebo_broad` |
| Narrowed baseline DiD | −0.1384, p = 0.0001 | −0.1497, p = 0.0004 | −0.1497, p = 0.007 | **−0.1858, p = 0.001** | `narrowed_did` |
| Narrowed placebo | −0.1382, p = 0.001 | −0.1098, p = 0.069 | −0.1098, p = 0.018 | **−0.1025, p = 0.004 (fails)** | `placebo_narrowed` |
| Pooled four-county DiD | −0.0600, p = 0.029 | −0.0661, p = 0.059 | −0.0661, p = 0.102 | **−0.0714, p = 0.022** | `pooled_did` |
| Pooled + seasonality | — | — | −0.0478, p = 0.034 | **−0.0597, p = 0.004** | `pooled_did_seasonal` |
| Pooled placebo | +0.0222, p = 0.484 | +0.0421, p = 0.338 | +0.0421, p = 0.314 | **+0.0313, p = 0.223** | `pooled_placebo` |
| Kherson vs Galați / Brăila / Constanța | −0.0695 / −0.0937 / −0.0064 | −0.081 / −0.128 / +0.019 | same, p 0.069 / 0.030 / 0.648 | **−0.077 (0.007) / −0.101 (0.003) / +0.001 (0.98)** | `per_control` |
| Placebo in space, Kherson rank | 1/5 | 2/5, 3/5 | 2/5, 3/5 | **2/5 one- and two-sided (p = 0.40)** | `placebo_in_space` |
| Control-only divergence T / G / B / C (p) | 0.64 / 0.69 / 0.069 / 0.033 | 0.742 / 0.567 / 0.027 / 0.020 | 0.746 / 0.308 / 0.014 / 0.051 | **0.176 / 0.634 / 0.045 / 0.084** | `control_divergence` |
| Pre-event quarters significant (of 5) | 1 reported | 1 reported | 3 | **4** | `event_study` |
| HAC lag 1–6, p range | 0.011–0.026 | 0.027–0.063 | 0.091–0.170 | **0.010–0.042** | `lag_sensitivity` |
| log(NDVI) | −0.49, p = 0.055 | −0.25, p = 0.081 | −0.25, p = 0.197 | **−0.29 (≈ −25%), p = 0.030** | `log_ndvi` |

Versions B and C differ only in standard errors (same point estimates). Versions C and D differ only in the NDVI data.

## Flood-extent numbers (UNOSAT FL20230606UKR, `flood_progression.py` → `outputs/flood_extent_table.csv`)

| Date | Sensor | Area km² | In Kherson Oblast km² | Analysis extent km² |
|---|---|---|---|---|
| 6 June | Sentinel-3 | 122.50 | 122.50 | 18,751 (278 km² cloud) |
| 7 June | ICEYE | 520.77 | 494.66 | 2,098 |
| 8 June | Sentinel-2 | 260.92 | 220.05 | 18,751 |
| 9 June | Sentinel-3 | 464.18 | 439.25 | 18,751 |
| 13 June | Sentinel-2 | 179.92 | 164.80 | 11,031 (6,055 km² cloud) |
| 21 June | Sentinel-1 | 21.17 | 15.95 | 10,788 |
| 6–9 June composite | multi-sensor | 617.00 | 563.99 | — |

Earlier versions attributed all dates to "ICEYE, Landsat-9, SkySat, WorldView-3, MODIS" and called 9 June the peak; both were wrong for these layers. The "~10,800 km² corridor" once quoted on the dashboard matches the 21 June Sentinel-1 analysis extent, not an independent estimate.

## Still outside this repository

- EarthArXiv preprint v1 and Zenodo v1.0.0 show version A. Post a new EarthArXiv version and a new Zenodo release once the paper is final.
- Sentinel Hub / CDSE credentials were once committed (`.env`, `.env.txt`); rotate them.
