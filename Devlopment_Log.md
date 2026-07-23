# ECOCIDE: A Causal-Inference Framework for Independently Verifying War-Time Environmental Damage

## Project Overview

ECOCIDE is a geospatial causal-inference framework designed to independently verify claims of environmental destruction arising from armed conflict, using Earth Observation (EO) data, remote sensing, and statistical causal-inference methods. In recent years, international legal bodies have begun formally considering the recognition of mass environmental destruction — "ecocide" — as a prosecutable international crime, alongside genocide, crimes against humanity, war crimes, and aggression.

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

Project Concept Finalized (Sharpened following literature review)
Version 2.0

----------------------------------------------------------------------------------------------------

# ECOCIDE — Module Architecture

# MODULE 1 — Project Conceptualization & Literature Review
Research question, aim, and objectives finalized. Existing literature on satellite-based conflict-environment assessment reviewed in depth, identifying the specific methodological gap this project addresses: existing geospatial assessments of war-related environmental damage rely on qualitative, visual before-after image interpretation and explicitly decline to establish statistical causality. No existing framework applies a genuine causal-inference design — matched control zone, Difference-in-Differences model, placebo validation — to conflict-attributable environmental damage.

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

# Development Log — ECOCIDE

## Study Area & Control Zone — Decision Log

**Conflict (Treatment) Zone**: Kakhovka Dam area and Dnipro River downstream floodplain (46.777°N, 33.370°E), Kherson Oblast, Ukraine. Dam destroyed 6 June 2023. Flood-affected analysis zone spans approximately 10,800 km² (dam to river mouth, per UNOSAT satellite analysis).

**Control Zone Selection Process**: A within-Ukraine non-frontline control zone (e.g., Dnipropetrovsk Oblast) was initially considered, but rejected — recent reporting indicates the frontline has moved closer to this region, and war-adjacent economic and demographic effects (supply disruption, displacement) could contaminate a control zone even without direct conflict in that specific area. This mirrors a methodological risk identified in prior work (GPIE), where an internal-to-the-affected-region control group proved insufficiently independent.

**Control Zone Selected**: Danube Delta, Tulcea County, Romania (45.200°N, 29.500°E). Selected for a comparable pre-conflict ecological baseline — river-delta wetland, Pannonian steppe, agricultural floodplain, similar continental climate — while being genuinely non-combatant. Explicitly verified as distinct from the Ukrainian side of the Danube Delta (Odesa Oblast), which has itself been affected by war-related strikes on Danube port infrastructure and is therefore unsuitable as a control.

---

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

