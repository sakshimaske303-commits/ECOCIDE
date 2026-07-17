# 🛰️ ECOCIDE — A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes

**Isolating conflict-attributable environmental damage from pre-existing trends, using causal inference rather than qualitative interpretation.**

## 🔗 Live Dashboard

**[View the interactive dashboard →](https://your-ecocide-app.streamlit.app/)**

## 📄 Project Documentation

| Document | What's Inside |
|---|---|
| 📘 [`Project_Journal.md`](./Project_Journal.md) | Polished project summary — methodology, findings, conclusions (start here) |
| 📗 [`Research_Paper.md`](./Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| 📙 [`Devlopment_Log.md`](./Devlopment_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

ECOCIDE is a geospatial causal-inference framework built to independently verify claims of environmental destruction arising from armed conflict, using Earth Observation data and rigorous causal-inference methods. As international legal bodies move toward formally recognizing "ecocide" as a prosecutable international crime, this project addresses a specific, acknowledged gap: existing satellite-based assessments of war-related environmental damage rely on qualitative, visual interpretation and explicitly decline to establish statistical causality. ECOCIDE fills that gap, applying a Difference-in-Differences framework — validated through placebo testing and event-study analysis — to the destruction of Ukraine's Kakhovka Dam.

---

Interactive geospatial map hosted separately via GitHub Pages and embedded live in the dashboard: **[View the interactive flood-extent map →](https://sakshimaske303-commits.github.io/ECOCIDE/dashboard/static/kherson_flood_extent_webmap/index.html)**

---

## 📊 What This Project Does

- Tests whether the Kakhovka Dam's destruction (6 June 2023) produced a statistically significant environmental effect, isolated from Ukraine's broader, already-elevated conflict baseline
- Uses a matched non-conflict control zone (Danube Delta, Romania) rather than a simple before-after comparison
- Validates every result through placebo testing (fake treatment dates) and quarterly event-study analysis
- Sources verified, multi-sensor flood-extent data (UNOSAT) rather than independently deriving flood detection from noisy raw satellite bands
- Presents before/after true-color satellite imagery, acquired programmatically for full reproducibility
- Transparently discloses a genuine methodological limitation discovered during validation, rather than concealing it

## 🔬 Key Findings

**A statistically significant, causally-validated NDVI decline was detected.** Comparing Kherson (treatment) against Tulcea, Romania (control), a Difference-in-Differences model found a coefficient of −0.0703 (p = 0.007), confirmed through a clean placebo test using a counterfactual pre-event date (p = 0.741, near-zero coefficient).

**A genuine complication was found and reported honestly.** A quarterly event study revealed a significant effect in a pre-treatment quarter — traced to Kherson already being an active conflict zone before the dam's destruction. Rather than concealing this, it is disclosed transparently as a limitation on a narrowed-baseline sensitivity analysis, while the primary, cleanly-validated result stands independently.

**Verified flood data confirms a complete hydrograph.** UNOSAT's multi-sensor flood-extent data shows a full rise-peak-recession cycle: 122.50 km² (6 June) → 464.18 km² peak (9 June) → 21.17 km² (21 June).

Full methodology, including every debugging decision and disclosed limitation, is documented in the dashboard's Methodology page and in `Project_Journal.md`.

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
├── Project_Journal.md               # Polished project summary and methodology
├── Research_Paper.md                # Formal academic research paper
├── Devlopment_Log.md                # Full technical development log
├── download_*.py                    # Dataset acquisition scripts
├── did_model*.py / event_study.py   # Causal inference scripts
├── map*.py                          # Static visualization scripts
└── requirements.txt
```

## 🛠️ Tech Stack

Python · GeoPandas · Rasterio · Statsmodels · Plotly · Streamlit · QGIS · QGIS2Web · GitHub Pages · Sentinel Hub API · UNOSAT

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

---

*This project's full development process — including every debugging session, methodology iteration, and disclosed limitation — is documented in `Devlopment_Log.md` for full transparency and reproducibility.*