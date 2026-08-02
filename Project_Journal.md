# ECOCIDE: A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes

## Project Journal

## Project Overview

ECOCIDE is a geospatial causal-inference framework built to independently verify claims of environmental destruction arising from armed conflict, using Earth Observation data, remote sensing, and rigorous causal-inference methods — "independent" of official government reporting from any party, not of all human judgment, since the analysis is built on publicly available, third-party-processed satellite products (Sentinel Hub, UNOSAT). International legal bodies have begun formally considering "ecocide" — mass environmental destruction — as a prosecutable international crime, alongside genocide, crimes against humanity, war crimes, and aggression. Despite this emerging legal recognition, no standardized, statistically rigorous methodology has existed for evidencing such damage claims.

This project addresses that gap directly, applying a Difference-in-Differences causal framework — validated through placebo testing and event-study analysis — to isolate conflict-attributable environmental damage from pre-existing or naturally occurring trends, using independently observed satellite data rather than self-reported administrative claims or purely visual interpretation.

## Problem Statement

Environmental damage in conflict zones is frequently documented through anecdotal reporting or qualitative before-after satellite image comparison — approaches vulnerable to bias and, critically, unable to distinguish conflict-caused degradation from broader trends already underway before the conflict. Even the most methodologically careful existing geospatial assessments of this specific event explicitly decline to make causal attribution claims for exactly this reason. To the best of this literature review, no existing framework applies a genuine causal-inference design — a matched control zone, statistical significance testing, and placebo validation — to this class of problem.

## Relationship to Existing Work

The most recent published geospatial assessment of Ukraine's war-related environmental damage relies on visual, qualitative interpretation of multi-temporal imagery, triangulated with institutional reporting, and explicitly identifies the development of standardized, quantitative indicators as a direction for future research. ECOCIDE is designed specifically to fill that acknowledged gap for a shared case-study region, applying the same causal-inference rigor previously developed and validated in this researcher's prior work.

## Demonstration Case

The Kakhovka Dam destruction, 6 June 2023, on Ukraine's Dnipro River — draining an 18.2 km³ reservoir and flooding hundreds of square kilometers of downstream floodplain.

## Study Design

**Treatment Zone**: Kherson Oblast, Ukraine (46.777°N, 33.370°E) — the dam site and Dnipro River downstream floodplain.

**Control Zone**: Tulcea County, Romania (45.200°N, 29.500°E) — the Danube Delta, selected for a comparable pre-conflict ecological baseline (river-delta wetland, steppe, agricultural floodplain, similar continental climate) while being genuinely non-combatant. A within-Ukraine control zone was considered and rejected due to war-adjacent contamination risk; the Ukrainian side of the Danube Delta itself was also ruled out, since it has been affected by strikes on Danube port infrastructure.

## Data Sources

- **NDVI (vegetation index)**: Monthly, Sentinel-2, both zones, January 2022–November 2024
- **Verified flood extent**: UNOSAT multi-sensor product (ICEYE radar, Landsat-9, SkySat, WorldView-3, MODIS Aqua/Terra), five dates across June 2023
- **True-color satellite imagery**: Sentinel-2 L2A, programmatically acquired for identical before/after bounding boxes
- **Administrative boundaries**: GADM v4.1

## Methodology and Findings

### Flood Extent

Rather than deriving flood extent independently from raw satellite bands — an approach that produced unreliable, noisy results in this project's own testing — a verified, multi-sensor UNOSAT product was used. This revealed a complete, physically credible flood hydrograph: rapid expansion from 122.50 km² (6 June) to a peak of 464.18 km² (9 June), followed by steady recession to 21.17 km² by 21 June — a full rise-peak-recession cycle within roughly two weeks.

### Vegetation Impact — Difference-in-Differences

A Difference-in-Differences model, with month fixed effects controlling for seasonal vegetation cycles, found a statistically significant NDVI decline in Kherson relative to Tulcea following the dam's destruction: coefficient = −0.0703, 95% CI [−0.130, −0.010], R² = 0.747. Because this design compares only two units (one treatment zone, one control zone) rather than a multi-unit panel, cluster-robust standard errors are not applicable; inference instead uses Newey–West HAC standard errors, under which the effect remains significant (p = 0.022), a modest attenuation from the classical estimate (p = 0.007) consistent with serial correlation in the monthly series.

### Validation

A placebo test using a fake treatment date (June 2022) produced a near-zero, non-significant coefficient (0.0148, 95% CI [−0.043, 0.072], HAC p = 0.612) — clean confirmation that the real result reflects a genuine event-specific effect rather than a general pre-existing trend.

A quarterly event study largely supported the finding (significant negative effects in the treatment quarter, the following quarter, and one year later, under HAC standard errors), but also revealed a significant effect in a pre-treatment quarter (summer 2022), traced to Kherson already being an active conflict zone before the dam's destruction. A sensitivity analysis narrowing the baseline to exclude this confounded period produced a larger effect (−0.1384, 95% CI [−0.209, −0.068], HAC p = 0.0001), but its own placebo test, while non-significant classically (p = 0.169), becomes statistically significant under HAC correction (p = 0.001) — a decisive validation failure rather than an ambiguous one, given the very short, serially correlated ten-observation window. Both results are reported transparently, with the broader-baseline result treated as the sole primary finding given its own placebo test remains clean under HAC, while the narrowed-baseline result is retained only as an illustration of the pre-treatment-quarter problem.

## Deliverables

A reproducible causal-inference pipeline testing conflict-attributable environmental damage; a validated UNOSAT-based flood-extent timeline; a placebo-tested and event-study-validated NDVI causal estimate; before/after true-color satellite imagery for the same verified bounding box; an interactive QGIS-based flood-extent map; and a multi-page interactive dashboard presenting all findings, including honestly disclosed validation limitations.

## Limitations

The narrowed-baseline sensitivity analysis fails its own placebo test once HAC-robust standard errors are applied and is therefore not treated as independent validating evidence — it is retained only to illustrate the pre-treatment-quarter problem that motivated it. The single treatment–control pair design also means cluster-robust inference is unavailable; a design with more comparison zones would allow a stronger external-validity test. Reservoir water-loss could not be tested causally, since no comparable control-zone equivalent exists for a large upstream reservoir collapse; this is reported descriptively rather than as an independently causally-tested finding.

## Current Status

Complete. Core causal analysis, satellite evidence, and interactive dashboard finished; GitHub deployment in progress.