# Sakshi D. Maske
Independent Geospatial Researcher

## Abstract

International legal bodies are actively considering the recognition of "ecocide" — mass environmental destruction — as a prosecutable international crime, with Vanuatu, Fiji, and Samoa formally submitting a Rome Statute amendment to this effect in September 2024. Yet no standardized, statistically rigorous methodology exists for evidencing such damage claims: existing satellite-based assessments of environmental war damage rely on qualitative, visual image interpretation and explicitly decline to establish statistical causality, unable to distinguish conflict-caused degradation from pre-existing environmental trends. This study addresses that gap directly, applying a Difference-in-Differences causal-inference framework to the destruction of Ukraine's Kakhovka Dam (6 June 2023). The design compares monthly NDVI in the conflict-affected Kherson Oblast against a four-county Romanian control panel along the Danube/Black Sea corridor — Tulcea, Galați, Brăila, and Constanța — chosen for comparable pre-conflict river-delta, steppe, and coastal ecology while being genuinely non-combatant. The primary specification, Kherson against Tulcea, identifies a statistically significant vegetation decline attributable to the event (coefficient = −0.0703, 95% CI [−0.130, −0.010], HAC-robust p = 0.022), validated through a clean placebo test using a counterfactual pre-event date. Pooling across the full four-county panel as a robustness check, the effect holds at a similar magnitude (coefficient = −0.0600, HAC p = 0.029), and three of the four controls reproduce it individually, while the fourth (Constanța) does not — reported as an open question rather than resolved away. A quarterly event study further reveals a genuine methodological complication — a significant effect in a pre-treatment quarter, traced to Kherson's already-active conflict status before the dam's destruction — which is reported transparently as a disclosed limitation rather than concealed, and the same complication resurfaces in a different form once the event study is run on the four-county panel, where cluster-robust inference becomes numerically unreliable at only five clusters. Verified multi-sensor flood-extent data (UNOSAT) independently confirms a complete flood rise-peak-recession cycle. This study demonstrates that causal-inference methods, not previously applied to satellite-based environmental war-damage assessment for this event, can quantify conflict-attributable damage with statistical confidence — directly addressing a gap the existing literature itself identifies as a priority for future research.

**Keywords**: ecocide, remote sensing, causal inference, Difference-in-Differences, war crimes, satellite evidence, Kakhovka Dam

---

## 1. Introduction

On 6 June 2023, the Kakhovka Dam on Ukraine's Dnipro River was destroyed, draining an 18.2 km³ reservoir and flooding hundreds of square kilometers of downstream floodplain — one of the most significant environmental consequences of the ongoing war in Ukraine. As international momentum builds toward formal legal recognition of ecocide, the evidentiary methods available to quantify such damage remain comparatively undeveloped relative to the legal frameworks now being proposed to prosecute it.

This study asks whether a causal-inference framework — already established practice in policy evaluation but not previously applied to satellite-based conflict-damage assessment for this event — can isolate the Kakhovka Dam destruction's specific environmental effect from the broader, already-elevated baseline of an active conflict zone, with quantified statistical confidence.

## 2. Literature Review

### 2.1 The Emerging Legal Recognition of Ecocide

The push to recognize ecocide as a prosecutable international crime has accelerated markedly in recent years. In September 2024, Vanuatu, Fiji, and Samoa formally submitted a proposed amendment to the Rome Statute of the International Criminal Court to add ecocide as a fifth international crime alongside genocide, crimes against humanity, war crimes, and aggression, building on a 2021 definition developed by an independent expert panel convened by the Stop Ecocide Foundation. Momentum has extended to domestic legislation as well, with Belgium becoming the first European country to recognize ecocide at both national and international levels, and further legislative proposals advancing in Mexico, Italy, the Netherlands, Brazil, and the United Kingdom. This rapidly evolving legal landscape underscores the need for evidentiary methodologies capable of supporting such prosecutions — a need this study directly addresses.

### 2.2 Satellite Imagery in International Legal Proceedings — Persistent Methodological Gaps

