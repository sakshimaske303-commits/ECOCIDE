# Deviations from ANALYSIS_PLAN_v2.md

Every change to the pre-registered plan is recorded here with its date, the reason, and what it changes. The paper reports all of them. Results that do not follow the plan are labelled *exploratory*.

## 1. Deviations (a written rule was changed or could not be applied as written)

| Date | Plan section | Change | Reason | Effect on results |
|---|---|---|---|---|
| 2026-09-24 | §6 Conley SE | Bartlett kernel (weight 1 − d/25 km) instead of a flat kernel inside 25 km. Scores are summed within pixel over years and aggregated to 2.3 km cells (H1) or 4.6 km cells (H2) before the spatial sum. | The plan did not name a kernel. The flat kernel gave a near-zero variance (SE 0.0003 vs cluster SE 0.010) in the small H1 matched sample, which is a known failure of that kernel (the variance matrix is not guaranteed positive). Cell aggregation keeps H2 (1.6 million pixels) computable. | H1 Conley SE 0.014, H2 0.013; neither changes any verdict. |
| 2026-09-24 | §6 randomization inference, H2 | Placebo zones: oblasts of zone O with fewer than 500 irrigated or fewer than 500 rainfed pixels are skipped (Cherkasy, Kharkiv, Kiev, Poltava, Vinnytsia). 6 placebo zones remain. | A placebo triple difference needs both groups; those oblasts have 0–207 rainfed pixels. | The smallest attainable randomization p is 1/7 = 0.14, so the plan's "randomization p < 0.10" condition for *supported* could not be met for H2 by construction (even with all 11 oblasts the minimum would be 1/12 = 0.083). This is reported in the paper as a design limitation. |
| 2026-09-24 | §6 randomization inference, H1 | The placebo unit is a 10 km segment × one side of the river (controls must be on the same side, as for the real flood). Segment–sides with < 50 floodplain pixels or < 100 control pixels are not formed; for the matched estimate, units with < 10 matched treated pixels are dropped. | Needed to apply "exactly the H1 pipeline" (same-side controls, matching) to each placebo. | 141 placebo units formed; 50 have ≥ 10 matched treated pixels and enter the matched randomization test; all 141 enter the test for the unmatched (robustness 1) estimate. |

## 2. Implementation choices (the plan was silent or ambiguous; fixed in code before the result was seen unless stated)

| Item | Implementation |
|---|---|
| H1 caliper (§4.1, "0.25 SD of the distance") | 0.25 × the standard deviation of Mahalanobis distances between 20,000 random treated–candidate pairs in the stratum. A flooded pixel is kept if at least one of its 3 nearest controls is inside the caliper; control weight = Σ 1/kᵢ over the flooded pixels it serves. Matching requires all six 2016–2021 outcomes. **Consequence (seen after running):** 148 of 8,446 flooded pixels (1.8 %) are matched, because flooded land (mostly floodplain wetland, pre-war NDVI about 2 SD above its surroundings) has almost no unflooded look-alikes 2–15 km away. The pre-registered robustness check without matching and an exploratory match without caliper are reported next to it. |
| Dnipro main channel and banks (§4.1) | Least-cost path through pre-breach water (UNOSAT 3–5 June 2023 water extent ∪ WorldCover water ≥ 50 %) from below the Kakhovka dam to the estuary mouth and from the Zaporizhzhia dam to the Kakhovka dam; cost 1/(1+distance-to-shore)². Land within 30 km of flooded pixels is split along this path into right and left bank; 106 pixels in small separate pieces go to the nearest bank. |
| Reservoir bed (§4.2) | Largest connected WorldCover-water ≥ 50 % component between the two dams: 1,812 km² on the grid (official reservoir area ≈ 2,155 km²; narrow margins fall below 50 % water at 231 m). |
| Kakhovka canal network (§4.3) | 1,879 of 5,910 OSM canal ways (3,264 km) after the 2 km-buffer seed rule and 50 m connectivity iteration. |
| Irrigated / rainfed (§4.3) | A year counts as "≥ 0.45" / "< 0.35" only if its July–August mean exists (≥ 2 valid observations); missing years count as not meeting the rule. |
| Secondary outcomes (§5) | July–August mean needs ≥ 2 valid observations; April–October mean and its 90th percentile need ≥ 8. |
| Weather covariates (§6) | Each pixel takes the nearest ERA5-Land land cell; July–October precipitation total (per 100 mm) and mean 2 m temperature (°C). |
| Wild cluster bootstrap (§6) | Restricted (WCR), Rademacher, 9,999 draws, computed from cluster-level scores after partialling out all fixed effects and other regressors. Two-sided p is used for the Holm correction. |
| Rambachan–Roth (§6) | Relative-magnitudes restriction with the reference year 2021 normalised to 0, so the violation in year t is bounded by (t − 2021)·M̄·M_pre; target = mean of the 2023 and 2024 event-study effects. The robust interval widens the bound by the 95th percentile of M_pre from 20,000 parametric draws of the event-study coefficients (conservative; not the HonestDiD FLCI). |
| H4 reference for the reservoir bed | No zone-O analogue exists (open water in 2021), so its raw change is used. |

## 3. Data notes

| Date | Item | Note |
|---|---|---|
| 2026-09-24 | MODIS availability | The Planetary Computer catalogue (`modis-13Q1-061`, Terra) returned 204 of the 207 expected 16-day composites for 2016–2024. Not in the catalogue: 2023-02-18, 2024-08-12, 2024-12-18. Only 2024-08-12 falls in the July–October outcome window; the ≥ 5 valid observations rule (plan §5) is applied unchanged. |
| 2026-09-24 | Grid corners | The EPSG:3035 grid is the envelope of the 29.0–36.5 °E × 45.3–49.3 °N box, so its corners reach 50.7 °N, where the MODIS h19v03/h20v03 tiles (not downloaded) would be needed. Analyses use only pixels whose centre lies inside the lon/lat box stated in plan §3. |
| 2026-09-24 | Season assignment (plan §5) | A pixel observation belongs to a season by its own MOD13Q1 composite day-of-year band, not by the composite start date. "Fewer than 5 of the 8 composites" is implemented as "fewer than 5 valid observations whose day-of-year falls in 1 July–31 October". |
| 2026-09-24 | OSM canals | Downloaded 24 Sept 2026 via the Overpass API (fallback server overpass.private.coffee): 5,910 `waterway=canal` ways. OSM reflects current mapping, not a dated pre-war snapshot. |
| 2026-09-24 | ERA5-Land | 120 monthly means (Jan 2015–Dec 2024), 0.1°; `tp` is a daily mean in metres, converted to monthly totals in mm (× days in month × 1000). |
| 2026-09-24 | H2 classification check | In zone O the rule labels 93 % of cropland "irrigated": in the wetter northern oblasts (e.g. Kirovohrad, Cherkasy, Vinnytsia) rainfed summer crops are green in July–August, so the plan's premise ("in this dry steppe, rainfed crops … senesce by July") holds only in the southern oblasts. The rule was not changed; the paper reports this as a limitation of the H2 exposure measure. |
