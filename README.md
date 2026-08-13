# 🛰️ ECOCIDE — A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21757974.svg)](https://doi.org/10.5281/zenodo.21757974)

**Isolating conflict-attributable environmental damage from pre-existing trends, using causal inference rather than qualitative interpretation.**

## 🔗 Live Dashboard

**[View the interactive dashboard →](https://ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app/)**

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| ⚡ [`ECO_Executive_Summary.pdf`](./ECO_Executive_Summary.pdf) | One-page snapshot — question, method, headline finding, robustness checklist, and links (fastest overview) |
| 📘 [`ECO_Project_Report.md`](./ECO_Project_Report.md) | Polished project summary — methodology, findings, conclusions (start here) |
| 📗 [`ECO_Research_Paper.md`](./ECO_Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| 📙 [`ECO_Development_Log.md`](./ECO_Development_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

ECOCIDE is a geospatial causal-inference framework built to independently verify claims of environmental destruction arising from armed conflict, using Earth Observation data and rigorous causal-inference methods — "independent" here means independent of official government reporting from any party, not independent of all human judgment; the analysis itself is built on publicly available, third-party-processed satellite products (Sentinel Hub, UNOSAT), and the full pipeline is open for scrutiny. As international legal bodies move toward formally recognizing "ecocide" as a prosecutable international crime, this project addresses a specific, acknowledged gap: existing satellite-based assessments of war-related environmental damage rely on qualitative, visual interpretation and explicitly decline to establish statistical causality. ECOCIDE fills that gap, applying a Difference-in-Differences framework — validated through placebo testing and event-study analysis — to the destruction of Ukraine's Kakhovka Dam.

---

Interactive geospatial map hosted separately via GitHub Pages and embedded live in the dashboard: **[View the interactive flood-extent map →](https://sakshimaske303-commits.github.io/ECOCIDE/dashboard/static/kherson_flood_extent_webmap/index.html)**

---

## 📊 What This Project Does

- Tests whether the Kakhovka Dam's destruction (6 June 2023) produced a statistically significant environmental effect, isolated from Ukraine's broader, already-elevated conflict baseline
- Uses a four-county Danube/Black Sea Romanian control panel (Tulcea, Galați, Brăila, Constanța) rather than a simple before-after comparison
- Validates every result through placebo testing (fake treatment dates) and quarterly event-study analysis
- Sources verified, multi-sensor flood-extent data (UNOSAT) rather than independently deriving flood detection from noisy raw satellite bands
- Presents before/after true-color satellite imagery, acquired programmatically for full reproducibility
- Transparently discloses a genuine methodological limitation discovered during validation, rather than concealing it

## 🔬 Key Findings

**A statistically significant, causally-validated NDVI decline was detected.** The primary specification compares Kherson (treatment) against Tulcea, Romania (control): a Difference-in-Differences model finds a coefficient of −0.0703 (95% CI [−0.130, −0.010], HAC-robust p = 0.022), confirmed through a clean placebo test using a counterfactual pre-event date (p = 0.612, near-zero coefficient). Standard errors use the Newey-West HAC correction rather than clustering, since this two-unit (treatment/control) design has too few clusters for cluster-robust inference to apply.

**The same model was also run as a robustness check against the full four-county control panel, and the effect held.** Tulcea sits alongside three other Danube/Black Sea Romanian counties — Galați, Brăila, Constanța — chosen for comparable pre-conflict ecology (river-delta wetland, steppe, agricultural floodplain, coastal) while being genuinely non-combatant. Pooled across all four, the effect stands: −0.0600 (HAC p = 0.029, 95% CI [−0.114, −0.006]; cluster-robust p = 0.002, 95% CI [−0.097, −0.023]). Tested individually, three of the four controls (Tulcea, Galați, Brăila) each independently reproduce a significant effect close to the primary-specification magnitude; the fourth, Constanța — the most purely coastal, most urbanized of the four — does not, and that's reported as an open question rather than smoothed over. A placebo test on the four-county panel comes back clean (+0.0222, p = 0.216, wrong sign).

**A genuine complication was found and reported honestly.** A quarterly event study on the two-zone (Kherson/Tulcea) specification revealed a significant effect in a pre-treatment quarter — traced to Kherson already being an active conflict zone before the dam's destruction. A narrowed-baseline sensitivity analysis built to address this produces a larger effect, but its own placebo test fails once the correct HAC standard errors are applied — a genuine validation failure, disclosed as such rather than downplayed, while the primary, cleanly-validated broader-baseline result stands independently. Running the same quarterly event study on the four-county panel surfaces an intrinsic property of a 5-cluster design (1 treatment + 4 control) against roughly 24 model parameters: cluster-robust standard errors become rank-deficient (rank 4, not 24) — numerically degenerate rather than genuinely precise — so HAC is reported for that specific model instead, where the exact-treatment-quarter effect is not significant (p = 0.972, versus p = 0.005 in the two-zone-only event study), though the quarter-plus-4 effect remains significant (p = 0.011).

**Verified flood data confirms a complete hydrograph.** UNOSAT's multi-sensor flood-extent data shows a full rise-peak-recession cycle: 122.50 km² (6 June) → 464.18 km² peak (9 June) → 21.17 km² (21 June).

Full methodology, including every debugging decision and disclosed limitation, is documented in the dashboard's Methodology page and in `ECO_Project_Report.md`.

## 🏗️ Architecture

```text
Satellite APIs (Sentinel Hub, UNOSAT)
        │
        ▼
Acquisition scripts (download_*.py, auth_sentinelhub.py)
        │
        ▼
Preprocessing (NDVI/NDWI extraction, boundary clipping, GADM matching)
        │
        ▼
Causal models (did_model.py, placebo_test.py, event_study.py — HAC-robust SEs)
        │
        ▼
Static figures (map*.py) ──► ECO_Research_Paper.md / ECO_Development_Log.md
        │
        ▼
Streamlit dashboard (dashboard/app.py + 8 pages) ──► Zenodo DOI
```

## 🗂️ Repository Structure

```text
ECOCIDE/
├── dashboard/                       # Streamlit dashboard (8 pages)
│   └── static/                      # QGIS2Web interactive map export (served via GitHub Pages)
├── data/
│   ├── boundaries/, ndvi/, ndwi/
│   └── satellite_imagery/           # Before/after true-color imagery
├── outputs/
│   └── plots/                       # Static visualizations (hydrograph, event study, etc.)
├── qgis_processing/                 # Original QGIS2Web webmap export
├── ECO_Project_Report.md            # Polished project summary and methodology
├── ECO_Research_Paper.md            # Formal academic research paper
├── ECO_Development_Log.md           # Full technical development log
├── download_*.py                    # Dataset acquisition scripts
├── did_model*.py / event_study.py   # Causal inference scripts
├── map*.py                          # Static visualization scripts
└── requirements.txt
```

## 🛠️ Tech Stack

Python · GeoPandas · Matplotlib · Statsmodels · Streamlit · QGIS · QGIS2Web · GitHub Pages · Sentinel Hub API · UNOSAT

## 📚 Data Sources

| Dataset | Provider |
|---|---|
| NDVI, True-Color Imagery | Sentinel-2, Sentinel Hub (Copernicus Data Space Ecosystem) |
| Verified Flood Extent | UNOSAT (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS) |
| Administrative Boundaries | GADM v4.1 |

## ▶️ Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/ECOCIDE.git
cd ECOCIDE
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

## 👤 Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## 📜 License

This project is licensed under [CC BY 4.0](./LICENSE) — you are free to share and adapt this work for any purpose, including commercially, with attribution.

---

*This project's full development process — including every debugging session, methodology iteration, and disclosed limitation — is documented in `ECO_Development_Log.md` for full transparency and reproducibility.*