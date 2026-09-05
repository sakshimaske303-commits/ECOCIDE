# ECOCIDE — A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes

[![EarthArXiv](https://img.shields.io/badge/EarthArXiv-Preprint-B7410E.svg)](https://eartharxiv.org/repository/view/14827/) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21757974.svg)](https://doi.org/10.5281/zenodo.21757974)

**Isolating conflict-attributable environmental damage from pre-existing trends, using causal inference rather than qualitative interpretation.**

## Live Dashboard

**[View the interactive dashboard →](https://ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app/)**

## Project Documentation

| Document | What's Inside |
|---|---|
| [`ECO_Executive_Summary.pdf`](./ECO_Executive_Summary.pdf) | One-page snapshot — question, method, headline finding, robustness checklist, and links (start here) |
| [`ECO_Research_Paper.md`](./ECO_Research_Paper.md) | Formal academic paper — literature review, statistical methodology, results, discussion |
| [`ECO_Development_Log.md`](./ECO_Development_Log.md) | Full technical development log — every bug, debugging session, and methodology iteration |

---

The ECOCIDE framework is a geospatial causal-inference approach designed to support the independent verification of environmental degradation resulting from the armed conflict. Both the analysis and the entire pipeline are open for review and are built upon publicly available and third party processed satellite products (Sentinel Hub, UNOSAT), not depending on official government reporting of either country. This project seeks to help fill an identified gap because legislative measures to recognize war-induced environmental damage as an international crime are progressing globally (e.g. International Criminal Court, Trial Chamber of the former Yugoslavia), and because most satellite-based environmental assessments of conflict impacts focus on qualitative visual interpretation and explicitly do not claim causality. Applied to the destruction of the Kakhovka dam, ECOCIDE implements a Difference-in-Differences principle, which was proved using a placebo change experiment and an event study analysis.

---

## Interactive Maps & Plots

Interactive maps and headline charts are hosted via GitHub Pages:

**Map**
- [Verified Flood-Extent Map](https://sakshimaske303-commits.github.io/ECOCIDE/dashboard/static/kherson_flood_extent_webmap/index.html)

**Plots**
- [Event Study — Quarterly Treatment Effect on NDVI](https://sakshimaske303-commits.github.io/ECOCIDE/outputs/plots/interactive/event_study.html)
- [Multi-Control Robustness Check](https://sakshimaske303-commits.github.io/ECOCIDE/outputs/plots/interactive/control_panel_comparison.html)
- [Classical vs. HAC Standard Errors](https://sakshimaske303-commits.github.io/ECOCIDE/outputs/plots/interactive/robustness_check.html)

*(All four are also embedded together on the dashboard's Interactive Maps & Plots page.)*

---

## What This Project Does

- Tests the environmental effect produced by the destruction of the Kakhovka dam (6 June 2023), isolated from Ukraine's already-elevated, ongoing conflict baseline.
- Provides a before/after comparison for reference, but does not rely on that for the conclusion; uses a four-county Danube/Black Sea Romanian control panel (Tulcea, Galați, Brăila, Constanța) instead
- Confirms all findings with placebo testing (phony treatment dates) and with quarterly event study analysis
- Flood-extent data (UNOSAT) is used directly from its already-verified, multi-sensor product, instead of extracting flood detection from the raw satellite bands myself, as that is a task prone to noisy raw satellite band contamination.
- Presentations of before/after true-color satellite imagery, programmatically generated for full reproducibleness
- Clearly states an honest methodological scope of error identified during the validation process, never attempts to cover it up
- Makes the flood-extent map and the three statistical charts, showing headline information about the flood, clickable and interactive, not just images to sit on a desk

## Key Findings

A significant decrease in NDVI has been identified causally, which is statistically valid. The primary specification involves comparing Kherson (treatment) to Tulcea, Romania (control): the coefficient is −0.0703 (95% CI [−0.130, −0.010] with HAC-robust p = 0.022), while the coefficient using a clean placebo methodology is near zero with p = 0.612. Since only two units (treatment/control) the standard errors are using Newey-West HAC correction instead of clustering for which there are insufficient clusters to support cluster-robust inference.

The same model was also fit to the entirety of the four counties that make up the control panel in Romania (Tulcea, Galați, Brăila, Constanța); the impact remained unaffected. Pooled across all four, the effect stands: −0.0600 (HAC p = 0.029, 95% CI [−0.114, −0.006]; cluster-robust p = 0.002, 95% CI [−0.097, −0.023]). When tested separately, each of the three controls (Tulcea, Galați, Brăila) produces a significant effect which is near the magnitude specified in the primary control, the fourth one (Constanța, most coastal, most urbanized of the four) not, and that is stated explicitly rather than smoothed over. The four-county panel results from a placebo test are clean (+0.0222, p = 0.216, wrong sign).

An actual complication was discovered and disclosed. A calendar effect analysis demonstrated a remarkable impact in one of the two-zone specification's pre-treatment quarters, due to the background conflict of Kherson already existing prior to destruction of the dam in the summer of 2022. A narrowed baseline sensitivity analysis, which samples the narrower range to get a bigger response, fails its own placebo test when the proper HAC standard errors are applied to it, and has an outright validation failure to boot which wasn't ignored or whitewashed, but rather revealed as such and the separate (and validated) broader-baseline result remains intact. Running the same quarterly event study on the four-county panel surfaces an intrinsic property of a 5-cluster model design (1 treatment + 4 controls) against around 24 model parameters: cluster-robust standard errors come out at rank 4, not 24, and are thus numerically degenerate instead of truly precise. Under the correct HAC specification for that design, the treatment-quarter effect is not significant when pooled across four heterogeneous controls (p = 0.972), while the one-year-later effect remains significant (p = 0.011).

UNOSAT flood extent data based on the multi-sensor approach shows a full rise-peak-recession cycle: 122.50 km² (6 June) to 464.18 km² peak (9 June) and 21.17 km² (21 June).

All of the methodology, along with each debugging decision, and revealed limitation are documented in the Methodology page on the dashboard, as well as in the ECO_Research_Paper.md document.

## Architecture

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
Streamlit dashboard (dashboard/app.py + 9 pages) ──► Zenodo DOI
```

## Repository Structure

```text
ECOCIDE/
├── dashboard/                       # Streamlit dashboard (9 pages)
│   └── static/                      # Interactive flood-extent map, built in Python/folium (served via GitHub Pages)
├── build_interactive_plots.py       # Plotly interactive chart generation
├── data/
│   ├── boundaries/, ndvi/, ndwi/
│   └── satellite_imagery/           # Before/after true-color imagery
├── outputs/
│   └── plots/                       # Static visualizations (hydrograph, event study, etc.)
│       └── interactive/             # Plotly interactive HTML charts
├── qgis_processing/                 # Original QGIS2Web webmap export
├── ECO_Research_Paper.md            # Formal academic research paper
├── ECO_Development_Log.md           # Full technical development log
├── download_*.py                    # Dataset acquisition scripts
├── did_model*.py / event_study.py   # Causal inference scripts
├── map*.py                          # Static visualization scripts
└── requirements.txt
```

## Tech Stack

Python · GeoPandas · Matplotlib · Folium · Statsmodels · Streamlit · GitHub Pages · Sentinel Hub API · UNOSAT

## Data Sources

| Dataset | Provider |
|---|---|
| NDVI, True-Color Imagery | Sentinel-2, Sentinel Hub (Copernicus Data Space Ecosystem) |
| Verified Flood Extent | UNOSAT (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS) |
| Administrative Boundaries | GADM v4.1 |

## Running Locally

```bash
git clone https://github.com/sakshimaske303-commits/ECOCIDE.git
cd ECOCIDE
pip install -r requirements.txt
cd dashboard
streamlit run app.py
```

## Author

**Sakshi D. Maske**

Independent Geospatial Researcher

## License

This project is licensed under [CC BY 4.0](./LICENSE) — you are free to share and adapt this work for any purpose, including commercially, with attribution.

---

*This project's full development process — including every debugging session, methodology iteration, and disclosed limitation — is documented in `ECO_Development_Log.md` for full transparency and reproducibility.*