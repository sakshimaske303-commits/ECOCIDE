# ECOCIDE — Research Completion Plan (the finish line)

Written 16 October 2026. This file fixes **what is left to do, and where the research stops.**
Anything not listed here is *not* part of this research. New ideas go into the paper's "Future work" paragraph, not
into new analyses.

---

## 1. The one question, and the shape of the final answer

**Research question.** Which physical pathway of the Kakhovka Dam's destruction — the flood, the drained reservoir, or
the loss of canal irrigation — left a detectable mark on vegetation, compared with similar land in the same war zone?

The finished paper gives **one answer per pathway**, each from one analysis:

| Pathway | Analysis | Status today | Final answer will be |
|---|---|---|---|
| Flood (H1) | flooded vs similar unflooded land | done, but matched on the outcome | redone with non-outcome matching (L4) |
| Reservoir bed (H3) | descriptive time series | done, strong | + one independent check (L8) |
| Irrigation loss (H2) | irrigated vs non-irrigated cropland | **not testable with the current NDVI proxy** | redone with independent irrigation maps (L1–L3) |
| Kherson Oblast as a whole (H4) | decomposition | descriptive, no uncertainty | redone with the new exposure and intervals (L6) |

Whatever the new results show — effect, no effect, or still inconclusive — they are written up as they come out
(Section 6). The research is then complete.

---

## 2. Limitations that could still cause desk rejection — and the fix for each

Ranked by risk. **A** = must fix. **B** = should fix. Each fix has a clear "done when".

### L1 [A] The irrigation exposure is not irrigation
- **Problem.** "Irrigated" is defined by July–August NDVI, which mostly picks up summer crops. In zone K alone the
  proxy marks about 97,000 pixels (≈ 5,200 km²) as irrigated, while the independent maps of Baber et al. (2026) give
  about 1,880 km² (188 kHa) of irrigated land in the whole of Kherson and Zaporizhzhia oblasts before the war. Any
  reviewer who knows that paper will reject an irrigation test built on this proxy.
- **Fix.** Use the Baber et al. (2026) 30 m irrigated-field maps (Zenodo record 22036773, CC BY 4.0, 2019–2025,
  ≈ 520 MB) as the exposure: the share of each 231 m pixel that was irrigated in 2019–2021.
  - Validate the NDVI proxy against these maps (confusion matrix by oblast) and report it.
  - Design (fixed in Addendum 2 before the data are opened): pixels mostly irrigated in 2019–2021 vs cropland never
    irrigated in 2019–2021, in Kherson and Zaporizhzhia oblasts, 2023–24 vs 2016–2018 (years not used to define
    irrigation). If at least 1,000 irrigated pixels lie more than 30 km from the Kakhovka canal network, add those as
    a second comparison (triple difference); otherwise not.
- **Done when.** H2 estimate, event study, placebo test and the validation table exist in `outputs/v2/r2_*.json`.
- **Note for the paper.** Baber et al. mapped the irrigated *area*; they did not measure what its loss did to
  vegetation. Measuring that is this paper's contribution on H2.

### L2 [A] Weather and the reference year (H2)
- **Problem.** The irrigated–rainfed contrast follows summer rain (r = −0.97, 2016–21), the models add weather only as
  separate terms, and the reference year 2021 was the wettest summer of the record.
- **Fix.** Interact July–October rainfall and temperature with the irrigation group (all lower-order terms included);
  report effects at the 2016–2021 average weather; event studies against the 2016–2018 mean instead of 2021.
- **Done when.** Part of the L1 run.

### L3 [A] Comparison land partly irrigated from the same canals (H2, H4)
- **Problem.** The 5 km canal buffer misses irrigated land; the most negative "placebo" districts are canal districts.
- **Fix.** Zone O and all placebo districts must lie more than 30 km from the canal network. In the new H2 design,
  never-irrigated comparison cropland must also lie more than 5 km from any field Baber et al. map as irrigated in
  2019–2021.
- **Done when.** Part of the L1 run.

### L4 [A] Flood matching uses the outcome itself (H1)
- **Problem.** Matching on 2016–2021 NDVI makes the flat pre-trend automatic, can create regression to the mean, and
  keeps only 1.8% of flooded pixels.
- **Fix.**
  1. Placebo in time: match on 2016–2018, "estimate" 2019–2021. A non-zero result measures the bias.
  2. Match instead on things the flood cannot change: height above the nearest drainage and slope (Copernicus DEM
     GLO-30, free), distance to the main channel, and WorldCover class shares.
  3. Report the unmatched estimate (all flooded pixels) next to it as the area-wide result.
- **Done when.** `outputs/v2/r2_h1_*.json` holds these three results.

