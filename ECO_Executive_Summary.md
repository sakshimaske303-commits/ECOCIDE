# ECOCIDE — Executive Summary

**What did the destruction of the Kakhovka Dam do to vegetation? Separating flood, reservoir and irrigation effects with satellite data**

Sakshi D. Maske · Independent Geospatial Researcher · Code and data: github.com/sakshimaske303-commits/ECOCIDE · Full paper: `ECO_Research_Paper_v2.md`

## The question

The Kakhovka Dam was destroyed on 6 June 2023. This could have changed vegetation in three ways:

- the flood below the dam;
- the draining of the reservoir;
- the loss of water for the irrigation canals.

All three happened inside an active war zone. **Research question:** which of these pathways left a mark on vegetation that can be told apart from the war itself, when exposed land is compared with similar land in the same war zone?

## Why I needed a second study

My first study (Study 1) compared the average greenness (NDVI) of the whole of Kherson Oblast with four counties in Romania. Kherson became less green after June 2023 (−0.108, p = 0.037). But I could not show that the dam caused this:

- the flood covered only 2% of the oblast;
- the two areas were already moving apart before the event;
- when each area was treated as the "affected" one in turn, Kherson ranked only second of five (p = 0.40).

## What I did in Study 2

- **Data.** I used MODIS NDVI at 250 m for 2016–2024 (2010–2015 for the revision) and looked at each pixel.
- **Exposure groups.** I defined each group by what physically happened to the land: flooded land (UNOSAT maps), the drained reservoir bed, and farmland within 5 km of the reservoir's canals (OpenStreetMap).
- **Comparisons.** I compared each group with similar land in the same war zone:
  - flooded land with matched unflooded land on the same river bank;
  - irrigated with rainfed farmland, inside and outside the canal zone.
- **Plan fixed in advance.** I wrote the full analysis plan, including the words I would use for each result, and made it public on GitHub before downloading any data (commit 521672f).
- **Registered revision.** When the first results showed five problems, I wrote a second plan and made it public before collecting the extra data it needed (commit 30e3840). It added:
  - irrigation status from 2010–2015;
  - a comparison zone limited to the steppe oblasts;
  - district-level placebo tests;
  - occupation and war intensity from VIINA;
  - yearly water masks.
- **Tests.** I used clustered and spatial standard errors, a wild cluster bootstrap, placebo tests, the Holm correction, and Rambachan–Roth sensitivity bounds.
- **Later checks (exploratory).** After all results were known, I checked summer weather in the canal zone and how close the placebo districts lie to the canals.

## What I found

| Pathway | Main plan | Revision | What it means |
|---|---|---|---|
| **Flood**: flooded vs unflooded land | All flooded pixels +0.010 NDVI (95% CI −0.004 to 0.025); matched sample (1.8% of pixels) +0.006 (−0.014 to 0.026); placebo p = 0.63 | Matched +0.055, unmatched +0.012 (n.s.) | No detectable lasting loss of July–October greenness |
| Floodplain wetlands | −0.041 | −0.061 | Wetlands lost greenness (flood or lower river level) |
| **Irrigated farmland**: canal zone vs elsewhere | −0.074, but already falling before the war | −0.053; close to the 2021 level after the breach (−0.006 to −0.014, n.s.); placebo p = 0.38 | Not testable with this design (see below) |
| **Reservoir bed** | Area with NDVI above 0.3: 86–100 km² each year before the breach, 906 km² in 2023, 1,574 km² in 2024 | Same path on land-only pixels | Largest change (description only, no comparison group) |
| **Kherson Oblast, 2021 to 2024** | −0.029 overall; reservoir bed +0.010; irrigated canal zone −0.013; land outside the exposure groups −0.024 | −0.052 (reservoir bed removed by the water rule) | The oblast average mixes changes of opposite sign |

By the naming rule in my plan, the flood result is "not supported" and the irrigation result is "suggestive".

**Why the irrigation result cannot be read as "no effect".** The year-by-year results are compared with 2021, the wettest summer of the record in the canal zone (161 mm of July–October rain, against 67 mm in 2023 and 94 mm in 2024). Before the war the farmland contrast moved closely with summer rain (r = −0.97), but my models do not let weather change that contrast. Also, the placebo districts with the largest declines lie next to the canal network and are partly irrigated by it. So my design neither shows nor rules out an effect of the lost canal water.

## What this means

1. **The reservoir bed changed the most.** About 1,500 km² became green within two seasons. This is a description, not a tested effect, because there is no comparison area. Field studies report the same (Kuzemko et al., 2025).
2. **I found no lasting loss of July–October greenness on flooded land, except in wetlands.** The wetland loss may come from the lower, unregulated river after the dam's loss rather than from the flood itself.
3. **The irrigation pathway was not testable with my design, even though irrigation stopped.** Other work shows that irrigated area fell by about 90% (Baber et al., 2026; NASA Harvest). Testing it needs field-level irrigation maps, comparison land outside the whole irrigation command area, and models in which weather can change the irrigated–rainfed contrast.
4. **Study 1's decline across Kherson Oblast was real, but an oblast average cannot say what caused it.** It mixes the greening reservoir, the flood, farmland and the war's other effects. To link change to one act, the analysis has to follow the physical footprint of each pathway.

## Main limitations

- **Irrigation measure.** Irrigation status is based on NDVI and mostly captures summer crops.
- **Weather and reference year.** Weather is not allowed to change the irrigated–rainfed contrast, and the reference year 2021 was the wettest of the record.
- **Exposed comparison land.** Irrigated land more than 5 km from the mapped canals counts as comparison land.
- **Parallel trends.** Pre-trend tests fail in most specifications; the one that passes was matched on the pre-war values it tests.
- **Small flood samples.** Few unflooded pixels look like the flooded floodplain, so the matched flood samples are small.
- **Scale of inference.** The canal zone and the flood are each one connected area, so the placebo tests are a better guide than the very small clustered p-values.
- **Timing of the revision.** It was written after the first results were known. I report it next to them, not instead of them.
- **Water maps.** The yearly water maps are coarse for 2023 and missing for 2024.
- **War data.** VIINA is based on news reports.
- **What NDVI shows.** NDVI measures greenness only.

## How to reproduce

- Data: `v2/01`–`08`.
- Main plan: `python v2/analysis/run_all.py`.
- Revision: `python v2/analysis/run_revision.py`.
- Later checks: `python v2/analysis/x1_review_diagnostics.py`.
- Results: `outputs/v2/study2_summary.json`, `outputs/v2/r1_summary.json` and `outputs/v2/x1_review_diagnostics.json`.
- All changes to the plans: `v2/DEVIATIONS.md`.
