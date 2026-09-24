# ECOCIDE v2 — Registered Revision 1 (addendum to ANALYSIS_PLAN_v2.md)

Version 1.0 · written 24 September 2026 · Sakshi D. Maske

## Status of this document

`ANALYSIS_PLAN_v2.md` (commit 521672f) was registered before any Study 2 data were downloaded. Its analyses have been run, and their results are reported unchanged as the **pre-registered results**.

Running them exposed five design problems. This addendum specifies how each is addressed. It is written and committed **before**:

- the additional data it needs are downloaded (MODIS 2010–2015, Impact Observatory annual land cover, conflict data), and
- any of the analyses below are run.

Results under this addendum are reported as **registered-revision results**, next to, never instead of, the pre-registered ones. The paper states that the addendum was written after the pre-registered results were known.

The changes below apply to the addendum analyses only. Everything not mentioned stays as in the plan: outcomes, periods, fixed panel, models, inference and robustness checks.

## Problems found in the pre-registered analysis

| # | Problem | Evidence |
|---|---|---|
| P1 | H2 exposure classification uses the outcome's own pre-period. Irrigated/rainfed status comes from July–August NDVI in 2017–2021, which overlap the event-study pre-period. This creates selection on the outcome and mean reversion. | H2 event study: 2016–2020 coefficients +0.05 to +0.07 relative to 2021; joint pre-trend p < 10⁻³⁸. |
| P2 | The H2 irrigation rule fails outside the dry steppe. | 93 % of zone-O cropland classified "irrigated", concentrated in forest-steppe oblasts (Kirovohrad, Cherkasy, Vinnytsia, Poltava, Kharkiv). |
| P3 | H2 randomization inference had a floor of p = 0.14 (six placebo oblasts). | The plan's "randomization p < 0.10" could not be met. |
| P4 | War intensity may confound both hypotheses. | H1: the flood zone is the front line, and controls lie 2–15 km from it. H2: most of zone K was occupied from 2022. The plan had no war-intensity or occupation term. |
| P5 | Water–land mixing after the reservoir drained. The pixel water share is fixed at 2021 (WorldCover), but river and floodplain water levels changed after June 2023. | Affects H1 (floodplain pixels) and H3. |

## R1 — Irrigation status from years outside the outcome panel (P1)

- **Irrigated:** mean July–August NDVI ≥ 0.45 in at least 4 of the 6 years 2010–2015.
- **Rainfed:** mean July–August NDVI < 0.35 in at least 5 of those 6 years.

A year counts only if its July–August mean exists (≥ 2 valid observations). Other cropland is excluded. The thresholds are those of the plan; the year counts keep the plan's proportions (3/5 → 4/6, 4/5 → 5/6). The data are MODIS Terra MOD13Q1 v061 for 2010–2015, processed exactly like 2016–2024 (`v2/01`, `v2/06`).

## R2 — Comparison zone restricted to the steppe oblasts (P2)

Zone O is restricted to cropland in the four southern steppe oblasts: Odesa, Mykolaiv, Kherson and Zaporizhzhia (Crimea stays excluded). All other zone-O rules are unchanged: more than 30 km from the reservoir and more than 5 km from the Kakhovka network.

Sensitivity check: add Dnipropetrovsk oblast.

## R3 — Placebo units for H2 (P3)

Placebo units are the GADM level-2 districts (raions) inside the restricted zone O with at least 300 irrigated and at least 300 rainfed pixels under R1. Each is treated in turn as if it were zone K, against the rest of the restricted zone O. The randomization p is the share of placebo estimates at least as negative as the real one (one-sided), with the real unit included in the denominator.

## R4 — War intensity and occupation (P4)

### Conflict events

Conflict events come from VIINA (Zhukov, 2023), or from UCDP GED if VIINA cannot be downloaded (the source used is reported). For each pixel and year 2022–2024:

- intensity = log(1 + number of geolocated events within 5 km during 1 March–31 October);
- 2016–2021 are set to 0.

### Occupation

Occupation is measured per pixel and year: whether the pixel lies in territory under Russian control on 1 August of that year.

**Primary source:** VIINA territorial-control data, if available. A pixel takes the control status of the nearest settlement within 10 km; otherwise it is coded unoccupied.

**Fallback source** (used only if VIINA control data cannot be obtained):

- **2022:** all of Kherson Oblast, plus Zaporizhzhia Oblast south of 47.45 °N.
- **2023–2024:** the Kherson Oblast left bank (as defined by the Dnipro main channel of plan §4.1, extended across the whole oblast), plus Zaporizhzhia Oblast south of 47.45 °N.

The paper must state that the fallback is a coarse approximation.

### H1 revised model

The H1 model adds:

- year × 2 km band of distance to the Dnipro main channel fixed effects (front-line gradient), and
- the conflict intensity term.

### H2 revised model

The H2 model adds:

- year × irrigated × occupied fixed effects, so that zone K is compared with zone-O cropland of the same occupation status, and
- the conflict intensity term.

## R5 — Annual water share (P5)

The water share of each pixel in each year 2017–2024 comes from the Impact Observatory 10 m annual land-use/land-cover maps (Microsoft Planetary Computer, `io-lulc-annual-v02`). Pixels containing clouds or no data are left out of the denominator. If a year is not published, the nearest earlier published year is used, and this is reported.

- **H1 and H4:** a pixel-year with an annual water share above 10 %, or a change of more than 10 points from its 2021 share, is set to missing. The fixed-panel rule is then re-applied.
- **H3:** reservoir-bed statistics are recomputed on pixel-years with an annual water share below 10 % ("land"), and the land area per year is reported.

## Specification set and reporting

### H1 registered-revision specification

- R4 terms (channel-distance × year fixed effects and conflict intensity)
- R5 water rule
- the plan's matching, controls and inference, unchanged

Also reported: the same specification without matching (plan robustness 1).

### H2 registered-revision specification

- R1 classification
- R2 comparison zone
- R4 terms (irrigated × occupied × year fixed effects and conflict intensity)
- R3 placebo inference
- the plan's wild bootstrap, Conley SEs, event study, pre-trend test and Rambachan–Roth bounds

### Decision rule

The plan's rule (§7) is applied unchanged to the registered-revision specifications. The Holm correction runs over the two revised primary tests.

### Robustness

For each revised specification, the plan's §8 checks that still apply are re-run:

- H1: checks 1–9
- H2: checks 3, 5, 6, 7 and 9, plus the R2 Dnipropetrovsk sensitivity

### Reporting rules

Every result from this addendum is labelled "registered revision". A result that depends on the fallback occupation source is additionally flagged.

## References

Zhukov, Y. M. (2023). Near-real time analysis of war and economic activity during Russia’s invasion of Ukraine. *Journal of Comparative Economics*. VIINA data: https://github.com/zhukovyuri/VIINA
