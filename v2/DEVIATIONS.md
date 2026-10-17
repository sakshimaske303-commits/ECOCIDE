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
| Decision rule, "unadjusted p" (§7) | The plan does not say which unadjusted p-value to use for the *suggestive* branch. `a7_summary.py` and `r1_summary.py` use the cluster-robust p-value (`p_cluster`); the *supported* branch uses the Holm-adjusted wild-bootstrap p-value. For both H1 and H2 the verdict is the same with either choice. |
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

## 4. Registered Revision 1 (ANALYSIS_PLAN_v2_ADDENDUM_1.md, commit 30e3840, 24 Sept 2026 22:53 IST)

Committed after the pre-registered results were known and before the MODIS 2010–2015, Impact Observatory and VIINA data were downloaded (first 2010 MODIS file written 23:27 IST). Implementation notes:

| Item | Implementation |
|---|---|
| R4 conflict events | VIINA `event_info` + `event_labels` 2022–2024, events located at settlement or street level (GEO_PRECISION ADM3 or STREET) and classified as war-related (t_mil ≥ 0.5): 105,838 / 48,086 / 42,444 events in 2022 / 2023 / 2024. The t_mil filter is an implementation choice (the addendum says "events"). |
| R4 occupation | VIINA `control_latest` status on 1 August of each year for the nearest settlement (`gn_UA_tess.geojson` points) within 10 km; RU = occupied, UA and CONTESTED = not occupied; 7,194 universe pixels have no settlement within 10 km and are coded unoccupied. |
| R4 download | The VIINA repository stores data with Git LFS; files were fetched from media.githubusercontent.com (script `v2/08_conflict_fixed.py`). |
| R5 annual water | Impact Observatory `io-lulc-annual-v02` maps for 2017–2023 (the first download mistakenly took the previous year's map because each item spans 1 Jan–1 Jan; fixed in `v2/07_io_lulc_fixed.py` and re-downloaded before any revised analysis). No 2024 map is published; 2024 uses 2023. The 2023 annual map still shows 68 % water on the reservoir because it covers the months before the breach. |
| R5 consequence for H4 | Every reservoir-bed pixel changes water share by more than 10 points, so the rule removes the reservoir bed from the revised H4 by construction. |
| H1 placebo (revision) | Distance-to-channel bands for each placebo use the distance to that placebo river's traced line; annual water is only available in the lower-Dnipro window, so the water rule does not apply to placebo rivers outside it. |
| H2 placebo raions | 15 districts qualified (≥ 300 irrigated and ≥ 300 rainfed pixels under R1). |
| Classification finding | In the restricted zone O the R1 rule still labels 490,950 pixels irrigated and 23,594 rainfed: in the steppe, too, the NDVI rule separates summer from winter cropping rather than irrigated from rainfed land. Reported as a limitation; the rule was not changed. |

## 5. Exploratory checks after an external review (16 Oct 2026; not registered)

Written after all pre-registered and registered-revision results were known. They change no registered estimate or verdict; they change how H2 and H4 are interpreted in the paper.

| Item | Implementation / finding |
|---|---|
| Script | `v2/analysis/x1_review_diagnostics.py` → `outputs/v2/x1_review_diagnostics.json`. The first version of the JSON was generated from an independent reconstruction of `layers.npz` and `r1_layers.npz`; on 17 Oct 2026 it was regenerated from the pipeline's own layers. Every reported value is unchanged except Chaplynskyi's share of cropland in zone K (86 % → 87 %). |
| Weather (D1, D2) | Pixel-mean July–October ERA5-Land rainfall in zone K (same nearest-cell rule as `v2lib.weather`): 2016–2024 = 131, 115, 129, 141, 131, 161, 118, 67, 94 mm. The H2 reference year 2021 is the wettest and coolest; 2023 the driest; 2024 the hottest. The 2016–2021 H2 event-study coefficients correlate with this rainfall at r = −0.94 (plan) and −0.97 (revision). The plan's models include weather only additively (§6), so they cannot absorb a weather-dependent irrigated–rainfed contrast. |
| Placebo districts (D3) | The four most negative revision placebo districts (Chaplynskyi, Novotroitskyi, Ivanivskyi, Nyzhnosirohozkyi) adjoin the Kakhovka network: 87 %, 77 %, 48 % and 2 % of their cropland is in zone K. Excluding the five districts with ≥ 1 % of cropland in zone K or a median zone-O distance to the network ≤ 20 km (the four plus Melitopolskyi), the one-sided randomization p is 0.18 (10 placebos) instead of 0.375. |
| Confidence intervals | All reported 95 % CIs are β ± 1.96·SE (normal), while p-values use t(G − 1). For the H1 matched estimate (G = 50) the t interval is −0.015 to 0.026 instead of −0.014 to 0.026. Not changed in the code, so that every registered output stays as produced. |

## 6. Registered Revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md, version 1.0, approved 16 Oct 2026)

Approved by the author on 16 October 2026 and committed to the local repository before any of its data were
downloaded. Not deposited with an independent registry (author's decision); the repository is pushed to GitHub only
when the project is finished, so the git commit is the only record of the date.

Addendum 2 SHA-256 (line endings normalised to LF): `0777f2c1871e2309ec616098e97fd7397ab612f9564e0c93268272d25c23f563`

`v2/analysis/run_revision2.py` and every `r2_*.py` script stop if the file's checksum differs from this value. Any
later change to the addendum must be recorded here as a deviation, with a new checksum, before the analysis is run.

| Item | Implementation |
|---|---|
| Code written before data | `v2/09_download_irrigation_maps.py`, `10_download_dem.py`, `11_download_s2_reservoir.py`, `v2/analysis/r2_*.py`, `run_revision2.py`, `tests/test_r2lib.py`; checked only on a synthetic world with known effects (H2 effect −0.050 recovered as −0.053; flood effect −0.020 recovered as −0.020; placebo-in-time test detects the regression-to-the-mean bias built into that world). |
| Map values (after download, before any analysis) | The 2019–2022 RF v6 files are 32-bit integers with values 0, 1 and −999 and no no-data tag; the 2024–2025 RF v7 files are 16-bit with 0 and 1. As the addendum's definitions say (value 1 = irrigated; no-data cells left out), −999 is read as no-data. Checked on 16 Oct 2026 by decoding sample tiles; no outcome data were looked at. |
| DEM values (after download, before any analysis) | `dem_glo30_mean.nc` reports a minimum of −362 m, which is impossible on land here: pixels beside areas with no DEM tiles (open sea) average in the fill value. `r2_prepare.py` sets elevations below −10 m to no-data and records how many pixels this affects in `r2_meta.json`. |
| First run on real data (16 Oct 2026, ~23:00) | The first full run of `run_revision2.py` used the earlier `r2_prepare.py` without the DEM rule above, because the updated file had not reached the run folder. Its outputs are kept unchanged in `outputs/v2/r2_run1_without_dem_rule/`. The run was then repeated with the registered code, and the repeated run is the one reported. |

## 7. Full re-run on 16 Oct 2026 (reproducibility check)

The derived files of `data/v2/derived/` were no longer on the author's computer, so `run_all.py` and `run_revision.py`
were run again from the downloaded data before Revision 2. Every sample size, matched count and verdict is the same
as in the committed outputs, and H3/H4 are identical. Coefficients differ from the 4th significant digit on (for
example Revision 1 H1 β = 0.05517 → 0.05541; plan H2 β = −0.073942 → −0.073942), and some p-values move (Revision 1
H1 pre-trend p = 0.0002 → 0.0016; plan H1 pre-trend p = 0.72 → 0.74). The likely cause is different library
versions on the two runs. The re-run outputs are the ones kept and reported from now on.

