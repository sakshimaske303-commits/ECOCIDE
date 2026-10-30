# ECOCIDE: Declarations

**What Did the Destruction of the Kakhovka Dam Do to Vegetation? Separating Flood, Reservoir and Irrigation Effects with Satellite Data**

Sakshi D. Maske · Independent Geospatial Researcher · ORCID [0009-0002-5683-5966](https://orcid.org/0009-0002-5683-5966)

Version 3.0.0 · Code and data: [github.com/sakshimaske303-commits/ECOCIDE](https://github.com/sakshimaske303-commits/ECOCIDE)  
Earlier, superseded analysis: [EarthArXiv preprint v1](https://eartharxiv.org/repository/view/14827/)

## Highlights

- Each pathway of the dam's destruction, the flood, the drained reservoir and the loss of canal irrigation, is tested separately with MODIS NDVI (2016–2024), comparing exposed land with similar land inside the same war zone.
- Flooded land shows no detectable lasting loss of July–October greenness (matched estimate −0.004, 95% CI −0.021 to 0.013); floodplain wetlands are the exception.
- Fields irrigated in 2019–2021 lost 0.18 NDVI after the breach relative to never-irrigated cropland, a third of their earlier level; the pre-registered rule names this suggestive because the placebo test fails.
- The area of the drained reservoir bed with NDVI above 0.3 grew from 86–100 km² before the breach to 1,574 km² in 2024.
- In Kherson Oblast, previously irrigated cropland (4% of the area) accounts for −0.008 of a −0.020 relative change in summer NDVI; the flood accounts for almost none.

## Authorship and interests

This is single-author work. I designed the study, wrote the analysis plans, built and ran the pipeline, checked the results, wrote the paper and produced the figures (CRediT: Conceptualization, Methodology, Software, Validation, Formal analysis, Investigation, Data curation, Writing – original draft, Writing – review and editing, Visualization). No organisation funded it, and I met its costs myself. I have no competing interests. The study uses satellite and public geographic data only and involves no human participants, animals or personal data, so no ethical approval applied. The results describe changes in vegetation and say nothing about intent, military necessity or responsibility.

## Pre-registration and deviations

The main analysis plan was committed to the public repository on 24 September 2026, before the first data file was downloaded. A first registered revision was committed the same day, after the first results were known but before its extra data were downloaded or any of its analyses were run. A second registered revision, written after external reviews of the project, was committed on 16 October 2026 before its irrigation maps, elevation data and Sentinel-2 images were downloaded; its date rests on a local commit and a SHA-256 checksum that the code verifies, not on an independent registry. Every change to the plans, and every choice they did not cover, is listed in `v2/DEVIATIONS.md`. Checks added after all registered results were known are labelled exploratory and change no estimate or verdict.

## Data, code and licences

All inputs are open: MODIS, ESA WorldCover, Impact Observatory land cover, the Copernicus DEM and Sentinel-2 through the Microsoft Planetary Computer; ERA5-Land from the Copernicus Climate Data Store; UNOSAT flood layers; canals from OpenStreetMap (ODbL); conflict data from VIINA; and the irrigation maps of Baber et al. (2026; CC BY 4.0). GADM boundaries are downloaded by the code and not redistributed. Each result has a script in the repository that reproduces it, and `tests/` checks the estimation engine against direct calculations. The source code is under the MIT licence; text, papers, figures and derived results are under CC BY 4.0; third-party data keep their own licences.

## Earlier versions

Study 1, an oblast-wide comparison of Kherson with Romanian counties, first reported a significant effect (−0.0703, p = 0.022) based on bounding-box NDVI and stacked-panel standard errors; that result is superseded and kept only as the background study. In Study 2, the NDVI proxy for irrigation used in the plan and the first revision agreed with independent irrigation maps on only 16% of its "irrigated" pixels, and the second revision replaced it. `ECO_RESULTS_RECONCILIATION.md` lists every headline number, old against current, and the development log records each step.

## Statement on AI tools

Alongside the external reviews described above, I also used Claude (Anthropic), an AI assistant, for smaller and more routine tasks. I gave it the paper, summaries, README and dashboard text to compare against the JSON result files of the main plan and both revisions, so that a flood estimate, an irrigation coefficient or a verdict quoted in one place matched the others. I sometimes turned to it when a download or estimation script stopped with an error I could not trace, and I used it for the layout of the project web pages. The writing is mine: I asked it to point out passages that were unclear or too technical, places where something seemed missing, and punctuation, and I chose which of those suggestions to take. It had no part in writing the analysis plans, choosing the exposed and comparison groups, setting the decision rule or naming any result. It did not fetch or process the satellite data, and it did not run the models. Every suggestion was checked by me before I used it, and I am responsible for all of the content.

## Citation

Citation metadata are in `CITATION.cff`.
