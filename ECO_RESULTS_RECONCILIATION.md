# ECOCIDE — Results Reconciliation Table

Baseline snapshot taken 2026-09-11, after Phase 1 (existing-data fixes) and Phase 2 (true
GADM-polygon NDVI extraction + pixel-level Sentinel-2 SCL cloud masking + full pipeline
rerun on the corrected data). Phase 2's numbers are now filled in below. **The headline
result changed materially under Phase 2**: the primary DiD weakened from HAC p=0.022 to
p=0.060, and the placebo-in-space check (row 12/13) shows Kherson is no longer the most
extreme of the five geographic units, with two Romanian control counties (Brăila,
Constanța) now independently significant in the control-only spillover check (row 15).
`ECO_Research_Paper.md` has been fully rewritten to reflect this (see its own text for the
reasoning). This table now tracks propagating the same corrected numbers into every other
file that states them.

## How to use this file

For every row below, the "New value (Phase 2)" column is now filled in from
`/home/claude/eco_check/full_v2_battery.py`. Grep each file listed under "Appears in" for
the "Old value" string and replace it with the new one, using the same honest framing
already applied in `ECO_Research_Paper.md` (do not just swap the number and leave
"statistically significant, placebo-validated" language in place — the significance
verdict itself changed for several of these). Do not consider Phase 2 finished until every
row in this table, and every file in "Files not yet checked," has been checked off.

## Primary results

| # | Quantity | Old value (bbox-based) | New value (Phase 2, polygon+SCL) | Appears in |
|---|---|---|---|---|
| 1 | Primary DiD (Kherson vs Tulcea), coefficient | −0.0703 | **−0.0747** | ECO_Research_Paper.md (Abstract, §4.2, §8) ✅ done; README.md, CITATION.cff, dashboard/app.py, ECO_Executive_Summary.md — not yet |
| 2 | Primary DiD, HAC p-value | 0.022 (also 0.026 in some re-derivations) | **0.060 — no longer significant at conventional 5% level** | same files as #1 |
| 3 | Primary DiD, 95% CI | [−0.130, −0.010] | **[−0.153, 0.003] — now straddles zero** | ECO_Research_Paper.md ✅ done; dashboard/app.py — not yet |
| 4 | Pre-treatment mean NDVI, Kherson | 0.222 | **0.3205** | ECO_Research_Paper.md §3.4, §4.2 ✅ done |
| 5 | Pre-treatment mean NDVI, Tulcea | 0.203 | **0.3156** | ECO_Research_Paper.md §3.4 ✅ done |
| 6 | Broad placebo, coefficient / p | +0.0148 / p=0.612 | **+0.0051 / p=0.882 (still clean)** | ECO_Research_Paper.md §4.2, §4.4 ✅ done; README.md, dashboard/app.py — not yet |
| 7 | Narrowed-baseline DiD, coefficient / p | −0.1384 / HAC p=0.0001 | **−0.1497 / HAC p=0.0004 (still significant, slightly stronger)** | ECO_Research_Paper.md §4.3, §4.4 ✅ done |
| 8 | Narrowed-baseline placebo, coefficient / p | −0.1382 / HAC p=0.001 | **−0.1098 / HAC p=0.069 — no longer significant (this specific check improved)** | ECO_Research_Paper.md §4.3, §4.4, §6 ✅ done |
| 9 | Four-county panel DiD, coefficient / p | −0.0600 / HAC p=0.029 | **−0.0661 / HAC p=0.059 — no longer significant** | ECO_Research_Paper.md §4.5, §6, §8 ✅ done; README.md, CITATION.cff — not yet |
| 10 | Four-county panel, cluster-robust p (cross-check only) | 0.002 | **0.034** | ECO_Research_Paper.md §4.5 ✅ done |
| 11 | Per-control breakdown: Tulcea / Galați / Brăila / Constanța | −0.0703 (p=0.022) / −0.0695 (p=0.026) / −0.0937 (p<0.001) / −0.0064 (p=0.808) | **−0.0747 (p=0.060) / −0.0805 (p=0.035) / −0.1277 (p=0.006) / +0.0186 (p=0.602, sign flipped)** | ECO_Research_Paper.md §4.5 ✅ done |

## Section 4.6–4.10 checks