Despite growing legal interest, the literature on satellite imagery as courtroom evidence consistently identifies a specific, unresolved gap: the absence of accepted forensic standards and methodologies. Satellite imagery has been admitted at the International Criminal Court to corroborate witness testimony, but has not yet been admitted as dispositive evidence of mass atrocities in its own right, a limitation attributed in part to the field's continued reliance on largely qualitative, expert-interpretive analysis rather than standardized statistical methods. Analysis identifying the criteria necessary for satellite evidence to be legally useful — operational feasibility, data reliability, and legal admissibility — highlights data reliability as a persistent weak point, precisely the gap a causal-inference design is structured to close by explicitly separating a genuine treatment effect from background noise and pre-existing trends.

### 2.3 Existing Geospatial Assessment of the Kakhovka Event

The most directly relevant prior work is a recently published geospatial assessment of Ukraine's war-related environmental destruction, which examined the Kakhovka Dam event among several case-study locations using multi-temporal satellite imagery. That assessment relied on visual interpretation and comparative review of before-after imagery, explicitly and deliberately declining to establish direct causality between observed environmental changes and military activity, and instead calling for future research to develop standardized, quantitative indicators. This study is designed specifically to answer that call for this event, applying a Difference-in-Differences framework — with matched control-zone comparison, placebo validation, and event-study robustness testing — that had not previously been applied to this specific case.

## 3. Data and Methodology

<p align="center">
  <img src="outputs/plots/study_area_overview.png" width="700">
</p>

**Figure 1.** Study area showing the treatment zone (Kherson Oblast, Ukraine) and the four-county control panel used in this study — Tulcea, Galați, Brăila, and Constanța, Romania. Administrative boundaries were obtained from GADM v4.1. The control counties were selected to represent comparable river-delta, steppe, and coastal ecosystems along the Danube/Black Sea corridor while remaining unaffected by the Kakhovka Dam destruction, enabling causal estimation through matched treatment–control comparison.

### 3.1 Study Design

A Difference-in-Differences design was used, comparing the treatment zone (Kherson Oblast, Ukraine, containing the dam and downstream floodplain) against a four-county control panel in Romania along the Danube/Black Sea corridor — Tulcea, Galați, Brăila, and Constanța — selected for comparable pre-conflict river-delta, steppe, and coastal ecology while being genuinely non-combatant. Tulcea, the Danube Delta county directly across the border, serves as the primary control for the headline specification (Section 4.2); the full four-county panel is used for the pooled and per-zone robustness checks reported in Section 4.5.

### 3.2 Data Sources

| Variable | Source |
|---|---|
| NDVI (monthly) | Sentinel-2, Sentinel Hub Statistical API |
| Verified flood extent | UNOSAT (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS) |
| True-color imagery | Sentinel-2 L2A, Sentinel Hub Process API |
| Boundaries | GADM v4.1 |

### 3.3 Causal Model

A Difference-in-Differences regression was estimated with month fixed effects to control for seasonal vegetation cycles, comparing NDVI before and after 6 June 2023 between treatment and control zones. Validation included a placebo test (a counterfactual treatment date, June 2022) and a quarterly-binned event study testing whether the effect was genuinely concentrated around the true event date.

The primary specification compares only two geographic units (Kherson and Tulcea) observed over time, so cluster-robust standard errors — the standard correction in panel designs with many independent units — are not meaningful there; with only two clusters, cluster-robust inference is degenerate. Inference for the primary specification therefore uses Newey–West heteroskedasticity- and autocorrelation-consistent (HAC) standard errors (Newey & West, 1987), the standard remedy for serial correlation within a small number of long time series. All reported p-values and confidence intervals are HAC-corrected unless otherwise noted; the corresponding classical OLS statistics are reported alongside them in Section 4.4 for comparison. Section 4.5 reports the same design's pooled and per-zone estimates run against the full four-county panel, where cluster-robust standard errors become mathematically defined — though only barely, at 5 clusters — and are reported alongside HAC there for comparison.

### 3.4 Pre-Treatment Covariate Balance

