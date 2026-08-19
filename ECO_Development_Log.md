# ECOCIDE: A Causal-Inference Framework for Independently Verifying War-Time Environmental Damage

Running log of every decision, data source, bug, and pivot in this project. Format: one entry per work session, most recent at the bottom.

ECOCIDE is a geospatial causal-inference framework I built to independently verify claims of environmental destruction arising from armed conflict, using Earth Observation data and statistical causal-inference methods rather than visual before-after image comparison. International legal bodies have started formally considering "ecocide" — mass environmental destruction — as a prosecutable international crime, but the geospatial assessments feeding that conversation, including the most recent published assessment of the Ukraine war, explicitly stop short of statistical causal attribution, describing observed changes as "conflict-associated" rather than conflict-attributable. ECOCIDE fills that specific gap: a Difference-in-Differences design, validated through placebo testing and event-study analysis, applied to the Kakhovka Dam's destruction against a matched non-conflict control zone.

## Index

1. [Entry 1](#entry-1)
2. [Entry 2](#entry-2)
3. [Entry 3](#entry-3)
4. [Entry 4](#entry-4)
5. [Entry 5](#entry-5)
6. [Entry 6](#entry-6)
7. [Entry 7](#entry-7)
8. [Entry 8](#entry-8)
9. [Entry 9](#entry-9)
10. [Entry 10](#entry-10)
11. [Entry 11](#entry-11)
12. [Entry 12](#entry-12)
13. [Entry 13](#entry-13)
14. [Entry 14](#entry-14)

---

## Entry 1

Started by locking down the actual research question rather than jumping straight to data. The existing published geospatial literature on Ukraine's war-related environmental damage relies on visual, qualitative before-after satellite comparison and explicitly declines to establish statistical causality — describing changes as "conflict-associated" rather than conflict-attributable. That's a reasonable choice for that prior work's broader descriptive aims, but it leaves a specific, acknowledged gap: no published framework I could find quantifies conflict-attributable environmental damage using a genuine causal-inference design — a matched non-conflict control zone, a Difference-in-Differences model, placebo validation.

That gap became the project's actual aim: build a reproducible geospatial framework that quantifies environmental damage statistically attributable specifically to armed conflict, distinguishing conflict-driven change from baseline environmental trends with quantified statistical confidence, rather than another qualitative before-after comparison. I picked the Kakhovka Dam's destruction (6 June 2023) and the surrounding Dnipro River floodplain and Donbas industrial region as the validation case, given how well-documented the conflict timeline and pre-conflict environmental baselines are for that specific event.

---

## Entry 2

Defining the treatment and control zones came before touching any data. The treatment zone was straightforward: the Kakhovka Dam area and Dnipro River downstream floodplain (46.777°N, 33.370°E), Kherson Oblast, Ukraine — a flood-affected analysis zone spanning roughly 10,800 km² from dam to river mouth, per UNOSAT's own satellite analysis.

The control zone took more thought. I first considered a within-Ukraine non-frontline zone like Dnipropetrovsk Oblast, but rejected it — reporting indicates the frontline has moved closer to that region, and war-adjacent economic and demographic effects (supply disruption, displacement) could contaminate a control zone even without direct conflict there. This is the same methodological risk I'd already run into in GPIE, where an internal-to-the-affected-region control group turned out not to be independent enough. I settled on the Danube Delta, Tulcea County, Romania (45.200°N, 29.500°E) instead — a comparable pre-conflict ecological baseline (river-delta wetland, Pannonian steppe, agricultural floodplain, similar continental climate) while being genuinely non-combatant. I explicitly checked that this is distinct from the Ukrainian side of the Danube Delta (Odesa Oblast), which has itself taken war-related strikes on port infrastructure and would have been unsuitable as a control.

---

## Entry 3

Pulled administrative boundaries for both zones from GADM version 4.1 — full country-level GeoPackage files for Ukraine and Romania, since GADM doesn't offer single-region downloads. Hit a naming inconsistency extracting them: Ukrainian oblasts sit at GADM's Level 1 (`NAME_1`), where Kherson matched directly. Romanian counties, though, aren't at the equivalent level — Level 2 in Romania's GADM schema is actually communes and small municipalities (hundreds of small place names), not counties, so Tulcea wasn't there. Checking Level 1 instead confirmed Romanian counties live there, and Tulcea extracted cleanly from it. This turned out to be a genuine cross-country inconsistency in GADM's own hierarchy numbering, not bad source data — I resolved it by actually inspecting each country's real level structure instead of assuming the numbering was consistent across countries.

Both boundaries got saved out independently, with confirmed bounding boxes: Kherson at 31.51°E–35.10°E, 45.90°N–47.58°N, and Tulcea at 27.99°E–29.72°E, 44.61°N–45.46°N.

---

## Entry 4

Pulled monthly NDVI for both bounding boxes via the Sentinel Hub Statistical API, January 2022 through November 2024 — 35 monthly points each — reusing the authentication module and evalscript pattern I'd already built for GPIE and DOUBLE JEOPARDY. Values came back in a plausible 0.07–0.17 range for winter months in a steppe/agricultural region, consistent with expected seasonal vegetation dormancy, and I accepted them as valid without further correction at this stage.

---

## Entry 5

NDWI turned into a genuine multi-attempt debugging chain. The first pull used the full Kherson Oblast bounding box at monthly resolution — and showed no discernible signal around the 6 June 2023 dam-destruction date at all. Rather than accept that as a null result, I dug into it: Kherson Oblast spans roughly 28,000 km², while the documented flood extent following the dam breach was only about 600 km² (UNOSAT). Averaging NDWI across the full oblast meant the flood signal, confined to about 2% of the box, was mathematically swamped by the unaffected 98%.

Narrowing the box to a tighter river corridor around the dam and floodplain helped a little — a marginally more plausible pre-breach reservoir-filling pattern in May 2023 — but still no clean spike in June or July. Two months returned no data at all, consistent with winter cloud cover, since Sentinel-2 is optical and can't see through it. Switching to weekly resolution on the same narrowed corridor actually made things worse in a specific, informative way: 3 June 2023, the week right before the dam's destruction, showed the single most negative (least-water-like) value in the whole window — the opposite of what flooding should look like.

Traced that to a structural problem in the box itself: it spanned both the upstream Kakhovka Reservoir, which drained rapidly after the breach (~18 km³ water loss), and the downstream floodplain, which flooded from the same event — two sub-regions moving in opposite directions, averaging out to noise. Splitting the box at the dam's exact latitude into separate upstream and downstream zones didn't fix it either; both still showed erratic, physically implausible week-to-week swings (one zone's water percentage jumping from 45% to 16% to under 3% across three consecutive weeks with no plausible mechanism). That volatility turned out to be sensor noise, not hydrology — Sentinel-2 is cloud-blocked, so each week's statistic comes from whatever cloud-free pixels happened to exist that week, a different random subset each time. The published Ukraine ecocide literature I'd already reviewed sidesteps exactly this by using radar-derived flood products instead of optical.

So I switched the upstream zone to Sentinel-1 SAR, which isn't blocked by cloud cover, using a standard −17 dB VV-polarization threshold to classify water pixels. That gave a clean, physically plausible signal: water percentage held around 2–5% through late May 2023, then dropped sharply the week of 3 June and stayed low (1–3%) through August with no reversion — a reservoir that drained and didn't refill, matching the known outcome. The downstream floodplain zone didn't get an equally clean signal from the same SAR approach — it oscillated in a narrower 4–6% band with an unexplained dip right after the breach, possibly because the flood's peak and recession both landed inside a single weekly composite window, or because flooded agricultural land produces a SAR signature that doesn't cross the same threshold calibrated for open reservoir water. I treated the upstream signal as clean enough to build the causal model on, and left the downstream floodplain as an open question rather than force-fitting the same threshold approach to it.

Looking back at the whole sequence: every unexpected or absent signal got treated as a diagnostic question — spatial dilution, opposing signals in one box, optical cloud contamination — rather than a dead end or an invitation to keep whichever result looked most convenient. Each fix traced to a specific, verifiable mechanism, not trial-and-error parameter tweaking, and the one piece that stayed unresolved got reported as unresolved.

---

## Entry 6

Rather than keep tuning a threshold on raw satellite bands for the downstream floodplain, I switched to sourcing a verified, pre-classified flood-extent product from an authoritative body — the same approach the published Ukraine ecocide literature already takes for this exact event. Found a comprehensive UNOSAT flood-mapping dataset via the Humanitarian Data Exchange (product code FL20230606UKR), built from multiple independent sensors (ICEYE radar, Landsat-9, SkySat, WorldView-3, MODIS Aqua/Terra) across several dates from 3 to 21 June 2023, each independently analyzed and quality-controlled by UNOSAT.

Loaded and verified the 6 June 2023 file — a single polygon in EPSG:4326, about 122.50 km² of flooded area on that date, smaller than UNOSAT's own later cumulative figure of ~600 km², which is consistent with flooding expanding progressively over the following two weeks rather than reaching full extent on day one. Loading all five available snapshots (6, 8, 9, 13, 21 June) gave a physically credible hydrograph: rapid expansion to a peak of 464.18 km² on 9 June, then steady recession to 21.17 km² by 21 June — a full rise-peak-recession cycle inside about two weeks. That explains why the independently-derived NDWI/SAR time series at weekly resolution never caught a clean signal: the flood's actual cycle moved faster than consistent cloud-free satellite revisits could reliably sample. This resolved the downstream measurement problem by substituting a verified, authoritative multi-sensor product for the specific dates needed, rather than further tuning a threshold that wasn't going to get there.

---

## Entry 7

Built the actual causal model, and it took several rounds to get to something trustworthy. The first Difference-in-Differences pass compared monthly NDVI between Kherson (treatment) and Tulcea (control) across the full 2022–2024 window, June 2023 as treatment — and came back weak and non-significant (R²=0.054, p=0.117). Rather than call that a null result, I treated the low R² itself as diagnostic: NDVI has strong, well-documented seasonal cycles, and a model explaining only 5% of variance pointed to a missing control variable, not an absent effect.

Adding month fixed effects confirmed that read directly — R² jumped to 0.747, and the same coefficient (did_term = −0.0703) came back statistically significant (p=0.007). The coefficient itself didn't move, only its estimated precision did, which is exactly what you'd expect if seasonal noise had been inflating uncertainty around a real effect rather than the effect being an artifact of a missing control. A placebo test with a fake June 2022 treatment date, restricted to pre-conflict data, came back near-zero and non-significant (0.0148, p=0.741) — a clean placebo requires both a near-zero coefficient and a high p-value together, and this had both, which is about as strong a validation as you get short of a randomized experiment.

Tried to push further with a full monthly-resolution event study, following the same category of check I'd used in GPIE's 23-quarter analysis — and it failed technically: with only 70 observations against roughly 68 needed parameters, the model went rank-deficient and every p-value came back NaN. That's an over-parameterization problem specific to this project's much smaller sample relative to GPIE's 27-country panel, not a flaw in the event-study logic itself, so I dropped to quarterly bins instead to bring the parameter count under the observation count.

The quarterly event study surfaced a genuine problem rather than a clean confirmation: post-event quarters showed significant negative effects (Quarter 0: p=0.035; Quarter +4: p=0.0001), but one pre-event quarter — summer 2022 — also came back significant (p=0.007), which isn't consistent with a clean parallel-trends assumption. I investigated rather than just flag it: Kherson Oblast was already an active conflict site well before the dam's destruction, including the Kherson liberation operation in August–November 2022, so the original "pre-period" wasn't a genuine pre-conflict baseline at all — it was a period of different, already-ongoing conflict intensity. That's a scope problem, since the project is trying to isolate the dam's specific effect, not the war's cumulative effect.

So I narrowed the pre-period to January–May 2023 only, immediately before the dam's destruction, and re-ran it — a larger, still highly significant effect (did_term = −0.1384, p=0.002, R²=0.768), which is what you'd expect if narrowing correctly isolated the marginal event-specific damage. But a placebo test inside that narrowed window (fake date: March 2023) came back with a coefficient of nearly identical magnitude to the real result (−0.1382), just not statistically significant (p=0.169) — a meaningfully weaker form of validation than a placebo near zero, especially with only 10 observations in that window giving it low power. I couldn't cleanly resolve whether that reflected a genuine null or an underpowered test of a real, possibly confounded effect, so I reported it as an honest, unresolved limitation rather than either confirmatory or disqualifying.

Both results stayed in the final reporting rather than picking the more favorable one: the broader-baseline result (−0.0703, p=0.007) as the primary finding, since its placebo was unambiguously clean, and the narrowed-baseline result (−0.1384, p=0.002) as a sensitivity analysis with its own placebo-validation limitation disclosed rather than hidden. The whole sequence follows the same discipline I'd already leaned on in GPIE and DOUBLE JEOPARDY — a favorable-looking result treated as a hypothesis needing more stress-testing, technical failures diagnosed to their actual cause rather than routed around, and an ambiguous validation reported as ambiguous.

---

## Entry 8

Tried to quantify reservoir and floodplain water-loss in the same Difference-in-Differences format as the NDVI result, and it wasn't feasible — there's no comparable control-zone equivalent for a river-mouth reservoir collapse, since Tulcea's Danube Delta has no equivalent large upstream reservoir infrastructure. Rather than force a comparison that doesn't exist, I reported reservoir and floodplain water changes descriptively instead, using the UNOSAT flood-progression data already validated: pre-breach reservoir extent of roughly 2,155 km² and 18.2 km³ of water (documented), against downstream floodplain inundation peaking at 464.18 km² on 9 June before receding to 21.17 km² by 21 June — presented as supporting descriptive evidence of physical scale alongside the statistically validated NDVI result, not as an independently causally-tested finding of its own.

---

## Entry 9

With the causal model, event study, and flood-extent analysis done, the remaining work turned the statistics into actual outputs. Built a set of static maps and plots from the validated data — the study-area overview, before/after true-colour imagery of the reservoir, the DiD regression result, the monthly NDVI comparison, the verified flood hydrograph, and the quarterly event-study chart — matching every figure the research paper references, plus an interactive QGIS2Web flood-extent map built from the UNOSAT polygons.

Then built the actual dashboard: a multi-page Streamlit app (overview plus eight sub-pages — Study Design, Flood Analysis, Vegetation Impact, Statistical Validation, Explore Trends, Satellite Evidence, Interactive Maps, and Methodology & Data), presenting every finding — including the narrowed-baseline limitation, disclosed honestly rather than smoothed over — in an interactive, non-technical format. Deployed it to Streamlit Community Cloud and linked it from GitHub. Finished by writing up the Project Report, Research Paper, and this development log, and a README summarizing the project for a GitHub audience, then published the repository.

---

## Entry 10

With the project functionally complete, I went back through it once more against the kind of scrutiny a scholarship review panel would actually apply — was the standard-error specification right for a two-unit comparative time series, did the reference list meet academic standards, were the reported figures consistent across every document, did the repo's security hygiene hold up to public scrutiny.

The standard-error question turned out to matter. The original models used classical OLS standard errors throughout, which isn't right for this design: with only two geographic units observed over time, cluster-robust standard errors — the correction I'd used in prior multi-country panel work — are degenerate, since cluster-robust inference needs many independent clusters, not two. Newey-West HAC (heteroskedasticity- and autocorrelation-consistent) standard errors are the appropriate fix for a small number of long time series, so I applied that across all five causal-inference scripts. The main finding and the narrowed-baseline estimate both survived the correction — the narrowed-baseline estimate actually got *more* significant, not less. The one real change: the narrowed-baseline placebo test, previously sitting in an "ambiguous" middle ground under classical standard errors, became statistically significant under HAC — meaning it fails outright as a validation check rather than staying unresolved. I reported that plainly as a validation failure throughout the paper and the dashboard rather than keeping the softer framing. It doesn't change the project's primary conclusion, since the broader-baseline result's own placebo stays clean under the same correction.

Fixed a handful of other things in the same pass: corrected figure numbering in the research paper (a stray decimal sub-figure and a missing number, now a clean 1–6 sequence); rewrote references with complete, verifiable citation details, replacing incomplete entries and a placeholder journal name; added confidence intervals alongside every reported coefficient and p-value, plus a new Robustness Checks subsection covering the classical-versus-HAC comparison in full; audited `requirements.txt` against actual imports across every script and fixed it (two unused packages dropped, two missing ones added); fixed the dashboard's PDF download buttons, which used working-directory-relative paths that break on Streamlit Cloud, to resolve relative to the script's own location instead, with a graceful fallback if a file's genuinely missing. Also found a real security issue: the `.env` file with live API credentials had been committed to the public repo, because `.gitignore` never excluded it. Replaced the committed file with placeholders, fixed `.gitignore` going forward, and I'm rotating the live credentials at the provider separately from this documentation pass. Added a LICENSE (CC BY 4.0) and CITATION.cff ahead of the project's Zenodo archival, and updated every page and document referencing the project's statistics to keep the HAC-corrected figures consistent everywhere.

---

## Entry 11

Went back through every quantitative claim in the research paper and independently recomputed it from the raw data directly, rather than trusting numbers that had accumulated across a lot of separate sessions. Re-derived the pre-treatment covariate-balance test from scratch (Kherson n=17, mean=0.222, SD=0.074; Tulcea n=17, mean=0.203, SD=0.110; t-test p=0.553), re-read the raw UNOSAT flood-extent shapefiles and reprojected them to EPSG:6933 for area calculation (122.50 km² / 464.18 km² / 21.17 km² — all matched), and re-ran all five causal-inference scripts directly against the raw NDVI files.

Everything matched exactly. The main DiD model reproduced did_term = −0.0703 (HAC p=0.022, classical p=0.0070), the broad-baseline placebo reproduced 0.0148 (HAC p=0.6124), the narrowed-baseline model reproduced −0.1384 (HAC p=0.000129), the narrowed placebo reproduced −0.1382 (HAC p=0.0011) — including the specific "classical non-significant, HAC significant" validation-failure pattern that's the whole point of that test — and all four cited event-study quarters matched to the reported precision, including the disclosed pre-treatment anomaly. The one figure I couldn't independently re-derive was the "~10,800 km² downstream analysis corridor" used for the ~4.3% peak-flood-coverage statistic — there's no dedicated script producing it, it looks like a manually-estimated extent, and the paper already hedges that framing explicitly, so I noted it rather than treated it as a discrepancy. Spot-checked three of the paper's six references against independent sources and confirmed them real and accurately cited; the remaining three weren't individually re-verified this round. This was the cleanest verification pass across the portfolio so far — every independently re-derivable statistic matched exactly, with no fixes needed anywhere.

---

## Entry 12

The paper's own limitations section already named the headline weakness plainly: this whole design rests on a single treatment zone against a single control zone, which is exactly why cluster-robust standard errors were never an option and Newey-West HAC had to carry the full burden of correcting for serial correlation. The obvious fix — named in my own Future Work list — was either a full Synthetic Control Method or a more modest control-zone sensitivity check against two or three alternatives. I went with the sensitivity check first, since it's the more direct test of whether −0.0703 is really about Kherson or just an artifact of Tulcea being the one control I happened to pick.

Stayed inside the same selection logic that picked Tulcea originally rather than reaching for a geographically distant, harder-to-defend control: Galați, Brăila, and Constanța are the three Romanian counties bordering Tulcea along the same Danube/Black Sea corridor — all non-combatant, all a broadly similar floodplain/deltaic/coastal mix, running 9,185–13,749 km² against Tulcea's 16,968 km², the same rough order of magnitude. Pulled their boundaries straight out of the GADM file I already had on disk from the original Tulcea extraction rather than downloading anything new, and derived bounding boxes from those geometries' bounds the same way the original Kherson/Tulcea boxes were built. Set up `download_ndvi_control_zones.py` to mirror the original NDVI acquisition exactly — same evalscript, same window, same monthly aggregation — pointed at the three new boxes, along with three downstream scripts ready to consume the new data once acquired: a multi-control DiD model reporting both cluster-robust (by zone) and HAC estimates side by side plus a per-zone breakdown, a multi-control placebo test, and a multi-control event study.

One honest note going in: five clusters (one treatment, four control) is a real improvement over two — the minimum for cluster-robust inference to even be defined — but still well short of the 30–40+ clusters the underlying asymptotic theory actually assumes. I planned to report the cluster-robust result as a genuine step forward, not a claim that this now matches a properly powered multi-unit panel, and to keep HAC reported alongside it for exactly that reason.

---

## Entry 13

Ran `download_ndvi_control_zones.py` and all three new zones came back clean — the same 35 monthly points as Kherson and Tulcea, no failed requests, plausible NDVI ranges (Galați and Brăila a bit greener on average than Tulcea, Constanța in between — three different landscapes, not a red flag).

The pooled result held: across all four controls, did_term = −0.0600 (HAC p=0.029, cluster-robust p=0.002) — a bit smaller than the original −0.0703, same direction, nowhere near zero. The placebo test on the same panel came back clean too (+0.0222, wrong sign, p=0.216). The per-zone breakdown turned out to be the more interesting result, and I didn't fold it quietly into the pooled number: Tulcea, Galați, and Brăila each reproduce a significant effect on their own (p=0.022, 0.026, and <0.001 respectively), but Constanța doesn't (−0.0064, p=0.808). Looking at what's different about it — it's the most purely Black Sea coastal, most urbanized of the four, less of the Danube floodplain/deltaic character the other three share more directly with the treatment zone. That's a plausible explanation, not a confirmed one — I don't have a land-cover breakdown to actually test it, so it went into Future Work rather than the results section as settled fact.

The cluster-robust standard errors came with their own honest asterisk. Even on the pooled DiD model, statsmodels flagged the cluster covariance matrix as rank-deficient — five clusters isn't enough for the full asymptotic theory to hold, though `did_term`'s own standard error still came out sane. It got worse on the event study: with roughly 24 parameters and only 5 clusters, several coefficients came back with standard errors on the order of 1e-16 — not real precision, a genuine computational breakdown from too many parameters relative to too few clusters. I caught that by actually reading the printed output rather than trusting the p-values at face value, and reported the HAC version of that model instead, showing the cluster-robust numbers only to document why they weren't used. The event study itself told a different story than the original two-zone version: under HAC on the four-control panel, the exact treatment quarter was no longer significant (p=0.972, versus p=0.005 originally), while the quarter-and-a-year-later effect still was (p=0.011). I didn't try to force that into one clean story — the pooled, non-quarterly result is robust to widening the control side, while the fine-grained quarterly timing gets genuinely noisier once averaged across four ecologically different controls. Both statements went into the paper as-is.

Wrote all of it up: a new figure comparing the control panel, a new section in the research paper covering the whole expansion, updated limitations (the "single treatment-control pair" weakness is now a "5-cluster, not 30–40-cluster" weakness) and Future Work (control-zone sensitivity is done, replaced with "explain why Constanța differs" and "get to a genuinely large cluster count"), and matching updates to the Project Report and README. Why Constanța doesn't reproduce the effect is a real open question, not a solved one — a land-cover comparison is the way to actually test the coastal-versus-deltaic explanation rather than just assert it. Getting cluster-robust inference to a properly trustworthy cluster count would mean going beyond Romania entirely — Bulgarian or Moldovan counterparts along the same basin — which is a considerably bigger acquisition and boundary-matching effort than this pass, so it stays on the list rather than getting attempted here.

---

## Entry 14

Wanted the flood-extent map built the same way GHOST_INFRASTRUCTURE's and DOUBLE_JEOPARDY's interactive maps now are — directly in Python with folium instead of round-tripping through a QGIS project file and the QGIS2Web plugin export. `build_kherson_flood_map.py` reads the same three verified UNOSAT flood-extent shapefiles the static-map script already uses, same colors for each date, same Kherson Oblast boundary outline.

Each date's shapefile is a single MultiPolygon with a lot of baked-in detail — 20K to 133K vertices depending on the date — so I simplified the geometry (0.0002°, well under anything visible at this zoom) before rendering. Had to drop the shapefiles' attribute columns before handing geometry to folium too — one of them comes in as a raw pandas Timestamp that folium's GeoJson serializer can't encode, and none of those columns were going in the popup anyway, since date and area get written directly into the popup HTML from the filename and area field. Output landed at 2.6MB, well within what GitHub Pages and the dashboard's iframe embed already handle fine for the other maps.

Feature counts and area figures matched the existing static map exactly — confirms this is the same verified UNOSAT data, just rendered differently. Updated the dashboard's Interactive Maps page, the README's tech stack and repo-structure notes, and the Project Report's deliverables line to say Python (folium) instead of QGIS. The old QGIS2Web export is left in place as unused legacy content, since I don't have a way to delete files on this machine directly — it stays until I remove it by hand.
