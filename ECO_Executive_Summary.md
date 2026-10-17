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

- **Data.** MODIS NDVI at 250 m for 2016–2024, pixel by pixel.
- **Exposure groups.** Each group is defined by what physically happened to the land: flooded land (UNOSAT), the drained reservoir bed, and farmland served by the reservoir's canals.
- **Comparisons inside the war zone.** Flooded land against similar unflooded land on the same river bank; irrigated against non-irrigated farmland.
- **Plan fixed in advance.** The full analysis plan, including the words for each result, was public on GitHub before any data were downloaded (commit 521672f).
- **Registered revision 1** (commit 30e3840), written when the first results showed five problems: irrigation from 2010–2015, steppe-only comparison, district placebos, occupation and war intensity (VIINA), yearly water masks.
- **Registered revision 2** (16 Oct 2026; checksum in `v2/DEVIATIONS.md`, local commit only), written after an external review and before its data were downloaded: independent 30 m irrigation maps (Baber et al., 2026), flood matching on terrain instead of past greenness, weather allowed to change the irrigation contrast, a 2016–2018 baseline, block-bootstrap intervals for the decomposition, and a Sentinel-2 check of the reservoir result.

## What I found

| Pathway | Plan and revision 1 | Revision 2 | Verdict (rule fixed in advance) |
|---|---|---|---|
| **Flood** | All flooded pixels +0.010 NDVI (95% CI −0.004 to 0.025); matched samples +0.006 and +0.055 | Matched on terrain (59% of flooded pixels): −0.004 (−0.021 to 0.013), placebo p = 0.42; placebo-in-time test 0.000 | **not supported**: no lasting loss of July–October greenness |
| Floodplain wetlands | −0.041 and −0.061 | — | wetlands lost greenness |
| **Irrigated farmland** | NDVI-proxy groups: −0.074 and −0.053, but trends, weather and exposed comparison land made it untestable | Irrigated fields (Baber maps) vs never-irrigated cropland: **−0.179** (−0.211 to −0.147), a third of their 2016–2018 level; the drop starts with the breach; the placebo test fails (+0.050 in 2019–2021, the years that define the groups) | **suggestive** |
| **Reservoir bed** | NDVI > 0.3: 86–100 km² each year before the breach → 1,574 km² in 2024 | Sentinel-2 agrees within 18% where both can be compared | description |
| **Kherson Oblast** | 2021→2024: −0.029; reservoir bed +0.010 | 2016–18→2023–24: −0.020 (−0.025 to −0.015); irrigated cropland, 4% of the area, −0.008; never-irrigated cropland 0.000; flood 0.000 | description with intervals |

The NDVI-based irrigation proxy of the first two analyses agreed with the independent maps on only 16% of its "irrigated" pixels in Kherson Oblast (1% in Zaporizhzhia).

## What this means

1. **The reservoir bed changed the most.** About 1,500 km² became green within two seasons, as field studies also report (Kuzemko et al., 2025).
2. **No lasting loss of greenness on flooded land, except in wetlands,** whichever way the comparison land was chosen.
3. **Fields that lost canal irrigation lost about a third of their summer greenness.** The loss starts with the breach and is not explained by weather. The pre-registered rule still calls it *suggestive*: the fields were already diverging in 2019–2021, and with no irrigated land outside the canal system there is no way to separate the lost water from other war effects that hit irrigated farms harder.
4. **An oblast average cannot say what caused a change.** In Kherson it mixes a greening reservoir, a flood with no lasting effect, a large loss on a small irrigated area and almost no change elsewhere. The analysis has to follow the physical footprint of each pathway.

## Main limitations

- **Irrigation comparison.** No irrigated land outside the canal system was available, so the irrigation result cannot be separated from other war effects on irrigated farms.
- **Placebo test.** The irrigation groups are defined by 2019–2021 maps, and fields were greener in those years; field maps before 2019 do not exist.
- **Map quality.** The irrigation maps have their own errors and cover only Kherson and Zaporizhzhia.
- **Parallel trends.** Pre-trend tests fail in most specifications.
- **Timing of the revisions.** Both were written after earlier results were known; revision 2 is dated only by a local commit.
- **Water maps.** The yearly water maps are coarse for 2023 and missing for 2024, which limits the reservoir checks.
- **War data.** VIINA is based on news reports.
- **What NDVI shows.** Greenness only; July–October misses spring and winter crops.

## How to reproduce

- Data: `v2/01`–`11`.
- `python v2/analysis/run_all.py`, `run_revision.py`, `run_revision2.py`.
- Results: `outputs/v2/study2_summary.json`, `r1_summary.json`, `r2_summary.json`.
- All changes to the plans: `v2/DEVIATIONS.md`.
