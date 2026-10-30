# ECOCIDE v2 — Pre-registered Analysis Plan

**Pixel-level, exposure-based study of vegetation change after the Kakhovka Dam destruction**

Version 1.0 · written 24 September 2026, **before any v2 data were downloaded or inspected** · Sakshi D. Maske

This plan is frozen by committing it to the public GitHub repository before the download scripts in `v2/` are run. The commit timestamp is the registration date. Any later change is recorded, with its date and reason, in `v2/DEVIATIONS.md`; the paper will report every deviation. Results that do not follow this plan will be labelled *exploratory*.

---

## 1. Why a second design

The first analysis (Study 1; `ECO_Research_Paper.md` before v2) compared the oblast-wide mean NDVI of Kherson Oblast with four Romanian counties. It found a statistically significant relative decline after June 2023, but it could not attribute that decline to the dam, for reasons that are properties of the design:

1. The treated unit (≈25,500 km²) is not the exposed area (flood ≈ 2% of it).
2. Parallel trends were violated (4 of 5 pre-event quarters) with only 17 pre-event months, all during the war.
3. The controls were in another country, with different land cover, agriculture and policy.
4. War and weather were not separated from the dam's effects.
5. Results changed across three data versions; the design invited forking paths.
6. Five units cannot support randomization inference (minimum p = 0.20).
7. Monthly means were taken over a changing set of valid pixels.
8. NDVI over cropland mixes vegetation damage with farming decisions.
9. 35 monthly observations of one treated unit.
10. The mechanism (flood vs irrigation loss vs war) was not tested.

Study 2 addresses these by moving to 231 m pixels, defining treatment by **exposure**, comparing exposed and unexposed land **inside the same war zone**, using a **2016–2024** record, and fixing every analytical choice in advance.

## 2. Questions and hypotheses

- **H1 — Flood.** Land flooded after the dam breach (6–9 June 2023) had lower July–October NDVI in 2023–2024, relative to comparable unflooded land on the same river bank, than it had in 2016–2021.
- **H2 — Irrigation loss.** Cropland irrigated before the war and served by the Kakhovka reservoir's canal network had lower July–October NDVI in 2023–2024, relative to rainfed cropland in the same zone, than the same irrigated–rainfed contrast outside that zone (triple difference).
- **H3 — Reservoir bed (descriptive).** Vegetation development on the drained reservoir bed is described; there is no counterfactual.
- **H4 — Decomposition (descriptive).** The oblast-level decline found in Study 1 is decomposed into the contributions of flooded land, the former reservoir bed, Kakhovka-irrigated cropland and all other land.

H1 and H2 are the **two primary confirmatory hypotheses**. Everything else is secondary or descriptive.

## 3. Data

| Dataset | Use | Access |
|---|---|---|
| MODIS Terra MOD13Q1 v6.1, 16-day, 250 m, 2016–2024 (NDVI, EVI, pixel reliability, composite day-of-year) | Outcomes | Microsoft Planetary Computer `modis-13Q1-061` |
| ESA WorldCover 2021 v200, 10 m | Land-cover class and fractions per pixel | Planetary Computer `esa-worldcover` |
| UNOSAT FL20230606UKR | Flood exposure (6–9 June composite; all June layers for exclusion); pre-breach water extent | Already in `data/ndwi/FL20230606UKR_SHP.zip` |
| ERA5-Land monthly means, 2015–2024 (2 m temperature, precipitation, top-layer soil moisture) | Weather covariates | Copernicus Climate Data Store |
| OpenStreetMap `waterway=canal` | Irrigation network | Overpass API |
| GADM v4.1 (Ukraine, levels 0–2) | Country/oblast masks | Already in `data/boundaries/` |

All rasters are placed on one grid (`v2/grid.py`): EPSG:3035, 231.656 m pixels, 29.0–36.5 °E × 45.3–49.3 °N.

## 4. Units and exposure definitions

### 4.0 Pixel universe
Grid pixels inside Ukraine (GADM level 0), **excluding Crimea** (Autonomous Republic of Crimea and Sevastopol: canal supply from Kakhovka restarted in 2022 and conditions are not comparable), with WorldCover valid coverage ≥ 90%. Each pixel's *dominant class* is the WorldCover class with the largest fraction; a pixel is *pure* if that fraction is ≥ 60%.

### 4.1 Flood exposure (H1)
- **Flooded (F):** ≥ 50% of the pixel inside the UNOSAT cumulative 6–9 June 2023 flood polygon, and WorldCover water < 20%.
- **Excluded:** pixels 10–50% flooded; pixels flooded in any other June 2023 UNOSAT layer but not in the composite.
- **Candidate controls (C):** 0% in every June 2023 UNOSAT flood layer; 2–15 km from the nearest flooded pixel; WorldCover water < 20%; not reservoir bed (4.2).
- **Bank:** each pixel is assigned to the left (south/east) or right (north/west) bank of the Dnipro according to which side of the Dnipro main channel (WorldCover water, dam to estuary) it lies on. Treated and control pixels are only compared within the same bank; the left bank was occupied throughout 2023–2024, the right bank was not after November 2022.
- **Matching:** within each bank × dominant-class stratum, each flooded pixel is matched to 3 control pixels (with replacement) by Mahalanobis distance on its six July–October mean NDVI values for 2016–2021; caliper 0.25 SD of the distance; unmatched flooded pixels are dropped and counted.

### 4.2 Former reservoir bed (H3)
Pixels with WorldCover water ≥ 50% that belong to the Kakhovka reservoir: the connected water body between the Kakhovka dam (33.37 °E, 46.78 °N) and the Dnipro hydroelectric dam at Zaporizhzhia (35.08 °E, 47.87 °N).

