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

The ECOCIDE framework is a geospatial causal-inference approach designed to support the independent verification of environmental degradation resulting from the armed conflict. Both the analysis and the entire pipeline are open for review and are built upon publicly available and third party processed satellite products (Sentinel Hub, UNOSAT), not depending on official government reporting of either country. This project seeks to help fill an identified gap because legislative measures to recognize war-induced environmental damage as an international crime are progressing globally (e.g. International Criminal Court, Trial Chamber of the former Yugoslavia), and because most satellite-based environmental assessments of conflict impacts focus on qualitative visual interpretation and explicitly do not claim causality. Applied to the destruction of the Kakhovka dam, ECOCIDE implements a Difference-in-Differences principle, tested and stress-tested using a placebo experiment and an event-study analysis — with both disclosed limitations and confirmed checks reported below, not just the checks that passed.

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
- Stress-tests the main finding with placebo testing (phony treatment dates), quarterly event-study analysis, exact randomization inference (placebo-in-space), and a control-only spillover check — not all of them hold up cleanly: the primary result no longer clears conventional significance under the corrected NDVI extraction, and randomization inference shows Kherson is no longer the most extreme of the five geographic units in this design (see Key Findings below)
- Flood-extent data (UNOSAT) is used directly from its already-verified, multi-sensor product, instead of extracting flood detection from the raw satellite bands myself, as that is a task prone to noisy raw satellite band contamination.
- Presentations of before/after true-color satellite imagery, programmatically generated for full reproducibleness
- Clearly states an honest methodological scope of error identified during the validation process, never attempts to cover it up
- Makes the flood-extent map and the three statistical charts, showing headline information about the flood, clickable and interactive, not just images to sit on a desk

## Key Findings

**Updated after a methodology correction.** An earlier version of this project's NDVI extraction queried Sentinel Hub using each zone's rectangular bounding box rather than its true GADM administrative polygon, and filtered clouds only at the whole-scene level rather than per pixel. Both are now corrected (true polygon geometry + pixel-level Sentinel-2 Scene Classification masking), and the correction materially weakens the headline result below. The numbers and framing here reflect the corrected analysis; see `ECO_RESULTS_RECONCILIATION.md` for the full before/after and `ECO_Research_Paper.md` §3.3 for the technical detail.

A directionally consistent decrease in NDVI in Kherson relative to its main control (Tulcea, Romania) is still present, but it no longer clears the conventional 5% statistical-significance threshold: the coefficient is −0.0747 (95% CI [−0.153, 0.003], HAC-robust p = 0.060), against the originally-reported −0.0703 (p = 0.022). The specification's own broad-window placebo test still comes back clean (near-zero, p = 0.882). Since only two units (treatment/control), the standard errors use Newey-West HAC correction instead of clustering, for which there are insufficient clusters to support cluster-robust inference.

The same model was also fit to the entirety of the four counties that make up the Romanian control panel (Tulcea, Galați, Brăila, Constanța); pooled across all four, the effect shows the same weakening: −0.0661 (HAC p = 0.059, 95% CI [−0.135, 0.003]; cluster-robust p = 0.034 — a cross-check only, since 5 clusters is the bare minimum for cluster-robust inference to be defined). When tested separately, two of the four controls (Galați, Brăila) still produce a significant effect near the primary magnitude; Tulcea is now itself only marginal; Constanța does not, and — unlike in the original analysis — this is no longer treated as an open ecological question: a direct test (below) traces it to Constanța having its own independent shift, unrelated to the dam.

**The most important new finding**: an exact randomization-inference check (placebo-in-space — assigning "treated" status to each of the five geographic units in turn, not just Kherson) shows Kherson is *no longer the most extreme unit* under the corrected data. Two of the four Romanian counties, Brăila and Constanța, show comparable-or-larger "effects" of their own under the identical procedure, with no dam ever having failed near them. A follow-up check, excluding Kherson from the panel entirely, confirms both counties have their own statistically significant post-June-2023 divergence, for reasons this design does not identify. With only five geographic units available, this design cannot statistically distinguish Kherson's real post-event decline from the independent variation already present among the control counties themselves — a materially narrower claim than this project originally made. Dropping the data's lowest-coverage months does not recover the original result either; it weakens it slightly further, ruling out one candidate benign explanation.

A separate, pre-existing complication remains disclosed as before: a calendar-effect analysis shows a significant pre-treatment-quarter effect in the two-zone specification, attributed to Kherson's background conflict already being under way before the dam's destruction, not to a violation of the design around June 2023 specifically. The narrowed-baseline specification's own placebo test, which previously failed once proper HAC standard errors were applied (an outright validation failure), no longer fails under the corrected data — one of the few checks that improved rather than worsened. Running the same quarterly event study on the four-county panel still shows cluster-robust standard errors are numerically degenerate at 5 clusters against ~24 parameters; under the correct HAC specification, the treatment-quarter effect remains not significant when pooled across four heterogeneous controls (p = 0.278), while the one-year-later effect remains significant (p = 0.0001).

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