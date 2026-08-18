# ECOCIDE: A Causal-Inference Framework for Independently Verifying War-Time Environmental Damage

## Index

1. [Project Overview](#project-overview)
2. [Problem Statement](#problem-statement)
3. [Aim](#aim)
4. [Objectives](#objectives)
5. [Research Question](#research-question)
6. [Relationship to Existing Work](#relationship-to-existing-work)
7. [Expected Outputs](#expected-outputs)
8. [Demonstration Case](#demonstration-case)
9. [Current Status](#current-status)
10. [Module Architecture](#ecocide-module-architecture)
11. [Module 1 — Project Conceptualization & Literature Review](#module-1-project-conceptualization-literature-review)
12. [Module 2 — Study Area & Control Zone Definition](#module-2-study-area-control-zone-definition)
13. [Module 3 — Core Dataset Acquisition](#module-3-core-dataset-acquisition)
14. [Module 4 — Conflict Event Timeline Construction](#module-4-conflict-event-timeline-construction)
15. [Module 5 — Difference-in-Differences Causal Model](#module-5-difference-in-differences-causal-model)
16. [Module 6 — Statistical Confidence & Damage Quantification](#module-6-statistical-confidence-damage-quantification)
17. [Module 7 — Geospatial Visualization](#module-7-geospatial-visualization)
18. [Module 8 — Dashboard & Deployment](#module-8-dashboard-deployment)
19. [Module 9 — Documentation](#module-9-documentation)
20. [Study Area & Control Zone — Decision Log](#study-area-control-zone-decision-log)
21. [Boundary Acquisition](#boundary-acquisition)
22. [NDVI Acquisition](#ndvi-acquisition)
23. [NDWI Acquisition — A Multi-Stage Debugging Process](#ndwi-acquisition-a-multi-stage-debugging-process)
24. [Design Principle Reinforced](#design-principle-reinforced)
25. [Downstream Floodplain — Resolution via Authoritative UNOSAT Flood Extent Data](#downstream-floodplain-resolution-via-authoritative-unosat-flood-extent-data)
26. [Difference-in-Differences Model — NDVI](#difference-in-differences-model-ndvi)
27. [Event Study Validation](#event-study-validation)
28. [Placebo Test Ambiguity — Narrowed Window](#placebo-test-ambiguity-narrowed-window)
29. [Difference-in-Differences Model — NDVI, Full Journey](#difference-in-differences-model-ndvi-full-journey)
30. [Design Principle Reinforced (Reservoir Analysis)](#design-principle-reinforced-1)
31. [Reservoir Water-Loss — Quantification Without a Comparable Control](#reservoir-water-loss-quantification-without-a-comparable-control)
32. [Geospatial Visualization, Dashboard, and Documentation (Modules 7–9)](#geospatial-visualization-dashboard-and-documentation-modules-79)
33. [Panel-Readiness Review and Robustness Pass](#panel-readiness-review-and-robustness-pass)
34. [Deep Verify: Independent Recomputation of Every Reported Statistic (2026-08-03)](#development-log-deep-verify-independent-recomputation-of-every-reported-statistic-2026-08-03)
35. [The Control-Zone Expansion — From a Single Control to a Small Panel (2026-08-13)](#development-log-the-control-zone-expansion-from-a-single-control-to-a-small-panel-2026-08-13)

## Project Overview

ECOCIDE is a geospatial causal-inference framework designed to independently verify claims of environmental destruction arising from armed conflict, using Earth Observation (EO) data, remote sensing, and statistical causal-inference methods — "independent" of official government reporting from any party, not of all human judgment, since the analysis is built on publicly available, third-party-processed satellite products. In recent years, international legal bodies have begun formally considering the recognition of mass environmental destruction — "ecocide" — as a prosecutable international crime, alongside genocide, crimes against humanity, war crimes, and aggression.

Existing geospatial assessments of conflict-related environmental damage — including the most recent published assessment of the Ukraine war (Leal Filho et al., 2026) — rely on visual, qualitative before-after satellite image comparison and explicitly do not attempt to establish statistical causality, instead describing observed changes as "conflict-associated" rather than conflict-attributable. This is a deliberate and reasonable methodological choice given the scope of that prior work, but it leaves a specific, acknowledged gap: To the best of this literature review, no published framework quantifies conflict-attributable environmental damage using a genuine causal-inference design with a matched non-conflict control zone, statistical significance testing, and placebo validation.

ECOCIDE addresses this specific gap directly, applying a Difference-in-Differences causal framework — validated through placebo testing and event-study analysis — to isolate conflict-attributable environmental damage from pre-existing or naturally occurring degradation, using independently observed satellite data rather than self-reported administrative claims or purely visual interpretation.

## Problem Statement

Environmental damage in conflict zones is frequently documented through anecdotal reporting, damaged infrastructure counts, or qualitative before-after satellite image comparison, all of which are vulnerable to bias, incompleteness, and — critically — an inability to distinguish conflict-caused degradation from broader environmental trends already underway prior to the conflict (drought cycles, pre-existing industrial pollution, seasonal variation). Even recent, methodologically careful geospatial assessments explicitly decline to make causal attribution claims for this reason. There is currently no accessible, reproducible geospatial methodology that quantifies environmental war damage with the statistical rigor of a genuine causal-inference design, sufficient to support legal evidence assessment , humanitarian, or policy use.

## Aim

To develop a reproducible geospatial framework that quantifies environmental damage statistically attributable specifically to armed conflict, using satellite-derived environmental indicators and a Difference-in-Differences causal-inference design — validated through placebo testing and event-study analysis — capable of distinguishing conflict-driven change from baseline environmental trends with quantified statistical confidence.

## Objectives

- Identify and acquire multi-temporal Earth Observation datasets capable of capturing environmental degradation (vegetation loss via NDVI, water turbidity/contamination indicators, land-cover change, burn severity) in conflict-affected regions, at pixel-level quantitative resolution rather than visual interpretation.
- Construct a Difference-in-Differences causal-inference design comparing conflict-affected zones against a matched non-conflict control zone with a comparable pre-conflict ecological baseline.
- Validate the causal estimate through placebo testing (applying the identical model to a counterfactual pre-conflict date) and event-study analysis, consistent with rigorous causal-inference practice.
- Quantify the magnitude and statistical confidence (confidence intervals, significance testing) of environmental damage directly attributable to conflict events — a level of statistical rigor not present in existing qualitative geospatial assessments of the same case.
- Develop a reproducible, satellite-driven methodology that can be applied to multiple conflict zones and time periods beyond the initial case study.
- Produce a geospatial evidence output structured to be interpretable in legal, humanitarian, and policy contexts, while remaining honest about the distinction between statistical attribution and formal legal classification.

## Research Question

Does armed conflict produce a statistically significant, quantifiable increase in environmental degradation beyond what a comparable non-conflict region would have experienced over the same period — and can this effect be isolated with sufficient statistical confidence to distinguish it from pre-existing environmental trends?

## Relationship to Existing Work

This project directly builds on and differentiates from the most recent geospatial assessment of Ukraine's war-related environmental damage (Leal Filho et al., 2026, Frontiers in Environmental Science), which explicitly identifies the development of standardized, quantitative indicators as a direction for future research. That study's methodology — visual interpretation of multi-temporal imagery, triangulated with qualitative institutional reporting, without a matched control zone or causal-inference design — is appropriate for its broader descriptive and typological aims, but does not attempt statistical attribution. ECOCIDE is designed specifically to fill that acknowledged gap for a shared case-study region, applying the same causal-inference rigor (Difference-in-Differences, placebo testing, event-study validation) previously developed and validated during previous research projects).

## Expected Outputs

- A satellite-derived, multi-temporal, pixel-level environmental damage dataset for the study region and matched control zone.
- A Difference-in-Differences causal-inference model isolating conflict-attributable environmental change, validated through placebo testing and event-study analysis.
- Statistical confidence estimates (p-values, confidence intervals) quantifying the magnitude of attributed damage — a level of rigor not present in comparable existing assessments.
- High-quality, publication-grade geospatial visualizations of the conflict timeline and environmental damage evidence.
- An interactive geospatial dashboard presenting damage timelines and evidence outputs.
- A reproducible methodology adaptable to other conflict zones and future case studies.
- Complete technical documentation and open-source implementation.

## Demonstration Case

The Kakhovka Dam destruction (6 June 2023) and surrounding Dnipro River floodplain and Donbas industrial region, Ukraine, will serve as the initial validation case study, given the availability of well-documented conflict timelines and pre-conflict environmental baseline data. Following validation, the framework is designed to be extended to other conflict-affected regions globally.

## Current Status

Complete — all nine modules finished: causal analysis (Modules 1–6), geospatial visualization and interactive dashboard (Modules 7–8), and full documentation with GitHub/Zenodo deployment (Module 9). The methodology was subsequently reviewed and strengthened with Newey-West HAC-robust standard errors and a full panel-readiness pass; see "Panel-Readiness Review and Robustness Pass" below.
Version 3.0

----------------------------------------------------------------------------------------------------

# ECOCIDE — Module Architecture

# MODULE 1 — Project Conceptualization & Literature Review
Research question, aim, and objectives finalized. Existing literature on satellite-based conflict-environment assessment reviewed in depth, identifying the specific methodological gap this project addresses: existing geospatial assessments of war-related environmental damage rely on qualitative, visual before-after image interpretation and explicitly decline to establish statistical causality. To the best of this literature review, no existing framework applies a genuine causal-inference design — matched control zone, Difference-in-Differences model, placebo validation — to conflict-attributable environmental damage.

# MODULE 2 — Study Area & Control Zone Definition
Definition of the conflict-affected treatment zone and a matched, genuinely non-conflict control zone with comparable pre-conflict ecological baseline, required for the Difference-in-Differences design.

# MODULE 3 — Core Dataset Acquisition
Acquisition of multi-temporal Earth Observation datasets capable of capturing environmental degradation — vegetation loss (NDVI), water turbidity/contamination indicators, land-cover change, burn severity — across both treatment and control zones, at pixel-level quantitative resolution.

# MODULE 4 — Conflict Event Timeline Construction
Construction of a verified conflict-event timeline establishing the treatment date(s) required for the causal model.

# MODULE 5 — Difference-in-Differences Causal Model
Statistical comparison of treatment-zone versus control-zone environmental change using a Difference-in-Differences framework, validated through placebo testing and event-study analysis.

# MODULE 6 — Statistical Confidence & Damage Quantification
Quantification of the magnitude and statistical confidence (confidence intervals, significance testing) of environmental damage attributable to the conflict event.

# MODULE 7 — Geospatial Visualization
Production of high-quality, professional-grade remote-sensing maps and visualizations of the conflict timeline and environmental damage evidence.

# MODULE 8 — Dashboard & Deployment
Development and deployment of an interactive geospatial dashboard presenting damage timelines and evidence outputs.

# MODULE 9 — Documentation
Project Journal, Research Paper, README, and GitHub deployment.

--------------------------------------------------------------------------------------------------

## Study Area & Control Zone — Decision Log

**Conflict (Treatment) Zone**: Kakhovka Dam area and Dnipro River downstream floodplain 
(46.777°N, 33.370°E), Kherson Oblast, Ukraine. Dam destroyed 6 June 2023. Flood-affected 
analysis zone spans approximately 10,800 km² (dam to river mouth, per UNOSAT satellite analysis).

**Control Zone Selection Process**: A within-Ukraine non-frontline control zone (e.g., 
Dnipropetrovsk Oblast) was initially considered, but rejected — recent reporting indicates the 
frontline has moved closer to this region, and war-adjacent economic and demographic effects 
(supply disruption, displacement) could contaminate a control zone even without direct conflict 
in that specific area. This mirrors a methodological risk identified in prior work (GPIE), where 
an internal-to-the-affected-region control group proved insufficiently independent.

**Control Zone Selected**: Danube Delta, Tulcea County, Romania (45.200°N, 29.500°E). Selected 
for a comparable pre-conflict ecological baseline — river-delta wetland, Pannonian steppe, 
agricultural floodplain, similar continental climate — while being genuinely non-combatant. 
Explicitly verified as distinct from the Ukrainian side of the Danube Delta (Odesa Oblast), which 
has itself been affected by war-related strikes on Danube port infrastructure and is therefore 
unsuitable as a control.

---------------------------------------------------------------------------------------------------

## Boundary Acquisition

Administrative boundaries for both zones were acquired from GADM version 4.1, downloaded as complete country-level GeoPackage files for Ukraine (`gadm41_UKR.gpkg`) and Romania (`gadm41_ROU.gpkg`), since GADM does not provide single-region downloads — the full country file must be downloaded and the specific region extracted afterward.

A naming inconsistency was discovered during extraction: Ukrainian oblasts are stored at GADM's Level 1 (`ADM_ADM_1`, field `NAME_1`), where Kherson matched directly by name. Romanian counties, however, were initially searched for at Level 2 (`ADM_ADM_2`), which in GADM's schema for Romania actually corresponds to communes and small municipalities (hundreds of small place names like "Abrud," "Aiud," "Alba Iulia"), not counties. Tulcea was not found at this level. Checking Level 1 (`ADM_ADM_1`) instead confirmed Romanian counties are stored there, and Tulcea was correctly extracted from this level. This reflects a genuine cross-country inconsistency in GADM's administrative hierarchy numbering, not an error in the source data itself, and was resolved by directly inspecting each country's actual level structure rather than assuming a consistent numbering scheme across countries.

Both boundaries were extracted and saved independently (`kherson_oblast.gpkg`, `tulcea_county.gpkg`), with confirmed bounding boxes:
- Kherson: 31.51°E–35.10°E, 45.90°N–47.58°N
- Tulcea: 27.99°E–29.72°E, 44.61°N–45.46°N

---

## NDVI Acquisition

Monthly NDVI (Normalized Difference Vegetation Index) was acquired via the Sentinel Hub Statistical API for both the Kherson and Tulcea bounding boxes, spanning January 2022 through November 2024 (35 monthly data points each), reusing the authentication module and evalscript pattern established in prior work (GPIE, DOUBLE JEOPARDY). Values returned were in a plausible 0.07–0.17 range for winter months in a steppe/agricultural region, consistent with expected seasonal vegetation dormancy, and were accepted as valid without further correction at this stage.

---

## NDWI Acquisition — A Multi-Stage Debugging Process

### Attempt 1: Full Kherson Oblast, Monthly Resolution

An initial NDWI (Normalized Difference Water Index) request was made using the same full Kherson Oblast bounding box used for NDVI, at monthly resolution, spanning the same three-year window. The resulting time series showed no discernible signal around the 6 June 2023 dam destruction date — June 2023's NDWI value did not differ meaningfully from surrounding months.

This was investigated rather than accepted as a null result. The root cause identified was spatial dilution: Kherson Oblast spans approximately 28,000 km², while the actual flood extent following the dam breach was documented at approximately 600 km² (UNOSAT). Averaging NDWI across the full oblast meant the flood signal, confined to roughly 2% of the bounding box's area, was mathematically overwhelmed by the surrounding 98% of unaffected land and was not detectable in the aggregate mean.

### Attempt 2: Narrowed Flood Corridor, Monthly Resolution

The bounding box was narrowed to a tighter river corridor directly surrounding the dam and downstream floodplain (32.0°E–33.6°E, 46.3°N–46.9°N), still at monthly resolution. This produced a marginally more plausible pattern (a less-negative, more-water-like value in May 2023 consistent with pre-breach reservoir filling), but still no clear, unambiguous spike in June or July 2023 relative to the surrounding months. Two months (December 2022, December 2024) returned no data at all, consistent with winter cloud cover over the region — Sentinel-2 is an optical sensor and cannot observe through cloud cover, meaning any given month's composite reflects only the cloud-free days within it, which can vary substantially month to month.

### Attempt 3: Weekly Resolution, Narrowed Corridor

To test whether the monthly aggregation itself was obscuring a shorter-duration flood signal, the same narrowed corridor was re-queried at weekly resolution for April–August 2023 specifically. This revealed an unexpected pattern: 3 June 2023 (the week immediately preceding the dam's destruction) showed the single most negative (least-water-like) NDWI value in the entire window, the opposite of what would be expected if flooding were being captured.

### Root Cause Identified: Opposing Signals Within a Single Bounding Box

This counterintuitive result was traced to a structural issue in the bounding box itself: it spanned both the upstream Kakhovka Reservoir (which drained rapidly after the dam breach, an approximately 18 km³ water loss) and the downstream Dnipro floodplain (which flooded following the same breach). These two sub-regions experience opposite water-level changes from the same event — the reservoir's water level dropping while the floodplain's water level rises — and averaging NDWI across both simultaneously caused the two opposing signals to statistically cancel each other out, producing an apparently flat or noisy combined result that reflected neither true underlying process.

### Attempt 4: Splitting Into Upstream and Downstream Sub-Zones

The bounding box was split at the dam's latitude (46.777°N) into two independent zones — an upstream reservoir zone and a downstream floodplain zone — each queried separately at weekly NDWI resolution for the same April–August 2023 window. This did not resolve the issue: both sub-zones still showed erratic, physically implausible week-to-week swings (for example, the upstream zone's mean NDWI-derived water percentage moving from 45% to 16% to under 3% across three consecutive weeks with no plausible physical mechanism for such rapid, repeated reversal).

### Root Cause Identified: Optical Cloud Contamination, Not a Hydrological Signal

This volatility was diagnosed as sensor-level noise rather than genuine hydrological variation. Because Sentinel-2 is a cloud-blocked optical sensor, each week's aggregated statistic is computed only from whatever cloud-free pixels happened to be available that specific week — a different, effectively random subset of the bounding box each time — rather than a consistent spatial sample. This produces large apparent swings in any area-averaged statistic that have nothing to do with actual water extent changing, and everything to do with which parts of the scene happened to be cloud-free in a given week. This same class of limitation is explicitly acknowledged in the existing published Ukraine ecocide literature reviewed during this project's conceptualization phase, which used pre-built Copernicus Emergency Management Service (CEMS) rapid-mapping flood products for the Kakhovka event specifically because those products are derived from radar rather than optical imagery.

### Attempt 5: Switching to Sentinel-1 SAR (Radar) Data

Following this diagnosis, the water-detection method was switched from Sentinel-2 optical NDWI to Sentinel-1 Synthetic Aperture Radar (SAR), which is unaffected by cloud cover since radar wavelengths penetrate clouds. A standard VV-polarization backscatter threshold (below −17 dB, a widely used threshold for identifying smooth open-water surfaces in SAR imagery) was used to classify each pixel as water or non-water, and the percentage of water pixels per week was computed for both the upstream and downstream sub-zones.

**Result — Upstream Reservoir**: A clean, physically plausible, and directionally consistent signal emerged. Water percentage remained in an approximately 2–5% range through late May 2023, then dropped sharply beginning the week of 3 June 2023 and remained persistently low (approximately 1–3%) through August 2023, with no reversion to pre-breach levels. This pattern is consistent with a reservoir that drained rapidly and did not refill — matching the known outcome of the dam's destruction.

**Result — Downstream Floodplain**: No comparably clean signal emerged. Water percentage oscillated within a narrower 4–6% band both before and after the breach date, without a clear directional shift, including an unexplained dip in mid-to-late June (the period immediately following the breach, when flooding would be expected to be at or near its peak). Possible explanations under consideration include the flood peak and recession both occurring within a single weekly composite window (given that flood levels were documented to recede substantially within roughly two weeks), and/or flooded agricultural land and submerged vegetation producing a SAR backscatter signature that does not cleanly cross the same open-water threshold calibrated for the reservoir's cleaner water surface.

**Current Status**: The upstream reservoir water-loss signal is considered sufficiently clean and physically credible to proceed toward the Difference-in-Differences causal model. The downstream floodplain signal remains unresolved and is being treated as a separate, currently open methodological question rather than force-fit into the existing threshold-based approach.

## Design Principle Reinforced

This sequence of five acquisition attempts reflects the same evidence-first debugging discipline applied throughout prior work: an unexpected or absent signal was treated as a diagnostic question at each stage — spatial dilution, opposing signals within one bounding box, optical cloud contamination — rather than as either a dead end or an invitation to select whichever result looked most convenient. Each fix was derived from a specific, verified mechanism (documented flood extent versus oblast area; the dam's exact latitude as a natural split point; the known cloud-penetration property of SAR versus optical sensors) rather than trial-and-error parameter adjustment, and the one sub-signal that remains unresolved (the downstream floodplain) is reported as an open problem rather than suppressed or silently worked around.

---

## Downstream Floodplain — Resolution via Authoritative UNOSAT Flood Extent Data

Following the diagnosis that both weekly-resolution NDWI and relaxed-threshold SAR classification failed to produce a clean, physically credible flood signal for the downstream floodplain zone, a decision was made to stop attempting to derive flood extent independently from raw satellite bands and instead source a verified, pre-classified flood-extent product from an authoritative body — consistent with the approach already taken by the existing published Ukraine ecocide literature reviewed during this project's conceptualization.

A comprehensive UNOSAT (United Nations Satellite Centre) flood-mapping dataset was located and downloaded via the Humanitarian Data Exchange (HDX) platform (product code FL20230606UKR), containing verified flood-extent polygons derived from multiple independent satellite sensors — ICEYE (radar), Landsat-9, SkySat, WorldView-3, and MODIS Aqua/Terra — across multiple dates spanning 3 June through 21 June 2023, each independently analyzed and quality-controlled by UNOSAT analysts. This represents a substantially more reliable data source than an independently-derived single-sensor threshold classification, since it incorporates cross-sensor validation and manual analyst review rather than a single automated backscatter or index threshold.

The file corresponding to 6 June 2023 (the date of the dam's destruction) — `ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp` — was loaded and verified: a single polygon feature in EPSG:4326, covering approximately 122.50 km² of flooded area on that specific date. This is smaller than UNOSAT's own subsequently-reported cumulative flood extent of approximately 600 km², consistent with flooding having progressively expanded over the following two weeks before reaching its documented peak around 21 June 2023, rather than reaching full extent on the first day.

This resolves the downstream floodplain measurement problem not by further tuning an independently-derived threshold, but by substituting a verified, authoritative, multi-sensor flood product for the specific dates needed — the same category of solution already validated in the existing literature for this exact event.

----------------------------------------------------------------------------------------------------

Loading all five available date-snapshots (6, 8, 9, 13, 21 June 2023) confirmed a physically 
credible flood hydrograph: rapid expansion from 122.50 km² (6 June) to a peak of 464.18 km² 
(9 June), followed by steady recession to 21.17 km² by 21 June — a complete rise-peak-recession 
cycle within approximately two weeks. This rapid dynamic explains why independently-derived 
NDWI/SAR time series at weekly or 3-day resolution failed to capture a clean signal: the flood's 
full cycle occurred faster than consistent, cloud-free satellite revisit intervals could reliably 
sample, reinforcing the decision to use UNOSAT's verified multi-sensor product for this specific 
measurement.

----------------------------------------------------------------------------------------------------

## Difference-in-Differences Model — NDVI

A Difference-in-Differences model was constructed comparing monthly NDVI between Kherson 
(treatment) and Tulcea (control), with June 2023 as the treatment date. An initial model without 
seasonal controls produced a weak, non-significant result (R²=0.054, did_term p=0.117) — 
consistent with strong uncontrolled seasonal vegetation cycles dominating the residual variance. 
Adding month fixed effects substantially improved model fit (R²=0.747) and revealed a 
statistically significant treatment effect: did_term = -0.0703 (p=0.007), indicating a genuine 
NDVI decline in Kherson relative to Tulcea following the conflict event, after controlling for 
baseline differences and seasonality.

A placebo test was conducted using a fake treatment date (June 2022, one year before the actual 
event), restricted to pre-conflict data only. This produced no significant effect (did_term = 
0.0148, p=0.7411), confirming the real result is not an artifact of a general pre-existing trend 
in Kherson, and providing strong validation of the genuine treatment effect's credibility.

## Event Study Validation

A quarterly-binned event study (necessary after monthly-resolution bins produced a 
rank-deficient, unestimable model with only 70 total observations) was conducted to test whether 
the treatment effect was genuinely concentrated around the June 2023 event, rather than reflecting 
a pre-existing trend.

Results were mixed rather than cleanly supportive. Quarters immediately following the event 
(Quarter 0, Jun-Aug 2023: p=0.035; Quarter +4, 2024: p=0.0001) showed significant negative 
effects, consistent with genuine post-conflict vegetation decline. However, one pre-event quarter 
(Quarter -4, summer 2022) also showed a significant negative effect (p=0.007), which is not 
consistent with a clean parallel-trends assumption and is reported honestly as a limitation rather 
than omitted. This does not invalidate the overall DiD and placebo-test results, but indicates 
the treatment effect should be interpreted with appropriate caution regarding pre-existing 
seasonal or baseline differences between the two zones, rather than presented as an unambiguous, 
fully clean causal estimate.

## Placebo Test Ambiguity — Narrowed Window

A placebo test using a fake treatment date (March 2023) within the narrowed pre-period produced 
a coefficient (-0.1382) nearly identical in magnitude to the real June 2023 result (-0.1384), 
though not statistically significant (p=0.169 vs p=0.002). This is interpreted cautiously rather 
than as clean validation: the narrowed placebo window (Jan-May 2023, only 10 observations) has 
substantially reduced statistical power, making it unable to reliably distinguish a genuine null 
effect from an underpowered test of a real effect. The near-identical coefficient magnitude means 
this placebo test cannot be treated as strong confirmatory evidence, unlike the original 
2022-baseline placebo test, which showed both a near-zero coefficient and a high p-value together. 
This is reported as a genuine methodological limitation: the narrowed-baseline DiD result should 
be interpreted as suggestive rather than definitively isolated from possible confounding events 
in the March-May 2023 period specifically.

## Difference-in-Differences Model — NDVI, Full Journey

### Initial Model (Full 2022-2024 Baseline, No Seasonal Control)

The first DiD model compared monthly NDVI between Kherson (treatment) and Tulcea (control) across the full available 2022-2024 window, with June 2023 as the treatment date. This produced a weak, non-significant result (R²=0.054, did_term coefficient=-0.0703, p=0.117). This was not accepted as a null finding without investigation, since NDVI is known to follow strong seasonal cycles that, if uncontrolled, dominate residual variance and can mask a genuine treatment effect regardless of whether one exists.

**Reasoning for next step**: Rather than concluding "no effect exists," the low R² itself was treated as diagnostic — a model explaining only 5% of variance in a variable with strong, well-documented seasonal structure suggested a missing control variable, not an absent effect.

### Adding Month Fixed Effects

Month fixed effects were added to control for seasonal vegetation cycles. This substantially improved model fit (R²=0.747) and produced a statistically significant treatment effect (did_term=-0.0703, p=0.007) — the same coefficient magnitude as before, now correctly estimated with appropriate precision once seasonal noise was removed from the residual variance.

**Reasoning**: The coefficient did not change, only its estimated precision did — confirming the seasonal confound was inflating uncertainty around a real effect, rather than the effect itself being an artifact of missing controls.

### Placebo Test (Fake Date, Full Baseline)

Following the standard validation discipline established in prior work (GPIE), a placebo test was run using a fake treatment date (June 2022) restricted to pre-conflict-event data. This produced a near-zero, non-significant coefficient (0.0148, p=0.741), providing strong validation that the real June 2023 result reflects a genuine event-specific effect rather than a general pre-existing trend.

**Reasoning for accepting this as validation**: A clean placebo result requires both a near-zero coefficient AND a high p-value together — this placebo test showed both, which is the strongest form of validation available short of a randomized experiment.

### Event Study — Monthly Resolution Failure

An attempt to run a full monthly-resolution event study (following the same category of validation used in GPIE's 23-quarter analysis) failed technically: with only 70 total observations and a model specification requiring roughly 68 parameters (monthly relative-time dummies, month fixed effects, and event-interaction terms), the model became rank-deficient and could not estimate standard errors (all p-values returned as NaN).

**Reasoning for the fix**: This was diagnosed as an over-parameterization problem specific to this project's much smaller sample size relative to GPIE's 27-country, multi-year panel — not a fundamental flaw in the event-study approach itself. The fix was to reduce temporal resolution (quarterly rather than monthly bins) to bring the parameter count well below the observation count, preserving the event-study logic while making it estimable.

### Event Study — Quarterly Resolution, Mixed Result

The quarterly event study revealed a genuine problem: while post-event quarters showed significant negative effects (Quarter 0: p=0.035; Quarter +4: p=0.0001), one pre-event quarter (Quarter -4, summer 2022) also showed a significant negative effect (p=0.007) — inconsistent with a clean parallel-trends assumption.

**Reasoning for investigating rather than reporting as-is**: A significant pre-treatment effect specifically threatens the core validity of a DiD design, so this was investigated for cause rather than noted and left unresolved. The investigation identified that Kherson Oblast was already the site of active conflict (including the Kherson liberation operation, August-November 2022) well before the June 2023 dam destruction — meaning the original "pre-period" baseline was not a genuine pre-conflict baseline at all, but a period of different, already-ongoing conflict intensity. This is a scope-definition problem: the project aims to isolate the dam destruction's specific effect, not the cumulative effect of the entire war, and a baseline period that itself contains major conflict events cannot cleanly serve that narrower purpose.

### Narrowed-Baseline DiD (Sensitivity Analysis)

To address this, the pre-period was narrowed to January-May 2023 only — the months immediately preceding the dam's destruction, avoiding the confounded 2022 baseline. This produced a larger, still highly significant effect (did_term=-0.1384, p=0.002, R²=0.768).

**Reasoning for treating this as a sensitivity check rather than an automatic replacement for the original result**: A larger effect size after removing a contaminated baseline is exactly what would be expected if the narrowing correctly isolated the marginal event-specific damage. However, a subsequent placebo test within this narrowed window (fake date: March 2023) produced a coefficient of nearly identical magnitude (-0.1382) to the real result, though not statistically significant (p=0.169).

**Reasoning for not accepting this narrowed result as cleanly validated**: A placebo coefficient of nearly identical magnitude to the real effect is a meaningfully different — and weaker — form of validation than a placebo coefficient near zero, even when the placebo's p-value is not significant. The narrowed placebo window contains only 10 observations, giving it low statistical power; a non-significant p-value in this context could reflect either a genuine null effect or an underpowered test of a real (possibly confounded) effect, and the near-identical coefficient magnitude means this distinction cannot be resolved with the current data. This is reported as an honest, unresolved limitation rather than treated as either confirmatory or disqualifying.

### Current Reporting Decision

Both results are retained and reported transparently rather than selecting only the more favorable one: the original broader-baseline DiD result (did_term=-0.0703, p=0.007) is treated as the primary finding, since its placebo test was unambiguously clean (near-zero coefficient, high p-value together). The narrowed-baseline result (did_term=-0.1384, p=0.002) is reported as a sensitivity analysis showing a larger effect once the confounded 2022 baseline is excluded, with its own placebo-validation limitation explicitly disclosed rather than omitted.

## Design Principle Reinforced

This sequence directly parallels the discipline established in prior work (GPIE's placebo-driven model correction; DOUBLE JEOPARDY's honest reporting of an unsupported hypothesis): a favorable-looking result at each stage was treated as a hypothesis requiring further stress-testing rather than a conclusion, technical failures (the rank-deficient monthly event study) were diagnosed to their specific cause rather than worked around by weakening the validation approach, and an ambiguous validation result was reported as ambiguous rather than either suppressed or force-interpreted in the more convenient direction.

## Reservoir Water-Loss — Quantification Without a Comparable Control

An attempt was made to statistically quantify reservoir/floodplain water-loss in a Difference-in-
Differences format matching the NDVI approach, but this was not feasible: no comparable control-
zone equivalent exists for a river-mouth reservoir collapse specifically, since Tulcea's Danube
Delta control zone has no equivalent large upstream reservoir infrastructure. This is reported as
a genuine data-availability constraint rather than worked around.

Instead, reservoir and downstream floodplain water changes are reported descriptively using the
UNOSAT flood-progression data already validated: pre-breach reservoir extent of approximately
2,155 km² and 18.2 km³ water volume (documented), against downstream floodplain inundation
peaking at 464.18 km² on 9 June 2023 before receding to 21.17 km² by 21 June — presented as
supporting descriptive evidence of physical scale alongside the statistically validated NDVI
DiD result, rather than as an independently causally-tested finding.

----------------------------------------------------------------------------------------------------

## Geospatial Visualization, Dashboard, and Documentation (Modules 7–9)

With the causal model, event study, and flood-extent analysis complete, the remaining modules
converted the statistical results into publication-grade outputs.

**Module 7 — Geospatial Visualization**: A set of static maps and plots was produced from the
validated data — the study-area overview (treatment/control zone boundaries), before/after
true-colour imagery of the Kakhovka reservoir, the DiD regression result, the monthly NDVI
comparison, the verified flood hydrograph, and the quarterly event-study chart — matching the
figures referenced throughout Research_Paper.md. An interactive QGIS2Web flood-extent map was
also built from the UNOSAT polygons for the dashboard's Interactive Maps page.

**Module 8 — Dashboard & Deployment**: A multi-page Streamlit dashboard was built (overview page
plus eight sub-pages: Study Design, Flood Analysis, Vegetation Impact, Statistical Validation,
Explore Trends, Satellite Evidence, Interactive Maps, and Methodology & Data), presenting every
finding — including the honestly disclosed narrowed-baseline limitation — in an interactive,
non-technical format. The dashboard was deployed to Streamlit Community Cloud and linked from the
project's GitHub repository.

**Module 9 — Documentation**: ECO_Project_Report.md, ECO_Research_Paper.md, and this development log
were finalized, and README.md was written to summarize the project, its findings, and its
reproducible pipeline for a GitHub audience. The repository was published to GitHub.

----------------------------------------------------------------------------------------------------

## Panel-Readiness Review and Robustness Pass

### Motivation

With the project functionally complete — causal analysis, dashboard, and documentation all
finished — the project was reviewed once more end-to-end against the kind of scrutiny an Erasmus
Mundus GEM/CDE scholarship panel would apply: whether the standard-error specification was
appropriate for a two-unit comparative time series, whether the reference list met academic
standards, whether the reported figures were internally consistent across every document, and
whether the repository's security hygiene held up to public scrutiny.

### Standard-Error Correction

The original models used classical OLS standard errors throughout. On reflection, these are not
the right choice for this design: with only two geographic units (Kherson as treatment, Tulcea as
control) observed monthly over time, cluster-robust standard errors — the correction used in this
researcher's prior multi-country panel work — are degenerate, since cluster-robust inference
requires many independent clusters, not two. The appropriate correction for a small number of long
time series is Newey-West HAC (heteroskedasticity- and autocorrelation-consistent) standard
errors, which was applied to all five causal-inference scripts (`did_model.py`,
`did_model_narrowed.py`, `placebo_test.py`, `placebo_narrowed.py`, `event_study.py`).

The main finding and the narrowed-baseline point estimate both survive this correction — the
narrowed-baseline estimate in fact becomes *more* significant, not less. The one substantive
change is that the narrowed-baseline placebo test, previously reported as merely "ambiguous"
under classical standard errors, becomes statistically significant under HAC — meaning it fails
outright as a validation check rather than sitting in an unresolved middle ground. This is now
reported plainly as a validation failure throughout Research_Paper.md, Project_Journal.md, and
the dashboard, rather than the softer "ambiguous" framing used previously. It does not change the
project's primary conclusion, since the broader-baseline result's own placebo test remains clean
under the same correction.

### Other Fixes Applied

- **Figure numbering** in Research_Paper.md was corrected — a stray decimal sub-figure and a
  missing figure number were resolved into a clean sequential 1–6 sequence.
- **References** were rewritten with complete, verifiable citation details, replacing incomplete
  entries and a placeholder journal name.
- **Confidence intervals** were added alongside every reported coefficient and p-value, and a new
  Robustness Checks subsection was added to Research_Paper.md summarizing the classical-versus-HAC
  comparison in full.
- **`requirements.txt`** was audited against actual imports across every script in the repository
  and corrected — two unused packages were dropped and two actually-used packages that were
  missing were added.
- **The dashboard's PDF download buttons** used paths relative to the working directory, which
  fails when the app is served from Streamlit Cloud (the working directory there is not the repo
  root); this was fixed to resolve paths relative to the script's own location, with a graceful
  fallback if a file is genuinely missing.
- **Repository security**: the `.env` file containing live API credentials had been committed to
  the public repository, because `.gitignore` never excluded it. The committed file was replaced
  with placeholders, `.gitignore` was corrected to exclude `.env` and similar credential files
  going forward, and the live credentials are being rotated at the provider separately from this
  documentation pass.
- A `LICENSE` (CC BY 4.0) and `CITATION.cff` were added ahead of the project's Zenodo archival, and
  every dashboard page and document referencing the project's statistics was updated to keep the
  HAC-corrected figures consistent throughout.

---

# Development Log — Deep Verify: Independent Recomputation of Every Reported Statistic (2026-08-03)

## Status

Complete. Everything matched exactly — no discrepancies found.

## Method

Every quantitative claim in `Research_Paper.md` was independently recomputed by re-running this project's own scripts (`did_model.py`, `did_model_narrowed.py`, `placebo_test.py`, `placebo_narrowed.py`, `event_study.py`) directly against the raw `data/ndvi/kherson_ndvi_monthly.json` / `tulcea_ndvi_monthly.json` files, plus independently re-deriving the flood-extent areas from the raw UNOSAT shapefiles (`ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp`, `ST3_20230609_FloodExtent_KhersonskaOblast_UKR.shp`, `ST1_20230621_FloodExtent_KhersonskarOblast_UKR.shp`) using the same EPSG:6933 equal-area reprojection `water_loss_summary.py` uses, and re-implementing the pre-treatment covariate-balance test (§3.4) from scratch since it has no standalone script.

## What was independently reproduced and confirmed exact

- **§3.4 Pre-Treatment Covariate Balance:** re-derived from the raw NDVI series (Jan 2022–May 2023): Kherson n=17, mean=0.222, SD=0.074; Tulcea n=17, mean=0.203, SD=0.110; two-sample t-test p=0.553. Seasonal amplitude (max−min over the pre-period): Tulcea 0.351, Kherson 0.274. The DiD model's own `treatment` main-effect term: 0.0193 (paper rounds to 0.019), HAC p=0.347. All match exactly.
- **§4.1 Flood Extent:** re-read the three raw UNOSAT flood-extent shapefiles and reprojected to EPSG:6933 for area calculation: 122.50 km² (6 June), 464.18 km² (9 June, the peak), 21.17 km² (21 June) — all match exactly. (The paper's "~4.3% of ~10,800 km² downstream corridor" figure is itself explicitly hedged as an approximate scale indicator — 464.18/10,800 = 4.30%, internally consistent with the stated corridor figure, though the corridor-area figure itself has no dedicated computation script to independently re-derive.)
- **§4.2 Vegetation Impact — Main DiD model:** re-ran `did_model.py`: did_term coefficient = −0.0703, HAC p = 0.022, 95% CI [−0.130, −0.010], R² = 0.747. Classical OLS: p = 0.0070, 95% CI [−0.1206, −0.0200]. All match exactly, including both the HAC and classical figures reported side-by-side in §4.4's table.
- **§4.2 Placebo test (broad baseline):** re-ran `placebo_test.py`: coefficient = 0.0148, HAC p = 0.6124; classical p = 0.7411. Matches exactly.
- **§4.3 Narrowed-baseline DiD:** re-ran `did_model_narrowed.py`: coefficient = −0.1384, HAC p = 0.000129 (paper: <0.0001, rounds correctly), 95% CI [−0.209, −0.068]; classical p = 0.0019 (paper: 0.002). Matches exactly.
- **§4.3 Narrowed-baseline placebo:** re-ran `placebo_narrowed.py`: coefficient = −0.1382, HAC p = 0.0011 (paper: 0.001); classical p = 0.1687 (paper: 0.169). Matches exactly — including the specific "classical non-significant, HAC significant" validation-failure pattern the paper calls out as the key finding of this test.
- **§4.3 Event study:** re-ran `event_study.py`'s full quarterly-bin regression. Treatment quarter (rel_quarter 0): p=0.0053 (paper: HAC p=0.005). Following quarter (rel_quarter +1): p=0.0233 (paper: HAC p=0.023). One year later (rel_quarter +4, i.e. 12–15 months post-event): p=0.0000 (paper: HAC p<0.0001). Pre-treatment quarter, summer 2022 (rel_quarter −4, correctly identified via `rel_month = (year−2023)×12+(month−6)`): p=0.0004 (paper: HAC p<0.001). All four cited quarters match exactly, including the specific "pre-treatment anomaly" the paper reports as a disclosed limitation rather than concealing it.
- **§4.2 "~32% relative decline" framing:** −0.0703 / 0.222 (Kherson's own pre-period mean, §3.4) = −31.7%, which the paper correctly rounds to "approximately 32%."

## What could not be independently re-derived

The "~10,800 km² downstream analysis corridor" figure used to compute the ~4.3% peak-flood-coverage statistic (§4.1) has no dedicated script producing it in this repository — it appears to be a manually-estimated corridor extent. The percentage itself is arithmetically consistent with the stated corridor area (464.18/10,800 = 4.30%), and the paper already explicitly hedges this framing ("roughly," "approximately," and "a scale indicator... not a substitute for" the statistical result), so this is noted rather than treated as a discrepancy.

## Citation spot-check

Spot-checked 3 of 6 references: Atılgan Pazvantoğlu (2025), *Ecocide as a separate crime under the Rome Statute: A legal analysis of the discourse*, Environmental Policy and Law 55(2–3), 57–67 — confirmed real on SAGE Journals, exact title match. Wang, Raymond, Gould & Baker (2013), *Problems from hell, solution in the heavens?*, Stability: International Journal of Security and Development 2(3), Art. 53 — confirmed real, exact title and DOI match. The paper's core factual claim (Vanuatu/Fiji/Samoa's September 2024 Rome Statute ecocide amendment proposal, cited to Stop Ecocide International 2024) was independently confirmed against Stop Ecocide International's own published article. No problems found in the 3 spot-checked; Kroker (2015), Newey & West (1987, a very well-established econometrics reference), and the Rome Statute primary-source citation were not individually re-verified this pass.

## Outcome

This is the cleanest Deep Verify pass across the portfolio so far — every single independently re-derivable statistic (pre-treatment balance test, all four causal models under both classical and HAC standard errors, all four cited event-study quarters, and all three flood-extent measurements) matched the paper exactly, with no fixes required to `Research_Paper.md`, `Project_Journal.md`, or the dashboard.

---

# Development Log — The Control-Zone Expansion — From a Single Control to a Small Panel (2026-08-13)

## Status

Complete. Ran the acquisition, ran all three multi-control scripts, and the results are in the paper, the project report, and the README now.

## Why this is next

Section 6 of the research paper already names the headline limitation plainly: this whole causal design rests on a single treatment zone (Kherson) against a single control zone (Tulcea), which is exactly why cluster-robust standard errors were never an option and Newey-West HAC had to carry the whole burden of correcting for serial correlation. Section 7's own Future Work list names the fix — either a Synthetic Control Method built from several candidate controls, or a more modest control-zone sensitivity check against two or three alternatives. I'm doing the second one first, since it's the more direct test of whether the −0.0703 result is really about Kherson specifically or just an artifact of Tulcea being the one control I happened to pick.

## Picking the new control counties

Tulcea was chosen originally for ecological comparability (Danube Delta biosphere character) and genuinely non-combatant status. I stayed inside that same logic rather than reaching for a geographically distant, harder-to-defend control: Galați, Brăila, and Constanța are the three Romanian counties bordering Tulcea along the same Danube/Black Sea corridor, all non-combatant, all with a broadly similar floodplain/deltaic/coastal land-cover mix. Their GADM Level 1 areas run 9,185–13,749 km², against Tulcea's 16,968 km² — not identical, but the same rough order of magnitude, not a Rhode-Island-versus-Texas mismatch.

I pulled their boundaries straight out of the `gadm41_ROU.gpkg` file I already had on disk from the original Tulcea extraction, rather than downloading anything new — `extract_control_zone_boundaries.py` does this and writes `galati_county.gpkg`, `constanta_county.gpkg`, and `braila_county.gpkg` alongside the existing `tulcea_county.gpkg`. Bounding boxes for the Sentinel Hub Statistical API pull come straight from those GADM geometries' `total_bounds`, the same way the original `kherson`/`tulcea` bboxes in `download_ndvi.py` were derived.

## What's ready to run

`download_ndvi_control_zones.py` mirrors `download_ndvi.py` exactly — same evalscript, same `2022-01-01` to `2024-12-31` window, same monthly aggregation — pointed at the three new bboxes instead of Kherson/Tulcea. I haven't run it yet; it needs my own Sentinel Hub client credentials from `.env`, and I'm not putting API keys through anything other than my own machine.

Once `data/ndvi/galati_ndvi_monthly.json`, `constanta_ndvi_monthly.json`, and `braila_ndvi_monthly.json` exist, three new scripts are ready to consume them:

- `did_model_multi_control.py` — the same DiD specification as the original `did_model.py`, but stacked across all four control zones instead of one. Reports both a cluster-robust model (clustered by zone) and, for direct comparability, the same HAC specification the original paper used. Also runs a per-zone check — Kherson against each control individually — so I can see immediately if the pooled result is being carried by one control zone rather than holding up across all four.
- `placebo_test_multi_control.py` — same fake-treatment-date logic as the original placebo test, run on the five-zone panel with cluster-robust SEs.
- `event_study_multi_control.py` — the same quarterly event-study design as `event_study.py`, generalized across the panel.

## An honest note on what "cluster-robust" buys me here

Five clusters (one treatment, four control) is a real improvement over two — it's the minimum for cluster-robust inference to even be *defined* — but it's still well short of the 30-40+ clusters the asymptotic theory behind cluster-robust standard errors actually assumes. Few-cluster settings are a known problem in applied econometrics; standard errors can be understated in exactly this regime. I'm reporting the cluster-robust result as a genuine step toward addressing Section 6's limitation, not as a claim that this now matches a properly powered multi-unit panel — and I'm keeping the HAC specification alongside it for that reason, the same way the original paper reported HAC next to classical OLS rather than picking one and hiding the other.

## Running it, and what came back

Ran `download_ndvi_control_zones.py`. All three new zones came back clean — same 35 monthly points as Kherson and Tulcea, no failed requests, NDVI ranges that look like real vegetation signal (Galați and Brăila both run a bit greener on average than Tulcea, Constanța sits in between — not a red flag, just three different landscapes).

**The pooled result holds.** Across all four controls, did_term = −0.0600 (HAC p = 0.029, 95% CI [−0.114, −0.006]; cluster-robust p = 0.002, 95% CI [−0.097, −0.023]) — a bit smaller than the original −0.0703, same direction, not close to zero. The placebo test on the same four-control panel comes back clean too (coefficient +0.0222, wrong sign, p = 0.216).

**The per-zone breakdown is the more interesting result, and I'm not folding it quietly into the pooled number.** Tulcea (−0.0703, p = 0.022), Galați (−0.0695, p = 0.026), and Brăila (−0.0937, p < 0.001) each reproduce a significant effect on their own. Constanța doesn't (−0.0064, p = 0.808). I looked at what's different about it before writing this up: it's the most purely Black Sea coastal, most urbanized of the four — less of the Danube floodplain/deltaic wetland character the other three share more directly with the treatment zone's own river-delta setting. That's a plausible explanation, not a confirmed one — I don't have a land-cover breakdown to actually test it, so it goes in Future Work rather than into the results section as settled fact.

**The cluster-robust standard errors themselves come with an honest asterisk.** Even on the pooled DiD model, statsmodels flags the cluster covariance matrix as rank-deficient (rank 4 of 14 constraints) — 5 clusters just isn't enough for the full asymptotic theory to hold, though `did_term`'s own standard error still came out sane. It gets worse, not just theoretically but numerically, on the event study: with ~24 parameters (12 month dummies, treatment, ~11 quarterly event terms) and only 5 clusters, several coefficients came back with standard errors on the order of 1e-16 — not real precision, a genuine computational breakdown from too many parameters relative to too few clusters. I caught this by actually reading the printed output rather than trusting the p-values at face value, and I'm reporting the HAC version of that specific model instead, with the cluster-robust numbers shown only to document why they're not used.

**The event study itself tells a different story than the original two-zone version.** Under HAC on the four-control panel, the exact treatment quarter is no longer significant (p = 0.972, versus p = 0.005 in the original two-zone design), while the quarter-and-a-year-later effect still is (p = 0.011). I'm not trying to reconcile this into a single clean story — the pooled, non-quarterly DiD result is robust to widening the control side; the fine-grained quarterly timing story is genuinely noisier once averaged across four ecologically different controls instead of one. Both statements are true and both are now in Section 4.5 of the paper.

**What went into the documentation.** A new figure (`map7_control_panel_comparison.py` → `outputs/plots/control_panel_comparison.png`), a new Section 4.5 in the research paper covering all of the above, updated Section 6 and 7 (the "single treatment-control pair" limitation is now a "5-cluster, not 30-40-cluster" limitation, and "control-zone sensitivity analysis" came off the Future Work list since it's done — replaced with the sharper, more specific "explain why Constanța differs" and "get to a genuinely large cluster count" items), the Project Report's Methodology and Limitations sections, and the README's Key Findings.

## What's still open

Why Constanța doesn't reproduce the effect is a real open question, not a solved one — Future Work now names a land-cover comparison as the way to actually test the coastal-versus-deltaic explanation rather than just assert it. And getting cluster-robust inference to a trustworthy cluster count would mean going beyond Romania entirely — Bulgarian or Moldovan counterparts along the same basin — which is a considerably bigger acquisition and boundary-matching effort than this pass, and stays on the list rather than getting attempted here.


## Retiring QGIS2Web for the Flood-Extent Map

Wanted this map built the same way GHOST_INFRASTRUCTURE's and DOUBLE_JEOPARDY's interactive maps now are — directly in Python (folium) instead of round-tripping through a QGIS project file and the QGIS2Web plugin export. `build_kherson_flood_map.py` reads the same three verified UNOSAT flood-extent shapefiles `map4_flood_extent_geospatial.py` already uses for the static PNG version (`ST3_20230606`, `ST3_20230609`, `ST1_20230621`), same colors (orange/red/cyan for 6/9/21 June), same Kherson Oblast boundary outline.

Each date's shapefile is a single MultiPolygon with a lot of detail baked in — 20K to 133K vertices depending on the date — so geometry gets simplified (0.0002°, well under anything visible at this zoom) before rendering, same approach as DOUBLE_JEOPARDY's ecosystem buffer maps. Also had to drop the shapefiles' attribute columns before handing geometry to folium — one of them (`Sensor_Dat`) comes in as a raw pandas Timestamp, which folium's GeoJson serializer can't JSON-encode, and none of those columns were going in the popup anyway (date and area are already written directly into the popup HTML from the filename and `Area_ha`). Output is 2.6MB, well within what GitHub Pages and the dashboard's `components.iframe()` already handle fine for the other maps.

Feature counts and area figures match the existing static map exactly (12,250 ha on 6 June, peaking at 46,418 ha on 9 June, down to 2,117 ha by 21 June recession) — confirms this is the same verified UNOSAT data, just rendered differently. Updated the dashboard's Interactive Maps page intro and footer caption, README's tech stack and repo-structure comment, and the Project Report's Deliverables line to say Python (folium) instead of QGIS. The old `qgis_processing/kherson_flood_extent_webmap/` export is left in place as unused legacy content — this app doesn't have a way to delete files on its own, so it stays until removed by hand.