### L5 [A] Inference at the wrong scale (H1, H2)
- **Problem.** Each treatment is one connected area; 10 km clusters give p-values like 10⁻²⁶ that overstate certainty.
- **Fix.** Placebo (randomization) p-values become the primary test; also report Conley errors at 50 and 100 km. Stop
  quoting tiny clustered p-values in the abstract.
- **Done when.** Part of the L1 and L4 runs; abstract uses placebo p-values.

### L6 [B] The Kherson decomposition (H4) has no uncertainty
- **Fix.** Use the new exposures (Baber irrigated land, flood, reservoir), 2016–2018 mean → 2023–24 mean, weather
  adjustment from the L2 model, and 95% intervals from a block bootstrap. If it still cannot separate irrigation loss
  from other war effects, H4 is reported as descriptive only, in one short paragraph.
- **Done when.** `outputs/v2/r2_h4.json` with intervals.

### L7 [A] Contribution not clear against recent work
- **Problem.** The reservoir greening (Kuzemko et al., 2025) and the irrigation collapse (Baber et al., 2026) are
  already published. A reviewer will ask what is new.
- **Fix.** Rewrite the introduction and discussion around one contribution: *the first counterfactual test of all three
  pathways of the dam's destruction in one design, inside the war zone* — including the first estimate of what the lost
  irrigation did to vegetation, and a measured null for lasting flood damage outside wetlands. Add the missing
  literature (about 10–15 references: dam-break and floodplain vegetation, drought and irrigation remote sensing,
  matching in difference-in-differences, Baber et al. 2026 Frontiers paper).
- **Done when.** New introduction, Section 2.3 and Discussion; no other section grows.
- ☑ 16 Oct: Sections 2.2–2.4 rewritten with 12 verified references (Baber et al. 2026 paper, Pichura & Potravka 2025,
  Lischenko et al. 2025, Shults 2025, Skakun et al. 2019, Witmer 2015, and the methods papers). Introduction and
  Discussion wait for the new results (Phase 5).

### L8 [B] No independent check of a derived layer
- **Fix.** One check only: compare the MODIS reservoir-bed result for 2024 (area with NDVI > 0.3) with a Sentinel-2
  10 m NDVI composite of August 2024 over the same bed. Report the agreement in one sentence and one supplementary
  figure. The L1 confusion matrix is the second validation.
- **Done when.** One number and one figure.

### L9 [B] Pre-registration credibility
- **Fix (decision of 16 Oct: no OSF).** Commit Addendum 2 locally before any new data are downloaded. Its
  SHA-256 checksum is in `v2/DEVIATIONS.md` §6 and the analysis code refuses to run if the file changes. The paper
  says plainly that the only record of its date is the author's own git commit, and that it was written after the
  review checks were known.
- ☑ 16 Oct: Addendum 2 approved (v1.0), checksum recorded, all download and analysis code written and checked on a
  synthetic world; committed 16 Oct (07b8ad1) before steps 9–11 were run.
- **Done when.** The paper states the commit and the limitation.

### L10 [B] Reproducibility
- **Fix.** One command reruns everything (`run_all.py`, `run_revision.py`, the new `run_revision2.py`); tests pass;
  frozen inputs that cannot be re-downloaded identically (OSM canal extract, WorldCover fractions, annual composites,
  Baber subset) go into one Zenodo archive.
- **Done when.** A clean run reproduces every number in the paper.

### L11 [B] Figures
- **Fix.** Exposure map with boundaries, labels, coordinates and an inset; rainfall panel under the H2 event study;
  one map of the Baber irrigated fields; updated H4 figure with intervals. No other new figures.

### L12 [A, non-scientific] Repository hygiene
- ☐ Change the Sentinel Hub / CDSE credentials that are in the git history.
- ☑ 16 Oct: removed duplicates and leftovers (`v2/04b_*`, `v2/05_*`, `v2/07_download_io_lulc.py`,
  `v2/08_download_conflict.py`, `data/ndvi` = identical copy of `data/ndvi_v2`, `qgis_processing/`,
  `outputs/proof_screenshots/02–04`, nine one-off `verify_*.py`). `__pycache__` was already ignored.
- ☑ 16 Oct: licence split — MIT for code (`LICENSE`), CC BY 4.0 for text and figures (`LICENSE-CC-BY-4.0`); GADM files
  no longer tracked (`download_gadm.py` + extract scripts); ODbL notice for the OSM canal layer in README.
- ☑ Removal committed (16 Oct).

---

## 3. What we will NOT do (scope fence)

These are good ideas, but they are outside this research. Each gets at most one sentence under "Future work".

