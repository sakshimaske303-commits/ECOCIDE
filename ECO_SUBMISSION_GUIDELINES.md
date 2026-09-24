> **Status note (24 Sept 2026):** Sections I–K describe the repository as of 11 Sept 2026 and are out of date — `ECO_Project_Report.md` no longer exists, all figure scripts now read `outputs/model_results.json`, and the headline numbers have changed (see `ECO_RESULTS_RECONCILIATION.md`). Sections A–H (journal rules) remain the reference.

# ECOCIDE — Environment and Security (SAGE) Submission Guidelines
### Verified reference document — combines the journal's own stated rules with an actual audit of this repository

Compiled 2026-09-11. Every journal-rule claim below was checked directly against the guidelines text Sakshi pasted from SAGE (`journals.sagepub.com/author-instructions/eas`), not taken on trust from any AI summary. Every repo-state claim below was checked directly with `grep` against the actual files in this project, not assumed. Where a ChatGPT review disagreed with what a direct check found, that is flagged explicitly in Section F.

---

## A. Scope fit — CONFIRMED, no doubt

The journal's own listed topics include "Environmental impacts of armed conflict" verbatim. ECOCIDE (Kakhovka Dam destruction, satellite-based vegetation attribution, armed conflict) sits squarely inside this. The journal explicitly accepts quantitative, qualitative, and mixed-method designs, and explicitly welcomes "innovative methods and data sources." Scope is not a real risk for this submission — being read as "just a remote-sensing paper" rather than an environment-security contribution is the actual risk, addressed in Section G.

## B. Article type and hard limits — verified on the SAGE site directly (2026-09-11)

Applies to **Research Article**, the correct type for this paper:

- Body text: **max 8,000 words** — text only. References, tables and figures are excluded from this count, **but table/figure titles and legends are included** in it.
- Title: **max 30 words**.
- Abstract: **max 200 words**, unstructured (one paragraph — purpose, major findings, conclusions; no sub-headings). (A ChatGPT review of this rule said "100-200 words" — the site's Research Article spec itself only states an upper bound of 200; treat 200 as the number that matters.)
- Minimum **5 keywords**.
- **No limit** on the number of references.
- Clinical-trial registration requirements do not apply — this study has no clinical trial.

## C. Two separate files are required, not one

1. **Main manuscript** — sent to peer reviewers. Must be **fully anonymized**: no author name anywhere in the text, headers, footers, or the file name itself.
2. **Title Page** — never sent to reviewers. Must contain: full title; full author list with affiliations; corresponding-author contact details (name, institutional address, phone, email); an Acknowledgments section; an Author Contributions section; and a **"Statements and Declarations"** section containing these exact six sub-headings, every one of them present even when the answer is "Not applicable":
   - Ethical considerations
   - Consent to participate
   - Consent for publication
   - Declaration of conflicting interest
   - Funding statement
   - Data availability

For a satellite/remote-sensing study with no human participants, Ethical considerations / Consent to participate / Consent for publication will almost certainly all read "Not applicable" — but the heading must still appear, stated explicitly, not omitted.

## D. Reporting guideline, ethics, funding, conflict-of-interest, data availability

- The journal requires identifying (via the EQUATOR Network wizard) whichever reporting guideline fits the study type, and uploading its checklist at submission. This study is not a clinical or biomedical design, so it may turn out no EQUATOR checklist applies cleanly — that determination itself needs to be made and documented before submission, not skipped.
- Conflict of interest: if none, the journal supplies the exact required wording: *"The author(s) declared no potential conflicts of interest with respect to the research, authorship, and/or publication of this article."*
- Funding statement is mandatory even with no funding, e.g.: *"This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors."*
- Data availability statement is required. This project's advantage: the GitHub repo (`github.com/sakshimaske303-commits/ECOCIDE`) and the Zenodo DOI already give a real answer — state what's public (code, NDVI outputs), what's derived (regression outputs), and where raw Sentinel-2/UNOSAT data originates.

## E. Authorship and AI disclosure

- AI chatbots (ChatGPT, Claude, etc.) **cannot be listed as authors**, per the journal's explicit policy.
- If AI tools were used for writing/editing/analysis assistance, this **must be disclosed in the Acknowledgements section and in the cover letter**. This project has used both ChatGPT and Claude at various points — this needs an honest disclosure line, not silence.
- All listed authors must meet the ICMJE criteria (contribution + drafting/revision + final approval + accountability). For a sole-author paper this is simpler, but the Author Contributions section must still exist and state the single author's role.

## F. References, figures, originality

- Reference style: **APA**. Every in-text citation must have a matching reference-list entry with identical spelling and year, and vice versa — this needs a manual pass, not an assumption.
- Figures: 300dpi, numbered consecutively in the order they appear in the text (this determines publication order).
- At submission you confirm: original work, rights to the work, first publication, not under simultaneous consideration elsewhere, and permissions secured for any non-own copyrighted material (maps/figures/quotations). ECOCIDE's own generated plots and satellite-derived maps are the cleanest case here since they're self-produced.

## G. Preprint policy

The journal **will** consider manuscripts already posted as a preprint (this project's EarthArXiv PDF qualifies). Requirements: supply the preprint DOI at submission, inform the journal's editorial office of it, and **do not update the preprint while the manuscript is under review**. If accepted, the published version must be linked back from the preprint.

## H. Submission mechanics

- Corresponding/submitting author needs an **ORCID ID**.
- A **cover letter** is not mandatory but is recommended, and should state the environment-security contribution directly (e.g., "this study examines how satellite-derived ecological evidence can be combined with counterfactual inference to assess conflict-associated environmental change under severe observational constraints") — not just "I used Sentinel-2 and NDVI."
- Peer review is **double-anonymized**: neither reviewer nor author identity is revealed to the other during review.
- Submission goes through Sage Track (ScholarOne).

---

## I. LIVE REPO AUDIT — what is actually stale right now (checked by direct `grep`, 2026-09-11)

This is the part no AI review can get right without actually opening the files. Below is what a real search across every `.md` and `.py` file in this repository found, for the specific pre-correction numbers (`−0.0703`, `p=0.022`, `−0.0600`, `p=0.029`, `+0.0148`, `p=0.612`) and the removed `10,800 km² / 4.3%` figure.

### ✅ Confirmed correctly updated (old numbers only appear framed as history, e.g. "originally-reported")
- `ECO_Research_Paper.md`
- `ECO_Executive_Summary.md`
- `ECO_RESULTS_RECONCILIATION.md` (by design — this file's whole purpose is old-vs-new)
- `README.md`
- `CITATION.cff`
- `dashboard/app.py`
- `dashboard/pages/3_Vegetation_Impact.py`
- `dashboard/pages/4_Statistical_Validation.py`
- `dashboard/pages/8_Methodology_Data.py`
- `ECO_Development_Log.md` (by design — it's a diary of the actual research journey, old numbers there are correctly the numbers she had *at that point in time*)

### 🔴 Confirmed still stale — presents pre-correction numbers as current fact, no correction framing at all
- **`ECO_Project_Report.md`** (lines 44, 54) — states *"found a statistically significant NDVI decline... p = 0.022"* and the four-county *"−0.0600 (HAC p = 0.029)"* as plain current findings. This file was never touched by this session's correction pass. It needs the same full rewrite already done to the Research Paper and Executive Summary.
- **`dashboard/pages/1_Theoretical_Foundations.py`** (line 93) — states *"project's causally-validated **NDVI decline (−0.0703, p = 0.022)**"* with zero mention of the correction. This dashboard page was missed entirely during the correction pass (only pages 3, 4, and 8 were updated). This is a live, reader-facing contradiction against every other page of the same dashboard.

### 🟠 Scripts that hardcode old numbers for plot/map generation — check before regenerating any figure for submission
- **`build_interactive_plots.py`** (lines 106, 110, 144, 146) — hardcodes `-0.0703`, `-0.0600`, `0.0148` and their old CIs/p-values directly as plot data, not computed from the corrected data files.
- **`map7_control_zone_expansion.py`** (lines 16, 24) — same pattern, hardcodes `-0.0703` and `-0.0600` for a map figure.
  Neither script recomputes from `data/ndvi` (now the promoted, corrected data) — they have the old numbers typed in directly. If either script's output is one of the figures actually going into the manuscript or supplementary material, it will visually contradict the corrected text (`−0.0747` / `−0.0661`) unless these scripts are updated first.

### ✅ Not actually a problem — correcting a stale ChatGPT claim
The **10,800 km² / 4.3% flooded-corridor figure** ChatGPT's review flagged as something to "remove before submission" **was already removed** from `ECO_Research_Paper.md` §4.1 earlier this session — the paper text explicitly says so ("*That number has been removed here: this paper does not report a quantitative result the author cannot currently regenerate from code*"). `dashboard/pages/1_Study_Design.py` still mentions the 10,800 km² corridor, but only as a plain geographic description of the treatment zone, already self-labeled "my own estimated corridor, not a published UNOSAT figure" — it is not re-presenting the removed 4.3% statistic as a finding, so no fix is required there. ChatGPT's review did not have visibility into this session's edits and was working from stale information on this specific point.

### Separately known, not found by this grep but already flagged earlier this session — still pending
- Five PDF exports (`ECO_Development_Log.pdf`, `ECO_Executive_Summary.pdf`, `ECO_Research_Paper.pdf`, `ECO_Research_Paper_EarthArXiv_Submission.pdf`, `ECOCIDE_Maps_and_Plots.pdf`) were generated **before** this window's correction and are stale relative to their `.md` sources.
- The corrected repo state has not yet been pushed to GitHub `main` — the public repo a reviewer would actually open is currently out of sync with the local corrected files.

---

## J. Net verdict on the ChatGPT review pasted this session

Cross-checked point-by-point against the real SAGE guidelines text and the real repo state:

- **Accurate and worth keeping**: everything in Sections A–H above (scope fit, word/abstract/title limits, anonymization + Title Page structure, Statements and Declarations headings, EQUATOR/ethics/funding/COI/data-availability requirements, authorship + AI-disclosure rule, APA + figure rules, preprint policy, ORCID/cover-letter/double-anonymized-review mechanics). ChatGPT's summary of the journal's own rules was substantially correct.
- **Outdated / wrong**: the "10,800 km² / 4.3% needs to be removed" instruction — already done, ChatGPT didn't know.
- **Right instinct, but not actually verified until now**: "audit the repo for old numbers." ChatGPT listed this as a to-do without checking; the actual audit above is what that check turns up, and it found two live-content files (`ECO_Project_Report.md`, `dashboard/pages/1_Theoretical_Foundations.py`) and two figure-generating scripts (`build_interactive_plots.py`, `map7_control_zone_expansion.py`) that genuinely still need fixing — a more specific and more useful result than the generic instruction to "search for these numbers."

---

## K. Priority order for what's left

1. Rewrite `ECO_Project_Report.md` with corrected numbers (same treatment as the Research Paper / Executive Summary).
2. Fix `dashboard/pages/1_Theoretical_Foundations.py` line 93 — add correction framing or update to `−0.0661`/`-0.0747` with historical context, matching the other three dashboard pages.
3. Check whether `build_interactive_plots.py` and `map7_control_zone_expansion.py` outputs are actually used anywhere in the current manuscript/dashboard; if yes, update the hardcoded numbers and regenerate.
4. Regenerate the five stale PDFs from the now-corrected `.md` files.
5. Push the corrected repo to GitHub so the public copy matches what's on disk.
6. Only then move into the manuscript-formatting checklist (Title Page, anonymization pass, EQUATOR checklist, ORCID, cover letter) — Sections B–H above are ready to use when that stage starts.
