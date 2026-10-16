# ECOCIDE v2 — Registered Revision 2

Version 1.0 · approved 16 October 2026 · Sakshi D. Maske

## Status of this document

`ANALYSIS_PLAN_v2.md` (commit 521672f) and `ANALYSIS_PLAN_v2_ADDENDUM_1.md` (commit 30e3840) have been run, and their
results are reported unchanged. This addendum is written **after** those results and after the exploratory review
checks in `v2/analysis/x1_review_diagnostics.py` were known (`v2/DEVIATIONS.md` §5). It is written **before**:

- the new data it needs are downloaded (independent irrigation maps, Copernicus DEM, Sentinel-2 August 2024), and
- any of the analyses below are run.

Its results will be reported as **registered-revision-2 results**, next to, never instead of, the earlier ones.

**Timestamp.** This addendum was approved and committed to the local git repository on 16 October 2026. It was not
deposited with an independent registry, and the repository is not pushed to GitHub until the project is finished, so
the only record of its date is the git commit, which the author controls. Readers should weigh it accordingly. The
SHA-256 checksum of this file at approval is recorded in `v2/DEVIATIONS.md` §6; the analysis code checks it before
running.

## Problems found after Revision 1

| # | Problem | Evidence |
|---|---|---|
| P6 | Weather can change the irrigated–rainfed contrast, but enters the H2 models only additively. | Zone-K July–October rain 2016–2024: 131, 115, 129, 141, 131, 161, 118, 67, 94 mm; r = −0.97 between the revision's 2016–2021 event-study coefficients and this rain. |
| P7 | The event-study reference year (2021) is the wettest year of the record. | As above. |
| P8 | Comparison land and placebo districts include land irrigated from the Kakhovka network beyond 5 km of OSM canals. | The four most negative revision placebo districts have 2–86 % of their cropland in zone K. |
| P9 | "Irrigated" is an NDVI proxy that mostly captures summer cropping. | 95 % of classified steppe cropland outside zone K is labelled irrigated. |
| P10 | H1 matching uses the pre-war outcome itself: a flat pre-trend is mechanical, regression to the mean is possible, and only 1.8 % of flooded pixels are matched. | `h1_results.json` balance and matching diagnostics. |
| P11 | Clustered and Conley errors work at 10–25 km, but each treatment is one connected area. | One canal zone; one flood corridor. |

## Definitions used below

- **Two oblasts:** Kherson and Zaporizhzhia (GADM level 1), the area covered by the maps of Baber et al. (2026b).
- **Cropland pixel:** as in the plan: `universe`, WorldCover 2021 crop share ≥ 60 %, not reservoir bed, not flooded
  (`F`), not touched by any June 2023 UNOSAT flood layer, not the Dnipro channel.
- **Irrigated fraction** of a pixel in year y (2019, 2020, 2021): share of the 30 m map cells inside the 231 m pixel
  that the map labels irrigated (value 1; if a file stores probabilities, p ≥ 0.5), computed by area-weighted
  averaging onto the grid; map no-data cells are left out of the share, and pixels with less than 50 % map coverage
  are left out of R9 altogether.
- **Contains a mapped field:** irrigated fraction ≥ 5 % in at least one year 2019–2021.
- **Canal-fed:** within 30 km of the OSM Kakhovka canal network (`dist_net` ≤ 30 km).
- **Relative height:** Copernicus DEM GLO-30 mean elevation of the pixel minus the DEM elevation of the nearest pixel
  of the river line the pixel is matched along (the Dnipro main channel for H1; the traced placebo river for the
  placebo floodplains).

## R6 — Weather-dependent contrast (P6)

In every H2 model of this revision, July–October precipitation (P, per 100 mm) and mean temperature (T, °C) enter on
their own and interacted with each group indicator of the design (and with their product in the triple difference).
P and T are centred at their 2016–2021 means over the irrigated pixels before the interactions are formed, so the
reported β is the effect at that average weather. No SPEI sensitivity check.

## R7 — Reference period (P7)