### 4.3 Irrigation exposure (H2)
- **Cropland:** WorldCover crop ≥ 60%.
- **Irrigated before the war:** mean July–August NDVI ≥ 0.45 in at least 3 of the 5 years 2017–2021. **Rainfed:** mean July–August NDVI < 0.35 in at least 4 of those 5 years. Other cropland is excluded. (In this dry steppe, rainfed crops are harvested or senesce by July; irrigated summer crops stay green.)
- **Kakhovka canal network:** OSM canals that intersect a 2 km buffer of the pre-breach reservoir (4.2) or of the Dnipro within 5 km downstream of the dam, plus every canal connected to them (segments within 50 m of each other, iterated to convergence).
- **Kakhovka zone (K):** cropland within 5 km of that network (outside Crimea).
- **Outside zone (O):** cropland > 30 km from the reservoir and > 5 km from the Kakhovka network.

### 4.4 Placebo units
- **Placebo floodplains (H1):** floodplain pixels within 3 km of permanent river water along the Southern Buh (upstream of Mykolaiv), the lower Dniester, and the Dnipro upstream of the Kakhovka reservoir, cut into 10 km river segments. Each segment is treated as if flooded and analysed with exactly the H1 pipeline (controls 2–15 km away on the same side).
- **Placebo zones (H2):** the irrigated–rainfed contrast in each oblast of zone O, treated in turn as if it were zone K.

## 5. Outcomes and periods

- **Primary outcome:** July–October mean NDVI per pixel and year, from composites with pixel reliability 0 (good) or 1 (marginal) whose composite day-of-year falls in July–October; missing if fewer than 5 of the 8 composites are valid. The July–October window keeps 2023 entirely after the breach.
- **Secondary outcomes:** July–August mean NDVI; April–October mean NDVI (2023 excluded); July–October mean EVI; for cropland, a *cropped* indicator (April–October 90th-percentile NDVI ≥ 0.5).
- **Years:** 2016–2021 pre-war (reference); 2022 war, pre-breach; 2023 and 2024 post-breach.
- **Fixed panel:** a pixel enters an analysis only if its outcome is non-missing in at least 7 of the 9 years, so every comparison is between the same pixels over time.

## 6. Estimation

**H1 (matched flood design):**

Y_iy = α_i + λ_(y,s) + β·F_i·Post_y + δ·F_i·War_y + γ′W_iy + ε_iy

with pixel fixed effects α_i, year × stratum (bank × dominant class) effects λ, Post = 2023–2024, War = 2022, and W the July–October ERA5-Land precipitation and mean temperature of the pixel's 0.1° cell. Matched controls are weighted by their matching frequency. **β is the primary estimand.** The event-study version replaces F·Post and F·War with F × year dummies (reference 2021).

**H2 (triple difference):**

Y_iy = α_i + λ_(y,oblast) + μ_(y,irrigated) + κ_(y,zone) + β·Irr_i·K_i·Post_y + δ·Irr_i·K_i·War_y + γ′W_iy + ε_iy

**β is the primary estimand.** Event-study version as for H1.

**Inference:** standard errors clustered on 10 km × 10 km blocks; wild cluster bootstrap p-values (Rademacher weights, 9,999 draws) for β; Conley spatial HAC standard errors (25 km cutoff) as a robustness check. **Randomization inference:** β compared with the distribution of the same estimate for all placebo units (4.4); p = share of placebo estimates at least as negative. **Multiplicity:** Holm correction across H1 and H2 at α = 0.05.

**Pre-trends:** joint test that the 2016–2020 event-study coefficients are zero. Whatever its result, post-breach effects are also reported with sensitivity bounds that allow post-period violations of parallel trends up to M̄ = 0.5, 1 and 2 times the largest pre-period violation (relative-magnitudes approach; Rambachan & Roth, 2023).

## 7. Decision rules for reporting

A primary hypothesis is reported as **supported** if β < 0 with Holm-adjusted wild-bootstrap p < 0.05, randomization p < 0.10, and the M̄ = 1 bound excludes zero; **suggestive** if β < 0 with unadjusted p < 0.05 but one of the other conditions fails; **not supported** otherwise. The same wording will be used in the abstract.

## 8. Pre-specified robustness checks

1. No matching (all candidate controls, 2–15 km).
2. Control band 5–25 km.
3. Without weather covariates.
4. Flood threshold 25% and 75% instead of 50%.
5. Irrigation thresholds 0.40/0.30 and 0.50/0.40 instead of 0.45/0.35.
6. EVI instead of NDVI.
7. Left and right bank separately (H1); Kherson and Zaporizhzhia parts of zone K separately (H2).
8. Effects by dominant land-cover class (cropland, grassland, wetland, trees).
9. Excluding pixels within 3 km of built-up land.

## 9. Decomposition (H4)

The 2021→2024 change in Kherson Oblast mean July–October NDVI is split into area-weighted contributions of F, former reservoir bed, K-irrigated cropland, K-rainfed cropland and all other land, each measured relative to the same-class change in zone O.

## 10. Relation to Study 1

Study 1 is kept unchanged as the administrative-unit analysis that motivates Study 2. The paper will present both, with Study 2 as the main result.

## 11. Deviations

Any departure from this plan (for example, a data product that is unavailable or a rule that cannot be implemented as written) will be logged in `v2/DEVIATIONS.md` with date, reason and the effect on results, before the affected result is interpreted.

## References

Rambachan, A., & Roth, J. (2023). A more credible approach to parallel trends. *The Review of Economic Studies*, 90(5), 2555–2591. https://doi.org/10.1093/restud/rdad018
