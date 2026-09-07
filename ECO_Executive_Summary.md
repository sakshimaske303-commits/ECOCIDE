# ECOCIDE
### A Satellite-Based Evidentiary Framework for War-Time Environmental Crimes

Executive Summary · DOI: 10.5281/zenodo.21757974 · Sakshi D. Maske

# Project Overview

I developed ECOCIDE as a geospatial, Causal-inference product, having the primary aim of verifying claims of environmental degradation resulting from armed conflict without having to rely explicitly on the official government reporting, but also without being immune to any forms of human judgment as the data sources used in ECOCIDE are all publicly available and/or processed by third parties (i.e. Sentinel Hub, UNOSAT). International courts have now begun considering "ecocide"—a new kind of crime that goes beyond genocide, war crimes, crimes against humanity and aggression.

Even with that evolving, there remains no well accepted or statistically valid means of support for those damage claims. Even the most careful existing geospatial assessments rely on visual, qualitative comparisons of before-and-after imagery, and their own authors are forthright about their inability to make causal inferences from these types of comparisons (hence, responses like that of this blogger about objective scale indicators remaining to be done).

I fill that yawning void right here in a Difference-in-Differences framework that I've validated by placebo testing and an event-study analysis in order to distinguish the conflict-damaged trend from ones that otherwise would occur. The Kakhovka Dam's break on 6 June 2023, where an 18.2 km³ reservoir was drained and hundreds of square kilometres of floodplain below the dam were flooded, is the demonstration case. The control group is a four-county panel of Romania which is situated along the Danube/Black Sea corridor, and has very similar ecological baseline levels before the conflict, but is genuinely non-combatant.

## The Question

But can a causal-inference model truly account for the heightened wartime risk in Ukraine compared to a dedicated control area and will that distinction hold when compared to more than one set of handpicked control? Behind the current satellite monitoring of events such as the destruction of the Kakhovka dam lies solely visual, qualitative analysis, and it explicitly denies the possibility of establishing statistical causality, but as the legal procedures of this destruction start to be used as a basis for “ecocide” prosecutions, this situation is becoming indistinct.

But it's not hard to see, there's a real challenge that Kherson was no quiet territory prior to the dam collapse. It was already a battlefield; a comparison before/after alone cannot detect exactly what damage has been done by flooding as there is underlying general degradation affliction during wartime. My approach uses a Difference-in-Differences design where I benchmark Kherson to others counties of similar geographic and demographic characteristics during the same time frame.

Not satisfying more than one (handpicked) comparison is a necessary condition for the result to have any meaning. To see if the effect existed or if it was only the result of the county that was chosen for the control is to test it in all four Romanian counties in the control panel, not just in Tulcea.

## The Method

My core model is a Difference-in-Differences (DiD) model, where I compare the changes in NDVI levels in Kherson, Ukraine, with the changes in comparable NDVI levels in 4 other non-conflict "matched counties" in Romania along the Danube/Black Sea corridor: Tulcea, Galați, Brăila, Constanța — none of which were ever at war, so "prewar" doesn't really apply to them; it's their ecological comparability to Kherson that matters, not a shared conflict timeline. Having a monthly effect in my model removes any regular seasonality, and what remains is the signal due to the conflict.

For my main specification, I compare Kherson and Tulcea only, as I do not meet the criteria for a two-unit design to justify making any cluster-robust inferences. For robustness purposes, I re-estimates the same model using the complete four county panel; for both HAC and cluster-robust specifications. The "flood extent" information is not independent of the various bands of the satellite, but is part of the "available bands" derived by UNOSAT from its verified multi-sensor product composed of ICEYE radar data, Landsat-9, SkySat, WorldView-3, and MODIS.

## The Finding

−0.0703. That's the NDVI change I observed at Kherson when compared to Tulcea after the dam was destroyed and it passed the placebo test, which was also conducted on a fake date before the dam was destroyed and yielded a non-significant result. I would expect the same if the change was not real — just some trend that already existed — but it didn't happen in Kherson.

Over the entire four-county panel, I found that there was no effect that was washed out, as it remained of a similar magnitude and was reproduced independently in three of the four panel comparisons


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

- Non-conflict control: County of Tulcea (the principal specification) and the three other counties of the Danube/Black Sea region of Romania—Galați, Brăila, Constanța (full panel is also robustness checked as a pooled check)
- Standard errors: HAC-robust throughout; cluster-robust also reported alongside HAC for the four-county panel
- Placebo Test #1 — clean pass on the main specification, and clean pass again on the four-county panel
- Placebo Test #2 — a genuine failure, disclosed openly and not hidden, on a narrowed baseline (see below for limitation)
- Quarterly event-study check conducted on the main specification; the four-county panel version is reported too, but it is noisier in the quarterly version
- The seasonal cycles are controlled for by adding month fixed effects.
- Flood extent data based on multi-sensor verification – UNOSAT, from the combination of 5 independent sensors

## Honest Limitations

In my quarterly event study I found a nuisance effect in the pre-treatment quarter (2022 summer) before the dam has been destroyed. This is because Kherson was by then an active theatre of conflict — and a clean before/after design wouldn't really want the pre-conflict period to be as serene as Kherson in Ukraine was then. The effect is bigger (-0.1384) and statistically significant (p = 0.0001) when I use this "narrowed-baseline" specification... but the placebo test for that same narrowed specification, once I apply the correct HAC standard errors, also turns significant (p = 0.001) instead of staying clean. It is indeed a validation failure and not just a rounding error, which I am acknowledging; I don't keep the baseline result to be used as separate evidence, but only for reference to the problem posed by the pre-treatment quarter

I don't have the opportunity to do cluster-robust inference with my treatment vs control zones: there is only one zone of treatment and one zone of control. I tried to do some of this in the four-county panel I built, and the pooled effect is true for the four counties, too; but has two complications of its own. The most purely coastal and urbanized of the 4 controls, Constanța doesn't produce the effect — an open question I haven't yet settled on, but most likely because it's the furthest of the 4 from being river-delta "wildland". 5 clusters (1 treatment, 4 control) is not enough to rely on cluster-robust standard errors confidently – the numbers I used as a guideline for full asymptotic reliability were in the range of 30-40+ clusters, so I consider these as a cross-check and not as a replacement to the primary HAC specification.

I report HAC for that model because the thinness of the four-county panel is most noticeable in its quarterly event study, which has around 24 parameters against only 5 clusters, with this being a byproduct of the panel's size rather than an indication that the effect is somehow more precise in that panel.

## Real-World Relevance

Satellite images have already been admitted as evidence in war-crimes trials, such as Al Mahdi's case, brought before the ICC, and Ukraine's Criminal Code (Article 441 of 2001) already includes a section related to the "mass destruction of flora and fauna" that leads to "ecological disaster." I treat this as I would do in the evaluation of a policy, applying that causal-inference standard to that evidence-based question, as open-source investigators such as Bellingcat and Human Rights Watch do.

GitHub: github.com/sakshimaske303-commits/ECOCIDE | Live Dashboard: ecocide-xbub2cwcqjx9rkdd6nk5j5.streamlit.app | Zenodo DOI: 10.5281/zenodo.21757974

Sakshi D. Maske — Independent Geospatial Researcher