Event studies of this revision are estimated with the year 2018 left out and reported relative to the 2016–2018 mean
(primary) and relative to 2021 (as before), both as linear transformations of the same coefficients. The pre-trend
test is the joint test that all pre-war coefficients (2016, 2017, 2019, 2020, 2021, relative to 2018) are zero.

## R8 — Comparison land (P8)

The zone O of this revision (used as the H4 reference area; the R9 design itself has no zone O) must lie more than
30 km from the OSM Kakhovka canal network used in the plan. In the two oblasts, land within 5 km of a pixel that
contains a mapped field is also excluded from it. The Revision 1 triple difference and its placebo districts are not
re-estimated.

## R9 — Independent irrigation exposure (P9)

Exposure: the irrigated fractions above from the random-forest v6 maps of Baber et al. (2026b; Zenodo record
22036773, CC BY 4.0) for 2019, 2020 and 2021, and their mean. The 2022–2025 maps are used only to describe the decline.

- **Validation:** cross-tabulate the R1 classes (irrigated / rainfed / unclassified, 2010–2015) against the R9
  classes (irrigated / never irrigated / neither) on cropland of the two oblasts, per oblast, and report the table.
- **Groups.** *Irrigated:* cropland pixels of the two oblasts with mean irrigated fraction ≥ 50 % in 2019–2021 that
  are canal-fed. *Never irrigated:* cropland pixels of the two oblasts with irrigated fraction < 5 % in each year
  2019–2021 that lie more than 5 km from any pixel containing a mapped field. If either group has fewer than 1,000
  pixels in the fixed panel, the 5 km distance is reduced to 2 km; there is no other fallback.
- **Model (primary H2 test of this revision):** pixel fixed effects; year × oblast and year × occupation fixed
  effects (occupation as in R4; a year × group effect would absorb β); conflict intensity (R4); the R6 weather terms; and the indicators Irr × Post (β; 2023–24),
  Irr × War (2022) and Irr × Def (2019–2021, the years that define the groups). β therefore compares 2023–24 with
  2016–2018. Fixed panel: at least 7 of the 9 years valid. Standard errors clustered by raion (GADM level 2).
- **Event study** as in R7. With a full set of year × group indicators the weather × group slopes are barely
  identified when weather varies mostly between years, so in the event study they are fixed at their main-model
  estimates (the outcome is adjusted by them); its standard errors do not include this first step.
- **Placebo test:** the same model on 2016–2021 only (fixed panel: at least 5 of the 6 years), with
  Irr × (2019–2021) as the "effect" and 2016–2018 as baseline.
- **Second comparison (only if feasible):** if at least 1,000 pixels of the two oblasts have mean irrigated fraction
  ≥ 50 % and are *not* canal-fed, they form a group whose water supply did not depend on the reservoir. The triple
  difference then adds year × Irr and year × Canal effects (Canal = canal-fed, for every pixel) and reports
  Irr × Canal × Post. Otherwise this test is not
  run, and the paper says so.
- **Outcome window:** July–October NDVI as in the plan. Baber et al. (2026a) report a shift to winter crops after the
  breach; this window does not capture it, and the paper says so.

## R10 — Flood matching on non-outcome covariates (P10)

All H1 models of this revision use the Revision 1 model and data (R4 band fixed effects and conflict, R5 water rule).

- **Placebo in time:** match on 2016–2018 NDVI only (same strata, k, caliper) and estimate, on 2016–2021 (fixed
  panel: at least 5 of the 6 years), the "effect" for 2019–2021. A non-zero estimate measures the bias from matching on the outcome.
- **Covariate matching (primary H1 test of this revision):** Mahalanobis matching within bank × dominant-class strata
  on relative height and the WorldCover shares of tree, shrub, grass, crop, built, bare, water and wetland (distance
  to the main channel is handled by the R4 band fixed effects, not by matching); 3 controls with replacement; caliper
  0.25 SD as in the plan. Report the share of flooded pixels matched, balance on these covariates and on 2016–2021
  NDVI.
- **Overlap rule:** flooded land is low land, so matching on height may find few comparable controls. If fewer than
  25 % of flooded pixels are matched, the matched estimate is reported but the primary H1 estimate of this revision
  is the unmatched one below, with its own placebo-floodplain randomization p. This is the only fallback.