A credible Difference-in-Differences design requires the treatment and control zones to be comparable before treatment, not merely afterward. This was tested directly rather than assumed. Over the pre-period (January 2022 – May 2023), mean NDVI was 0.222 in Kherson (n=17 months, SD=0.074) against 0.203 in Tulcea (n=17 months, SD=0.110) — a raw difference not statistically distinguishable from zero (two-sample t-test, p=0.553). Formally, the DiD regression's own `treatment` main-effect term (the estimated baseline level gap between zones, holding month fixed effects constant) is 0.019 NDVI, 95% CI [−0.021, 0.059], HAC p=0.347 — again not significant. Pre-period variability differs somewhat between zones (Tulcea's seasonal amplitude, 0.351, exceeds Kherson's, 0.274), which is disclosed here rather than smoothed over; this asymmetry is consistent with Tulcea's wetland hydrology and does not, on its own, indicate a violation of parallel pre-trends, which is tested directly via the event study in Section 4.3.

## 4. Results

### 4.1 Flood Extent

Verified UNOSAT data revealed a complete flood hydrograph: 122.50 km² (6 June), expanding to a peak of 464.18 km² (9 June), before receding to 21.17 km² by 21 June — a full rise-peak-recession cycle within approximately two weeks. At its peak, the flood covered approximately 4.3% of the roughly 10,800 km² downstream analysis corridor (dam to river mouth) — a scale indicator alongside the statistical vegetation result, not a substitute for it.

<p align="center">
  <img src="outputs/maps/before_may2023_final.png" width="700">
</p>

<p align="center">
  <img src="outputs/maps/after_july_2023_final.png" width="700">
</p>

**Figure 2.** Sentinel-2 true-colour imagery of the Kakhovka reservoir immediately before (May 2023) and after (July 2023) the destruction of the Kakhovka Dam. The post-event image reveals the near-complete drainage of the reservoir and extensive exposure of the former lakebed. This pair is presented to illustrate the spatial scale of the event and to motivate the statistical analysis that follows; it is not, on its own, evidence of a causal effect — that evidence is established separately in Sections 4.2–4.4, precisely to avoid the reliance on visual interpretation this study critiques in the existing literature (Section 2.3).

<p align="center">
  <img src="outputs/plots/flood_extent_map.png" width="700">
</p>

**Figure 3.** Verified multi-sensor UNOSAT flood-extent polygons over the Kherson Oblast flood corridor, at three dates spanning the event (6, 9, and 21 June 2023), showing the spatial footprint of the flood's rise, peak, and recession.

<p align="center">
  <img src="outputs/plots/flood_hydrograph.png" width="700">
</p>

**Figure 4.** Verified flood hydrograph derived from UNOSAT observations showing the temporal evolution of downstream flooding following the Kakhovka Dam destruction. Flood extent increased rapidly from 122.50 km² on 6 June 2023 to a peak of 464.18 km² on 9 June before progressively receding to 21.17 km² by 21 June, confirming the complete rise–peak–recession cycle independently of the statistical vegetation analysis.

### 4.2 Vegetation Impact

<p align="center">
  <img src="outputs/plots/ndvi_comparison.png" width="700">
</p>

**Figure 5.** Monthly mean NDVI trends for the treatment region (Kherson Oblast, Ukraine) and the primary control region (Tulcea County, Romania) from January 2022 to December 2024. Following the June 2023 Kakhovka Dam destruction, the treatment region exhibits a clear and statistically consistent decline in vegetation greenness relative to the control region, providing preliminary evidence of an environmental impact prior to formal Difference-in-Differences estimation.

The Difference-in-Differences model found a statistically significant NDVI decline in Kherson relative to Tulcea (coefficient = −0.0703, 95% CI [−0.130, −0.010], R² = 0.747). Under HAC-robust standard errors the effect remains statistically significant (p = 0.022), a modest attenuation from the classical OLS estimate (p = 0.007) consistent with positive serial correlation in monthly NDVI. A placebo test using a fake June 2022 treatment date produced a near-zero, non-significant coefficient (0.0148, 95% CI [−0.043, 0.072], HAC p = 0.612), providing clean validation that the real effect is event-specific rather than an artifact of the estimation procedure.

In practical terms, a coefficient of −0.0703 represents a decline of approximately 32% relative to Kherson's own pre-period mean NDVI (0.222; Section 3.4) — a substantial relative reduction in vegetation greenness, not merely a statistically detectable one. This framing is offered as a scale reference; NDVI is a spectral index, not a direct physical measurement of biomass or land area lost, and this study does not attempt to convert it into hectares or tonnes of vegetation without field-validated calibration, which was outside its scope.

### 4.3 Event Study and a Disclosed Limitation