| # | Quantity | Old value | New value (Phase 2, polygon+SCL) | Appears in |
|---|---|---|---|---|
| 12 | Placebo-in-space: Kherson / Tulcea / Galați / Constanța / Brăila did_term (HAC p) | −0.0600 (0.030, rank 1/5) / +0.0279 / +0.0269 / −0.0520 / +0.0571 | **−0.0661 (0.059, rank 2/5 one-sided, 3/5 two-sided) / +0.0273 / +0.0345 / −0.0893 (0.048) / +0.0935 (0.015)** — Kherson is no longer the most extreme unit | ECO_Research_Paper.md §4.6 ✅ done |
| 13 | Exact randomization p-value | 1/5 = 0.20 (best possible) | **2/5 = 0.40 one-sided, 3/5 = 0.60 two-sided** | ECO_Research_Paper.md §4.6, Abstract, §6, §8 ✅ done |
| 14 | Event-study quarterly p-values (11 quarters) + Bonferroni/BH results | 2 of 4 flagged quarters survive Bonferroni | **4 of 11 quarters survive Bonferroni (stronger); +1 more survives BH** — see §4.7 table | ECO_Research_Paper.md §4.7 ✅ done |
| 15 | Control-only spillover: Tulcea / Galați / Brăila / Constanța did_term,p | +0.0137,0.642 / +0.0127,0.691 / +0.0449,0.069 / −0.0714,0.033 | **+0.0116,0.742 / +0.0192,0.567 / +0.0821,0.027 (now significant) / −0.1129,0.020 (more significant)** — TWO controls now significant, not one | ECO_Research_Paper.md §4.8, §6 ✅ done |
| 16 | HAC lag-length sensitivity (maxlags 1–6) | p range 0.011–0.026 (always significant) | **p range 0.027–0.063 (straddles 0.05 depending on lag choice)** | ECO_Research_Paper.md §4.9 ✅ done |
| 17 | log(NDVI) functional-form check | coefficient ≈ −0.49 (≈49% proportional), p=0.055 | **coefficient ≈ −0.25 (≈25% proportional), p=0.081** | ECO_Research_Paper.md §4.9, §6 ✅ done |
| 18 | Low-coverage-month check (Model A vs B) | 50% threshold, 1 month dropped: −0.0703 (p=0.026) vs −0.0699 (p=0.030) | **15%/25% thresholds (50% no longer meaningful — see §3.3/§4.10): −0.0747 (p=0.060) vs −0.0733 (p=0.070) at 15%, vs −0.0731 (p=0.083) at 25% — cleaning weakens further, not less** | ECO_Research_Paper.md §4.10, §6 ✅ done |

## New in Phase 2 (not in the Phase 1 table)

| Quantity | Value | Appears in |
|---|---|---|
| Kherson worst-month valid-pixel fraction (Dec 2022) | 7.9% (was 31.4% under bbox) | ECO_Research_Paper.md §6 ✅ done |
| Zone polygon-to-bbox area ratios (explains the lower coverage ceiling) | kherson 0.498, tulcea 0.658, galați 0.664, constanța 0.432, brăila 0.649 | ECO_Research_Paper.md §3.3 ✅ done |
| Multi-control quarterly event study, treatment quarter / +1yr | Q0: p=0.278 (not sig, same as before) / Q+4: p=0.0001 (still sig) | ECO_Research_Paper.md §4.5 ✅ done |
| Multi-control broad placebo (HAC / cluster) | +0.0421, HAC p=0.338 (clean) / cluster p=0.078 (borderline, was 0.216) | ECO_Research_Paper.md §4.5 ✅ done |

## Removed / demoted (do not resurrect without a reproducible script)

| Quantity | Status | Reason |
|---|---|---|
| ~10,800 km² analysis corridor / 4.3% flooded at high water | Removed from ECO_Research_Paper.md §4.1 | Manually delineated, no surviving script to regenerate it |

## Wording flags — status after Phase 2

- Title / framing of the project as a general "evidentiary framework for war-time environmental crimes" (README.md title, CITATION.cff `title` field) is broader than the single-case-study scope the paper demonstrates. **Still not changed** — CITATION.cff's title is tied to the published Zenodo DOI (10.5281/zenodo.21757974, v1.0.0); changing it would create a title mismatch against the already-published record. Still needs Sakshi's explicit decision before editing.
- Causal language was already softened in Phase 1; Phase 2 goes further in `ECO_Research_Paper.md` — the paper now explicitly states the primary result "no longer clears the conventional 5% significance threshold" rather than only softening "caused" to "associated with." This is a bigger change than a wording pass and needs to propagate to every other file with the same honesty, not just the same softened verbs.
- Constanța's wording ("independent post-event divergence... for a reason this design does not identify") is preserved and now extended to Brăila as well, since Phase 2's control-only spillover check (§4.8) found both significant.
- **New flag**: every remaining file below still states the ORIGINAL bbox-based numbers and the ORIGINAL "statistically significant, placebo-validated" framing. Until they are updated, the repo is internally inconsistent — the paper says one thing, everything else still says the stronger, superseded thing.

## Files not yet checked/updated against this table

- `README.md` — headline numbers and framing not yet updated (staged fresh, not yet edited)
- `CITATION.cff` — abstract/description field states old numbers; title question separately flagged above
- `dashboard/app.py` — headline metrics, CI, and "placebo-tested, HAC-robust" framing not yet updated
- `dashboard/static/*.pdf` — served copies; same staleness pattern as DOUBLE_JEOPARDY, needs the same check once the .md/.pdf sources are regenerated
- `ECO_Development_Log.md` / `.pdf`
- `ECO_Executive_Summary.md` / `.pdf`
- `ECO_Project_Report.md`
- `ECO_Research_Paper_EarthArXiv_Submission.pdf` — this is a PDF export of an even older version; needs full regeneration from the corrected .md, not a patch
- `ECOCIDE_Maps_and_Plots.pdf`
- `data/ndvi_v2/` has not yet been promoted to `data/ndvi/` — the old bbox-based data is still the one every *other* script in the repo (not just this paper) would read by default. Decide with Sakshi whether/how to do this promotion before regenerating any other document from code.
- GitHub `main` branch — push once all of the above is done, so any future external review reflects the corrected state, not the superseded one