- The unmatched estimate (all flooded pixels in the fixed panel against all candidate controls) is reported next to
  the matched one as the area-representative estimate.

## R11 — Inference at the scale of treatment (P11)

- **H1:** the randomization p from the placebo floodplains, each analysed with the R10 covariate matching (or
  without matching, under the overlap rule), is the primary randomization p. Wild cluster bootstrap and Conley errors (25, 50, 100 km) are also reported.
- **H2 (R9):** exposure varies field by field across many raions, so the primary p is the wild cluster bootstrap
  p with raions as clusters; Conley errors with 25, 50 and 100 km cut-offs are also reported. There is no regional
  placebo design for R9; the placebo test of R9 takes the place of the randomization condition in the decision rule.

## H4 under this revision

Kherson Oblast change from the 2016–2018 mean to the 2023–2024 mean, by category: flooded land (F), former reservoir
bed, R9 irrigated cropland (mean fraction ≥ 50 %, canal-fed or not), R9 never-irrigated cropland (< 5 % in each year,
without the distance rule), other cropland, all other land. Each pixel's change is
adjusted for weather with the P and T coefficients of the R9 model (the group-specific ones for irrigated pixels).
Reference changes come from the area of the new zone O (the R8 distance rules applied to all land in the steppe
oblasts, not only cropland): its cropland for the three cropland categories, the same dominant-class mix for the
rest; the reservoir bed is reported raw. The R5 water rule applies; each pixel needs at least one valid year in
2016–2018 and one in 2023–2024; area shares are held fixed in the bootstrap. 95 % intervals from a block bootstrap (10 km blocks, 999 draws,
blocks resampled separately inside Kherson Oblast and inside zone O). If the interval of the irrigated-cropland
contribution includes zero, H4 is reported as descriptive only.

## R12 — Independent check of H3

Sentinel-2 L2A scenes of 1–31 August 2024 over the former reservoir bed (Planetary Computer `sentinel-2-l2a`, scenes
with less than 60 % cloud) are read on the study's 23.2 m fine grid; clouds, cloud shadow, cirrus, snow and saturated
pixels are masked with the scene classification band, and each fine pixel's August median NDVI is computed. The
check compares the 2024 area with NDVI > 0.3 on the bed from MODIS (Revision 1 H3, land pixel-years) with the
Sentinel-2 area with August median NDVI > 0.3 over the same bed pixels. Both areas and their ratio are reported. No
test, no further analysis.

## Decision rule

The plan's rule (§7) is applied with these inputs: Holm correction over the two primary tests of this revision
(H1 primary WCR p — covariate-matched, or unmatched under the overlap rule; H2 R9 WCR p); the Rambachan–Roth M̄ = 1 interval from the R7 event study (reference
2018, all pre-war years as pre-period); and as the third condition, for H1 the placebo-floodplain randomization
p < 0.10 and for H2 a placebo-test estimate with p ≥ 0.10. Each analysis is run once as written; results are
reported whatever they show, using the stopping rules in `RESEARCH_COMPLETION_PLAN.md` §6.

## Data to obtain (after this addendum is committed)

1. Baber et al. (2026b) irrigation maps, 2019–2025 (`v2/09_download_irrigation_maps.py`).
2. Copernicus DEM GLO-30, mean elevation per grid pixel (`v2/10_download_dem.py`).
3. Sentinel-2 L2A, August 2024, over the former reservoir bed (`v2/11_download_s2_reservoir.py`).

Not used in this revision: SPEI, MODIS 2025, official irrigation-system maps.

## References

Baber, S., et al. (2026a). A semi-supervised multi-sensor remote sensing pipeline for mapping irrigation dynamics in
ground-truth deficient conflict zones: A case study of the Kakhovka Dam failure. *Frontiers in Remote Sensing*, 7,
1920951. https://doi.org/10.3389/frsen.2026.1920951

Baber, S., et al. (2026b). *Irrigation of Kherson and Zaporizhzhia 2019–2025* [Data set]. Zenodo.
https://doi.org/10.5281/zenodo.22036773
