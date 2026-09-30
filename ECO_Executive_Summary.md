# ECOCIDE — Executive Summary

**What did the destruction of the Kakhovka Dam do to vegetation? Separating flood, reservoir and irrigation effects with satellite data**

Sakshi D. Maske · Independent Geospatial Researcher · Code and data: github.com/sakshimaske303-commits/ECOCIDE · Full paper: `ECO_Research_Paper_v2.md`

## The question

The Kakhovka Dam was destroyed on 6 June 2023. This could have changed vegetation in three ways:

- the flood below the dam;
- the draining of the reservoir;
- the loss of water for the irrigation canals.

All three happened inside an active war zone. I wanted to know which of them left a mark on vegetation that can be separated from the war itself.

## Why I needed a second study

My first study (Study 1) compared the average greenness (NDVI) of the whole of Kherson Oblast with four counties in Romania. Kherson became less green after June 2023 (−0.108, p = 0.037). But I could not show that the dam caused this:

- the flood covered only 2% of the oblast;
- the two areas were already moving apart before the event;
- when each area was treated as the "affected" one in turn, Kherson ranked only second of five (p = 0.40).

## What I did in Study 2

- **Data.** I used MODIS NDVI at 250 m for 2016–2024 (2010–2015 for the revision) and looked at each pixel.
- **Exposure groups.** I defined each group by what physically happened to the land: flooded land (UNOSAT maps), the drained reservoir bed, and farmland near the reservoir's canals (OpenStreetMap).
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

## What I found

| Pathway | Main plan | Revision | What it means |
|---|---|---|---|
| **Flood**: flooded vs matched unflooded land | +0.006 NDVI (95% CI −0.014 to 0.026); placebo p = 0.63 | +0.055 (flooded land greener) | No lasting loss of greenness |
| Floodplain wetlands | −0.041 | −0.061 | Wetlands did lose greenness |
| **Irrigated farmland**: canal zone vs elsewhere | −0.074, but already falling before the war | −0.053; no change after the breach compared with 2021 (−0.006 to −0.014, not significant); placebo p = 0.38 | The decline came before the war; no effect of the breach detected |
| **Reservoir bed** | Area with NDVI above 0.3: about 95 km² before the breach, 906 km² in 2023, 1,574 km² in 2024 | Same path on land-only pixels | Largest and clearest change |
| **Kherson Oblast, 2021 to 2024** | −0.029 overall; −0.024 of it from land not exposed to any pathway | −0.052 (reservoir bed removed by the water rule) | Most of the decline is not from the dam |

By the naming rule in my plan, the flood result is "not supported" and the irrigation result is "suggestive". In plain terms: **I found no loss of greenness on flooded land (except wetlands), and no change on canal-zone farmland after the breach.**

## What this means

1. **The reservoir bed changed the most.** About 1,500 km² became green within two seasons. Field studies report the same (Kuzemko et al., 2025).
2. **The flood did not cause a lasting loss of summer greenness, except in wetlands.** The wetland loss may come from the lower, unregulated river after the dam's loss rather than from the flood itself.
3. **The irrigation loss was not detected by my design, even though it happened.** Other work shows that irrigated area fell by about 90% (Baber et al., 2026; NASA Harvest). My NDVI-based "irrigated" group mostly captures summer crops, and the farmland trend was already moving before the war. Field-level irrigation maps are needed for this question.
4. **Study 1's decline across Kherson Oblast was real, but mostly not caused by the dam.** An oblast average mixes effects with opposite signs. To link change to one act, the analysis has to follow the physical footprint of each pathway.

## Main limitations

- **Irrigation measure.** Irrigation status is based on NDVI and is weak.
- **Parallel trends.** Pre-trend tests fail in most specifications.
- **Small flood samples.** Few unflooded pixels look like the flooded floodplain, so the matched flood samples are small.
- **Timing of the revision.** It was written after the first results were known. I report it next to them, not instead of them.
- **Water maps.** The yearly water maps are coarse for 2023 and missing for 2024.
- **War data.** VIINA is based on news reports.
- **What NDVI shows.** NDVI measures greenness only.

## How to reproduce

- Data: `v2/01`–`08`.
- Main plan: `python v2/analysis/run_all.py`.
- Revision: `python v2/analysis/run_revision.py`.
- Results: `outputs/v2/study2_summary.json` and `outputs/v2/r1_summary.json`.
- All changes to the plans: `v2/DEVIATIONS.md`.
