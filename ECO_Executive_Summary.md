# ECOCIDE — Executive Summary

**Satellite evidence and causal-inference testing of the Kakhovka Dam destruction**

Sakshi D. Maske · Independent Geospatial Researcher · Code and data: github.com/sakshimaske303-commits/ECOCIDE

## Question

The Kakhovka Dam on the Dnipro was destroyed on 6 June 2023, draining a reservoir of about 18.2 km³ and flooding the downstream floodplain. Most satellite assessments of the event describe the change visually. This project asks a narrower, testable question: after June 2023, did vegetation greenness (NDVI) in Kherson Oblast change more than in comparable regions outside the war, by more than those regions vary among themselves?

The difficulty is that Kherson was an active war zone well before the dam failed, so a simple before–after comparison mixes the dam's effect with everything else the war was doing. A Difference-in-Differences design compares Kherson's change with the change in control regions over the same months.

## Data and method

- **NDVI:** monthly Sentinel-2 L2A composites, January 2022 – November 2024, over each zone's GADM polygon on a common ~150–220 m grid, with cloud, cloud shadow, cirrus, snow and water masked and each pixel's median over all clear acquisitions in the month (Sentinel Hub Statistical API).
- **Zones:** Kherson Oblast (treatment); Tulcea County, Romania (primary control); Galați, Brăila and Constanța counties (four-county panel). Controls were chosen by hand for broadly similar delta, steppe and coastal landscapes; no formal matching was done.
- **Estimation:** the monthly Kherson-minus-control NDVI gap before vs after June 2023, Newey-West HAC standard errors (maxlags = 3, t-distribution).
- **Checks:** a model with zone-specific seasonality, placebo dates, a quarterly event study with Bonferroni/Benjamini–Hochberg correction, the four-county panel, placebo in space (randomization inference) and a control-only divergence check.
- **Flood extent:** UNOSAT FL20230606UKR layers, reported descriptively.

## Findings

| Check | Result |
|---|---|
| Primary DiD, Kherson vs Tulcea | −0.108 NDVI, 95% CI [−0.209, −0.007], p = 0.037 |
| With zone-specific seasonality | −0.069, p = 0.005 |
| Placebo, fake date June 2022 | +0.012, p = 0.802 |
| Narrowed baseline (from January 2023) | −0.186, p = 0.001 — but its own placebo is significant (p = 0.004) |
| Kherson vs four-county mean | −0.071, p = 0.022 |
| Per control: Tulcea / Galați / Brăila / Constanța | significant decline against the first three; none against Constanța |
| Placebo in space | Kherson ranks 2nd of 5 (exact p = 0.40); Constanța shifts by as much |
| Event study | 4 of 5 pre-event quarters deviate; the summer–autumn gap deepens in 2024 |
| UNOSAT flood extent, 6–9 June (cumulative) | ≈617 km² |

Kherson's NDVI declined relative to comparable unaffected regions after June 2023. The decline is statistically significant, survives zone-specific seasonality and every specification check, is absent at a placebo date, and is largest in the 2024 growing season. **It cannot, however, be attributed to the dam's destruction with this design:** Constanța shows an equally large shift, pre-event quarters already deviate, and the oblast-wide unit mixes flooding, reservoir drainage and war effects.

## What changed from the first version

The first version (EarthArXiv preprint v1; Zenodo v1.0.0) reported −0.0703, p = 0.022, from bounding-box extraction and stacked-panel standard errors. Correcting the geometry and the standard errors gave −0.075, p = 0.16. Correcting the pixel size, masking water and compositing each month over all clear acquisitions gave the current −0.108, p = 0.037. Each technical change moved the headline across the 5% threshold — the reason every step is documented in `ECO_RESULTS_RECONCILIATION.md`.

## Limitations

- The NDVI unit is the whole oblast (≈25,500 km²); the mapped flood covered only about 2% of it, so an oblast-wide decline points to slower, larger-scale pathways (irrigation loss, war effects on agriculture) that this design cannot separate.
- Five geographic units: randomization inference cannot go below p = 0.20, and the controls were chosen by hand.
- Pre-event quarters deviate from the reference quarter, so parallel trends do not hold cleanly.
- NDVI measures greenness only.

## Relevance

A standalone crime of ecocide has been proposed for the Rome Statute (Vanuatu, Fiji and Samoa, September 2024) but not adopted; Ukraine's Criminal Code already contains an ecocide offence (Article 441). Any claim that satellite data show conflict-attributable environmental damage will face exactly the tests reported here. This case shows the difference between a statistically significant satellite signal and an event-attributable one — a distinction any such evidence should be tested for before it is relied on.