A quarterly event study found significant negative effects in the treatment quarter (HAC p = 0.005), the following quarter (HAC p = 0.023 — not significant under classical standard errors, p = 0.075, but significant under HAC), and one year later (HAC p < 0.0001), but also a significant effect in a pre-treatment quarter (summer 2022, HAC p < 0.001) — traced to Kherson already being an active conflict zone (including a major liberation operation) before the dam's destruction, meaning the original baseline period was not a genuinely quiet pre-conflict period. A sensitivity analysis narrowing the baseline to immediately pre-event months produced a larger effect (−0.1384, 95% CI [−0.209, −0.068], HAC p = 0.0001), but its own placebo test — non-significant under classical standard errors (p = 0.169) — becomes statistically significant under the methodologically correct HAC correction (p = 0.001), a consequence of serial correlation in the very short, ten-observation narrowed window. This is reported as a decisive validation failure for the narrowed-baseline specification, not merely an ambiguous one: the window is too short and too serially correlated to support an independent causal estimate. Both results are reported, with the broader-baseline estimate — whose own placebo test remains clean under HAC — treated as the sole primary, validated finding, and the narrowed-baseline estimate retained only as an illustration of the pre-treatment-quarter problem rather than as independent evidence.

<p align="center">
  <img src="outputs/plots/event_study.png" width="700">
</p>

**Figure 6.** Quarterly event-study estimates (Newey-West HAC standard errors) showing treatment effects relative to the pre-event baseline. Significant negative effects emerge during the treatment quarter, the following quarter, and one year later, while a statistically significant pre-treatment coefficient highlights the influence of earlier conflict-related vegetation changes in Kherson. This pre-treatment signal motivated the sensitivity analysis and is reported transparently as a methodological limitation rather than being excluded.

### 4.4 Robustness Checks

Every regression in this study was re-estimated with Newey–West HAC standard errors alongside the classical OLS estimates that most statistical software reports by default, to test sensitivity to the standard-error specification.

| Model | Coefficient | 95% CI (HAC) | Classical p | HAC p |
|---|---|---|---|---|
| Main DiD | −0.0703 | [−0.130, −0.010] | 0.007 | 0.022 |
| Narrowed-baseline DiD | −0.1384 | [−0.209, −0.068] | 0.002 | 0.0001 |
| Placebo (broad baseline) | 0.0148 | [−0.043, 0.072] | 0.741 | 0.612 |
| Placebo (narrowed baseline) | −0.1382 | [−0.221, −0.055] | 0.169 | 0.001 |

<p align="center">
  <img src="outputs/plots/robustness_check.png" width="700">
</p>

**Figure 7.** Point estimates and 95% confidence intervals for all four causal-inference models under classical OLS versus Newey-West HAC standard errors. The main and narrowed-baseline DiD estimates hold, and remain clearly bounded away from zero, under both specifications. The broad-baseline placebo interval straddles zero under both specifications (clean validation). The narrowed-baseline placebo interval straddles zero classically but excludes zero under HAC — the visual signature of the validation failure discussed above.

The main finding and the narrowed-baseline point estimate both survive HAC correction — the narrowed-baseline estimate in fact becomes more significant, not less. The one qualitative reversal is the narrowed-baseline placebo test, which fails under HAC. This reinforces, rather than undermines, the paper's decision to treat the broader-baseline specification as its sole primary result.

### 4.5 Multi-Control Robustness Check — A Four-County Panel

The primary specification (Section 4.2) rests on a single control zone, Tulcea. As a further robustness check on that choice, the identical causal design was run against the full four-county control panel introduced in Section 3.1 — Tulcea, Galați, Brăila, and Constanța — all pulled over the identical January 2022–December 2024 window with the identical acquisition method (`download_ndvi_control_zones.py`, mirroring `download_ndvi.py` exactly) and chosen for the same reasons: non-combatant status and comparable deltaic or coastal land cover along the Danube/Black Sea corridor.

Pooling Kherson against all four controls, the effect holds: did_term = −0.0600 (HAC 95% CI [−0.114, −0.006], p = 0.029; cluster-robust by zone, 95% CI [−0.097, −0.023], p = 0.002) — a similar direction and only a modestly smaller magnitude than the primary specification's estimate (−0.0703), not a reversal or a collapse toward zero. A placebo test on the same four-control panel, using the same fake June 2022 treatment date as the primary placebo test, comes back clean (coefficient +0.0222, cluster-robust p = 0.216, wrong sign relative to the real effect) — the panel-based design does not spuriously detect a treatment effect at a date nothing happened.