- No 2025 season (would need new MODIS downloads and re-registration).
- No re-run of the whole study at Sentinel-2 10 m.
- No SAR, crop-type mapping, yield, soil contamination, salinity or biodiversity analysis.
- No new hypotheses, pathways, regions or countries.
- No more Study 1 work (synthetic control, more controls, more HAC variants). Study 1 stays as the background study.
- No machine-learning models, field work or interviews.
- No re-specification after seeing Addendum 2 results. Every analysis in Addendum 2 runs once, as registered.

---

## 4. Order of work

| Phase | What | Done |
|---|---|---|
| 0 | Change credentials; commit the review changes | ☑ commits; ☐ credentials |
| 1 | Finalise Addendum 2 (L1–L6, L8); commit locally (no OSF) | ☑ 16 Oct (07b8ad1) |
| 2 | Download Baber maps, Copernicus DEM, Sentinel-2 Aug 2024 bed composite | ☑ 16 Oct |
| 3 | Run Addendum 2 analyses once (`run_revision2.py`) | ☑ 16 Oct (repeated once with the DEM rule, see DEVIATIONS §6) |
| 4 | Write results into paper, summary, README, dashboard; new figures (L11) | ☑ 17 Oct |
| 5 | Introduction, literature and contribution rewrite (L7) | ☑ 17 Oct |
| 6 | Repository hygiene, licence, Zenodo archive, clean full re-run (L10, L12) | ☑ hygiene, licence, re-run (16–17 Oct); ☐ Zenodo archive |
| 7 | Final consistency check of every number; tag version 3.0.0; push to GitHub (first push since 16 Oct) | ☑ check (17 Oct); ☐ tag and push |

---

## 5. Definition of done — the full stop

The research is **complete** when every box below is ticked. Then we stop.

- ☑ Addendum 2 committed (checksum in DEVIATIONS §6) before its data were downloaded; the paper states that the date
  rests on the author's own git commit.
- ☑ H1, H2, H3, H4 each have one final result and one plain-language verdict, traceable to one JSON file.
- ☑ The irrigation exposure comes from independent maps, and the NDVI proxy's error is reported.
- ☑ Weather is allowed to change the irrigated–non-irrigated contrast; event studies do not use 2021 alone as reference.
- ☑ Zone O and placebo districts lie more than 30 km from the canal network; never-irrigated comparison cropland lies
  more than 5 km from mapped irrigated fields.
- ☑ Flood matching does not use the outcome; the placebo-in-time bias test is reported.
- ☑ Placebo p-values are the headline tests (flood); district-cluster bootstrap for the irrigation design (Addendum 2, R11).
- ☑ One independent validation each for H2 (confusion matrix) and H3 (Sentinel-2 check).
- ☑ Introduction states one contribution, positioned against Kuzemko et al. (2025) and Baber et al. (2026).
- ☐ Paper, executive summary, README, CITATION and dashboard give the same numbers and the same answer.
- ☑ One clean re-run reproduces every number; tests pass (16–17 Oct; DEVIATIONS §7).
- ☐ Credentials changed; repository cleaned; licence fixed; inputs archived; version 3.0.0 tagged.

**After this point only these are allowed:** journal choice and formatting, DOIs (Zenodo, EarthArXiv), cover letter,
and changes a journal's reviewers ask for.

---

## 6. Stopping rules for the new results

Decided now, so that no result leads to more analysis.

- **H2 shows a significant negative effect that passes the placebo test** → "supported"; write it up.
- **H2 is negative but fails the placebo or sensitivity test** → "suggestive"; write it up with the reason.
- **H2 is near zero with a tight interval** → "no detectable effect on July–October greenness", noting that farmers
  switched to winter crops (Baber et al., 2026), which this outcome window does not capture. Write it up.
- **H2 is still too imprecise** → "the irrigation pathway could not be resolved at 250 m"; write it up.
- **H1 placebo-in-time shows bias** → report the bias-corrected range and the unmatched estimate as the main result.
- **Anything surprising** → one sentence in the Discussion or Future work. **No new analysis.**

In every case the next step is writing, not more analysis.

---

## 7. What the finished paper will claim (and no more)

1. The drained reservoir bed became about 1,500 km² of green land within two seasons (description, independently
   checked).
2. Flooded land showed / did not show a lasting change in July–October greenness, measured against land matched on
   terrain rather than on past greenness; floodplain wetlands are reported separately.
3. Previously irrigated fields did / did not lose July–October greenness relative to never-irrigated cropland after
   the breach, using independent irrigation maps, with weather allowed to change the contrast.
4. An oblast average mixes these pathways; with physical exposure maps, X% of Kherson Oblast's change can be assigned
   to them (with intervals).
5. Method lesson: attribution of war damage needs exposure-based units, comparisons inside the war zone, validated
   exposure maps, and a plan fixed in advance.
