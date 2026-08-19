# ECOCIDE
### A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes

Executive Summary · DOI: 10.5281/zenodo.21757974 · Sakshi D. Maske

## The Question

On 6 June 2023, Ukraine's Kakhovka Dam was destroyed, draining an 18.2 km³ reservoir and flooding downstream floodplain. Legal bodies are now considering "ecocide" as a prosecutable international crime, but existing satellite assessments of this event rely on visual, qualitative interpretation and explicitly decline to establish statistical causality. Can a causal-inference framework independently quantify conflict-attributable environmental damage, separated from Ukraine's already-elevated conflict baseline — and does that quantification hold up against more than one hand-picked control zone?

## The Method

A Difference-in-Differences (DiD) model compares Kherson, Ukraine (treatment) against a matched non-conflict control panel of four Danube/Black Sea Romanian counties — Tulcea, Galati, Braila, Constanta — chosen for comparable pre-conflict ecology (river-delta wetland, steppe, agricultural floodplain, coastal) while remaining genuinely non-combatant, with month fixed effects to isolate the conflict-attributable effect from seasonal cycles. The primary specification (Kherson against Tulcea alone) uses Newey-West HAC standard errors, since a two-unit design has too few clusters for cluster-robust inference; as a robustness check, the same model is run against the full four-county panel, which reports both HAC and cluster-robust specifications side by side. Flood extent is sourced from UNOSAT's verified multi-sensor product (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS) rather than derived independently from raw bands.

## The Finding

A statistically significant, causally-validated NDVI decline was detected in Kherson relative to Tulcea, the primary control zone, following the dam's destruction — confirmed through a clean placebo test using a counterfactual pre-event date. As a robustness check across the full four-county panel, the effect held at a similar magnitude, reproducing independently in three of the four controls.

| Metric | Value |
|---|---|
| NDVI DiD Coefficient (primary specification, Tulcea) | -0.0703 |
| P-value (HAC-robust) | 0.022 — significant |
| 95% Confidence Interval | [-0.130, -0.010] |
| NDVI DiD Coefficient (four-county panel, pooled robustness check) | -0.0600 |
| P-value (HAC / cluster-robust) | 0.029 / 0.002 — significant |
| Per-control check | 3 of 4 controls confirm; Constanta does not |
| Placebo Test #1 (fake date, June 2022, primary specification) | +0.0148, p = 0.612 — clean pass |
| Placebo Test (four-county panel, fake date) | +0.0222, p = 0.216 — clean pass |
| Peak Flood Extent (9 June 2023) | 464.18 sq. km (UNOSAT, 5-sensor verified) |

## Validation & Robustness Checklist

- Matched non-conflict control panel — four Danube/Black Sea Romanian counties (Tulcea, Galati, Braila, Constanta), with Tulcea as the primary specification and the full panel as a pooled robustness check
- HAC-robust standard errors (Newey-West correction) throughout; cluster-robust reported alongside HAC for the four-county panel
- Placebo Test #1 — clean pass on the primary specification, and again on the four-county panel
- Placebo Test #2 — genuine failure disclosed on a narrowed baseline (see limitation below)
- Quarterly event-study validation on the primary specification; four-county panel version shows a genuinely noisier quarterly signature (disclosed, not hidden)
- Month fixed effects (seasonal controls)
- Multi-sensor verified flood data (UNOSAT, 5 independent sensors)

## Honest Limitations

A quarterly event study found a significant effect in a pre-treatment quarter (summer 2022) — traced to Kherson already being an active conflict zone before the dam's destruction, meaning the baseline wasn't a genuinely quiet pre-conflict period. A narrowed-baseline specification built to address this produces a larger effect (-0.1384, p = 0.0001) but its own placebo test fails once the correct HAC standard errors are applied (p = 0.001) — a genuine validation failure, disclosed as such and kept only as an illustrative sensitivity check.

Cluster-robust inference is not possible on the primary (two-zone) specification — one treatment zone against one control zone leaves no room for clustering. The four-county panel was built in part to test this directly, and the pooled effect holds there too, but the panel comes with two honestly disclosed complications of its own: Constanta, the most purely coastal and urbanized of the four controls, does not reproduce the effect (an open question, not yet explained — plausibly because it is the furthest of the four from deltaic wetland character, though this is not confirmed); and at only 5 clusters (1 treatment + 4 control), cluster-robust standard errors are the bare minimum at which cluster-robust inference is even mathematically defined — not enough for full asymptotic reliability (30-40+ clusters is standard guidance) — so they are treated as a useful cross-check rather than a substitute for the primary HAC specification. This shows up most sharply in the quarterly event study on the four-county panel: with roughly 24 parameters against 5 clusters, cluster-robust standard errors become rank-deficient (rank 4, not 24) — an intrinsic property of a panel this small, not a sign of unusual precision — so HAC is reported instead for that specific model.

## Real-World Relevance

International courts have already accepted satellite evidence in war-crimes prosecutions — the ICC's Al Mahdi case was built on satellite imagery of cultural-heritage destruction — and Ukraine's own Criminal Code (Article 441, enacted 2001) already criminalizes "mass destruction of flora and fauna" causing ecological disaster. This project applies the same causal-inference discipline used in policy evaluation to that evidentiary question, at the standard open-source investigators like Bellingcat and Human Rights Watch hold themselves to.

GitHub: github.com/sakshimaske303-commits/ECOCIDE | Live Dashboard: ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app | Zenodo DOI: 10.5281/zenodo.21757974

Sakshi D. Maske — Independent Geospatial Researcher