<p align="center">
  <img src="outputs/plots/control_panel_comparison.png" width="700">
</p>

**Figure 8.** Kherson's NDVI decline tested against each of the four control counties individually, plus the pooled four-control estimate. Three of four controls (Tulcea, Galați, Brăila) individually reproduce a statistically significant negative effect in a similar range; Constanța alone does not.

The individual, one-control-at-a-time breakdown behind that pooled figure is itself the more informative result, and is reported in full rather than only as a pooled summary: Tulcea (−0.0703, p = 0.022), Galați (−0.0695, p = 0.026), and Brăila (−0.0937, p < 0.001) each independently reproduce a significant negative effect close in magnitude to the primary finding, while Constanța (−0.0064, p = 0.808) shows essentially nothing. This is reported as a genuine, unresolved finding rather than smoothed into the pooled number: Constanța is the most purely coastal, most urbanized of the four counties, sitting further from the Danube's floodplain and deltaic wetland character that Tulcea, Galați, and Brăila all share more directly, which is a plausible ecological reason a Kherson comparison would behave differently there — but this study has no land-cover classification or vegetation-type breakdown to confirm that explanation rather than assert it, so it is left as an open question rather than a settled one.

Two honest caveats belong alongside this result rather than after it. First, five clusters (one treatment, four control) is the minimum at which cluster-robust inference is even mathematically defined, not a number large enough for the asymptotic theory behind it to be fully trustworthy — standard guidance wants 30-40+ clusters, and few-cluster settings are a documented source of understated standard errors, so the cluster-robust p-values here are reported as a useful cross-check, not a substitute for a properly powered multi-unit panel. Second, running the same four-county panel through a quarterly event study (`event_study_multi_control.py`) pushes this limitation past the point of being usable at all: with roughly 24 parameters (twelve month dummies, treatment, and around eleven quarterly event terms) estimated from only 5 clusters, the cluster-robust covariance matrix comes out severely rank-deficient (rank 4, not 24), and several individual quarter coefficients return numerically degenerate standard errors on the order of 1e-16 — not real precision, an artifact of too few clusters for too many parameters. The HAC specification of the same panel-based event study is reported instead, and shows a genuinely different temporal signature than the primary specification's two-zone event study: the treatment-quarter effect itself is no longer significant when pooled across four ecologically heterogeneous controls (p = 0.972, versus p = 0.005 in the primary two-zone design), while the quarter-and-a-year-later effect remains significant (p = 0.011). This is disclosed as a real complication rather than reconciled away — the pooled, non-quarterly DiD result in this section is robust to the choice of control panel; the finer-grained quarterly timing story is not, at least not yet, at this cluster count.

## 5. Discussion

This study's central methodological contribution is not merely applying satellite data to a conflict-damage question, but subjecting that application to the same falsification discipline standard in causal-inference research generally — a discipline the existing literature on satellite evidence in legal contexts identifies as precisely what is missing. The pre-treatment-quarter anomaly, rather than being suppressed, itself illustrates why naive before-after comparisons of conflict zones are methodologically fragile: an active war zone rarely has a genuinely undisturbed "before" period, and treating one as such risks conflating cumulative war effects with the effect of a specific, dateable event.

### 5.1 Legal Relevance and Its Limits

Article 8(2)(b)(iv) of the Rome Statute — the existing war-crime provision most directly concerned with environmental harm, distinct from the separately proposed standalone crime of ecocide discussed in Section 2.1 — prohibits attacks known to cause "widespread, long-term and severe damage to the natural environment which would be clearly excessive in relation to the concrete and direct overall military advantage anticipated." This study's findings speak to only one element of that conjunctive, multi-part test. The magnitude and statistical confidence of the vegetation decline (Section 4.2) and the spatial scale of the verified flood extent (Section 4.1) provide quantified evidence relevant to the "severe" and "widespread" elements specifically. They do not, on their own, establish the "long-term" element — this study's NDVI series runs only through November 2024, some 18 months post-event, which is suggestive but not conclusive of a durable, non-recovering change — and they say nothing about the "clearly excessive... military advantage" element, which is a legal and factual judgment outside this study's data and scope entirely. This study is offered as a contribution to the evidentiary basis such a legal determination would require, not as a substitute for one.

## 6. Limitations and Threats to Validity

The narrowed-baseline sensitivity analysis fails its own placebo test once HAC-robust standard errors are applied (Section 4.4) and is therefore not treated as independent validating evidence; it is retained in this paper only to illustrate the pre-treatment-quarter problem that motivated it. The primary specification rests on a single treatment-control comparison (Kherson vs. Tulcea); Section 4.5 reports the same design run against the full four-county panel as a robustness check, where the pooled effect holds (did_term = −0.0600, HAC p = 0.029) and three of the four individual controls reproduce it independently. That check is a genuine strengthening of confidence in the result, not a complete resolution of every open question: five clusters is the minimum at which cluster-robust inference is even defined, not a number large enough for the underlying asymptotic theory to be fully trustworthy, and the same panel's quarterly event study is not usable under cluster-robust standard errors at all (Section 4.5) — HAC remains the load-bearing specification throughout this paper for exactly that reason. Reservoir water-loss could not be tested causally, since no comparable control-zone equivalent exists for a large upstream reservoir collapse, and is reported descriptively rather than as an independently causally-tested finding.

The following threats to validity were considered specifically, beyond the headline limitations above:

- **Selection bias in the control zone.** Tulcea County was chosen for ecological comparability and genuinely non-combatant status (Section 3.1), and pre-treatment covariate balance was tested directly rather than assumed (Section 3.4). This is tested directly in Section 4.5's four-county panel check rather than left as an unaddressed concern; it remains four human-selected controls rather than an algorithmically weighted synthetic counterfactual, as a Synthetic Control Method design would provide (Section 7). One of the four (Constanța) does not reproduce the effect, which is reported as an open, unexplained question rather than a settled one (Section 4.5).
- **Spatial spillover.** The Difference-in-Differences design assumes the control zone is unaffected by the treatment. Tulcea, Galați, Brăila, and Constanța, all roughly 250-400 km from Kherson across an international border, are reasonable candidates for this assumption, but no formal spillover test (e.g., a spatial-lag diagnostic) was conducted for any of them.
- **Data attrition from cloud contamination.** As documented in ECO_Development_Log.md, optical Sentinel-2 composites are affected by cloud cover, which can bias which pixels contribute to a given month's statistic. This motivated the switch to UNOSAT's multi-sensor (including radar) flood product for the flood-extent analysis specifically; the NDVI series itself remains optical and inherits this general limitation, partially mitigated by monthly (rather than higher-frequency) aggregation.
- **Serial correlation.** Addressed directly via Newey-West HAC standard errors throughout (Section 3.3, 4.4, 4.5) rather than left uncorrected.
- **Few-cluster inference.** Cluster-robust standard errors, available once the panel comprises more than two units (Section 4.5), come from only 5 clusters — thinner than the 30-40+ standard guidance wants, and the quarterly event study at that cluster count produces numerically degenerate cluster-robust coefficients, addressed by reporting HAC instead for that specific model.
- **Single-index measurement.** NDVI captures vegetation greenness specifically; it does not directly measure soil salinization, water contamination, or other dimensions of environmental harm potentially relevant to a fuller damage assessment (Section 7).

## 7. Future Work

Several extensions were identified as valuable but out of scope for this study's timeline and data budget, and are recorded here rather than silently omitted:

- **Synthetic Control Method (SCM).** This study's four-county panel (Section 4.5) uses hand-selected controls; a full SCM design would go further, constructing an algorithmically weighted synthetic counterfactual from those same candidate regions (and potentially more) rather than treating all four equally or individually, and would directly speak to why Constanța behaves differently from the other three.
- **A land-cover explanation for the Constanța result.** Section 4.5 leaves Constanța's null result as an open question. A land-cover classification comparison across the four control counties (proportion cropland vs. urban vs. wetland) would test the working hypothesis that Constanța's more purely coastal, more urbanized character — rather than anything about the causal design itself — explains why it alone does not reproduce the effect.
- **A genuinely large-N control panel.** Even with the four-county panel (Section 4.5), this design has 5 clusters against the 30-40+ that cluster-robust asymptotics assume. Reaching that scale would mean moving beyond adjacent Romanian counties to a wider, non-combatant Black Sea/Danube basin sample (e.g., Bulgarian and Moldovan counterparts), a considerably larger acquisition and boundary-matching effort than the current panel.
- **Additional vegetation and moisture indices.** Re-running the causal model on EVI (Enhanced Vegetation Index, less sensitive to soil background) and NDMI (Normalized Difference Moisture Index) would test whether the NDVI-based finding is an artifact of index choice or a robust cross-index signal.
- **Meteorological and soil covariates.** Incorporating ERA5-Land reanalysis temperature and precipitation as regression covariates would help isolate the conflict-attributable signal from ordinary climate variability beyond what month fixed effects capture.
- **SAR-based soil moisture and salinization analysis.** Sentinel-1 C-band SAR (VV/VH ratio) time series could speak to soil salinization and moisture-regime change in the drained reservoir bed and downstream floodplain — a dimension of damage NDVI alone cannot capture.
- **Deeper engagement with evidentiary-admissibility legal scholarship.** Beyond Section 5.1's treatment of Article 8(2)(b)(iv), a fuller discussion of scientific-evidence admissibility standards (e.g., the *Daubert* framework and its international-tribunal analogues) would strengthen the paper's positioning at the law–statistics interface.

## 8. Conclusion

Applying a causal-inference framework — previously undemonstrated for this event — to satellite-derived vegetation data, this study identifies a statistically significant, placebo-validated environmental effect attributable specifically to the Kakhovka Dam's destruction, while transparently disclosing a genuine methodological complication arising from the region's pre-existing conflict status. A four-county control-panel robustness check (Section 4.5) tests the design's reliance on a single comparison zone directly rather than leaving it as an abstract caveat: the pooled effect holds, three of four individual controls reproduce it, and one open, honestly unresolved question remains — why Constanța alone does not. This directly addresses a gap the existing literature on both satellite-based conflict-damage assessment and legal evidentiary standards for environmental crimes explicitly identifies: the absence of standardized, statistically rigorous methods capable of distinguishing conflict-attributable damage from background environmental trends.

## References

Atılgan Pazvantoğlu, C. (2025). Ecocide as a separate crime under the Rome Statute: A legal analysis of the discourse. *Environmental Policy and Law*, 55(2–3), 57–67. [https://doi.org/10.1177/18785395251351171](https://doi.org/10.1177/18785395251351171)

Kroker, P. (2015). Satellite imagery as evidence for international crimes. *International Justice Monitor*. [https://www.ijmonitor.org/2015/04/satellite-imagery-as-evidence-for-international-crimes/](https://www.ijmonitor.org/2015/04/satellite-imagery-as-evidence-for-international-crimes/)

Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708. [https://doi.org/10.2307/1913610](https://doi.org/10.2307/1913610)

Rome Statute of the International Criminal Court. (1998, as amended). Article 8(2)(b)(iv). United Nations. [https://legal.un.org/icc/statute/99_corr/cstatute.htm](https://legal.un.org/icc/statute/99_corr/cstatute.htm)

Stop Ecocide International. (2024). Mass destruction of nature reaches International Criminal Court (ICC) as Pacific island states propose recognition of "ecocide" as international crime. [https://www.stopecocide.earth/2024/mass-destruction-of-nature-reaches-international-criminal-court-icc-as-pacific-island-states-propose-recognition-of-ecocide-as-international-crime](https://www.stopecocide.earth/2024/mass-destruction-of-nature-reaches-international-criminal-court-icc-as-pacific-island-states-propose-recognition-of-ecocide-as-international-crime)

Wang, B. Y., Raymond, N., Gould, G., & Baker, I. (2013). Problems from hell, solution in the heavens?: Identifying obstacles and opportunities for employing geospatial technologies to document and mitigate mass atrocities. *Stability: International Journal of Security and Development*, 2(3), Art. 53. [https://doi.org/10.5334/sta.cn](https://doi.org/10.5334/sta.cn)

---

**Full dataset, code, and reproducible pipeline**: github.com/sakshimaske303-commits/ECOCIDE
**Live interactive dashboard**: https://ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app/