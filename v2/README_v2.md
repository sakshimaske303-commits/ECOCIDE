# ECOCIDE v2 — how to download the data (run on your own computer)

Everything here runs from the ECOCIDE folder (PowerShell or any other shell), with the Python environment in which the requirements are installed.

## Step A — freeze the analysis plan FIRST (pre-registration)

Before downloading anything, commit and push the plan so its timestamp is public:

```powershell
git add ANALYSIS_PLAN_v2.md v2/
git commit -m "Pre-register v2 analysis plan (before data download)"
git push origin main
```

Do not open or look at v2 data before this commit exists.

## Step B — install packages

```powershell
python -m pip install -r v2/requirements_v2.txt
python v2/00_check_env.py
```

Everything should say `[ok]` except the CDS key (Step 3 below).

## Step 1 — MODIS NDVI (largest download: ~207 files, a few GB, 1–3 hours)

```powershell
python v2/01_download_modis.py --test     # one file only, ~1 minute; check it works
python v2/01_download_modis.py            # everything; re-run if it stops, it resumes
```

## Step 2 — land cover

```powershell
python v2/02_download_worldcover.py       # ~20–60 minutes
```

## Step 3 — weather (needs a free Copernicus account, one time)

1. Register at https://cds.climate.copernicus.eu and log in.
2. Open the dataset page "ERA5-Land monthly averaged data from 1950 to present" → *Download* tab → scroll down → accept the licence.
3. Your profile page shows an API key. Create the file `.cdsapirc` (no extension) in your home folder (`%USERPROFILE%` on Windows, `~` on Linux/macOS) containing two lines:
   ```
   url: https://cds.climate.copernicus.eu/api
   key: PASTE-YOUR-KEY-HERE
   ```
4. Run:
   ```powershell
   python v2/03_download_era5land.py      # the request waits in a queue; 5–60 minutes
   ```

## Step 4 — canals

```powershell
python v2/04_download_osm_canals.py
python download_gadm.py                   # oblast and raion boundaries (GADM v4.1; not stored in the repository)
```

## Step 5 — check the downloads

```powershell
python v2/05b_check_and_sample.py
```

This writes `data/v2/CHECK_REPORT.json` (files, sizes, value ranges, and composites missing from the catalogue) and a small sample, `data/v2/sample_kherson.nc`. Inspect the report to confirm the downloads are complete. (The first version of this script, `05_check_and_sample.py`, is in git history up to commit 47093cc.)

## Step 6 — yearly summaries

```powershell
python v2/06_annual_composites.py         # ~5 minutes; writes data/v2/annual/annual_2016.nc … 2024.nc
```

## Step 7 — the analysis (Study 2)

```powershell
python v2/analysis/run_all.py             # ~20 minutes, needs ~6 GB free RAM
```

| Script | What it does | Plan section |
|---|---|---|
| `a1_layers.py` | pixel universe, flood fraction, reservoir bed, Dnipro channel and banks, Kakhovka canal network, zones K/O | §3–§4 |
| `a2_panel.py` | pixel sets and yearly outcome panels for H1 and H2, ERA5-Land covariates | §5 |
| `a3_h1.py` | H1 matching, balance, main estimate, event study, pre-trend test, Rambachan–Roth, robustness 1–9, secondary outcomes, exploratory checks | §4.1, §6, §8 |
| `a4_h2.py` | H2 triple difference, event study, robustness, secondary outcomes, placebo zones | §4.3, §6, §8 |
| `a5_h1_placebo.py` | 141 placebo floodplain segments (Southern Buh, lower Dniester, Dnipro above Zaporizhzhia) → randomization p for H1 | §4.4 |
| `a6_h3_h4.py` | H3 reservoir-bed vegetation, H4 decomposition of the Kherson change | §2, §9 |
| `a7_summary.py` | Holm correction and the pre-registered decision rules → `outputs/v2/study2_summary.json` | §6–§7 |
| `a8_figures.py` | six figures → `outputs/v2/figures/` | — |
| `v2lib.py` | shared engine: exact multi-way fixed-effects projection, cluster-robust SEs, wild cluster bootstrap, Conley SEs, Holm, Rambachan–Roth | — |

Every departure from the plan and every implementation choice is in `v2/DEVIATIONS.md`.

## Registered Revision 1 (`ANALYSIS_PLAN_v2_ADDENDUM_1.md`)

Commit and push the addendum BEFORE any of the downloads below:

```powershell
git add ANALYSIS_PLAN_v2_ADDENDUM_1.md v2/
git commit -m "Register Revision 1 (addendum) before extra downloads and analyses"
git push
```

Then:

```powershell
python v2/01_download_modis.py --years 2010 2011 2012 2013 2014 2015   # ~138 files, ~1 hour (R1)
python v2/06_annual_composites.py --years 2010 2011 2012 2013 2014 2015
python v2/07_io_lulc_fixed.py                                           # annual water share 2017-2023 (R5)
python v2/08_conflict_fixed.py                                          # VIINA conflict + control data (R4; fixed version)
python v2/analysis/run_revision.py                                      # all revision analyses (~15 min)
```

Results: `outputs/v2/r1_*.json`, summary `outputs/v2/r1_summary.json`, figure `outputs/v2/figures/s2_fig7_revision_event_studies.png`.

(`07_download_io_lulc.py` took the previous year's map for each year and `08_download_conflict.py` read Git LFS pointers; both were fixed in `07_io_lulc_fixed.py` and `08_conflict_fixed.py` before any revised analysis. The two first versions, and an identical copy of `04_download_osm_canals.py` (`04b_osm_canals.py`), were removed on 16 October 2026 and remain in git history up to commit 47093cc.)

## Registered Revision 2 (`ANALYSIS_PLAN_v2_ADDENDUM_2.md`)

Commit the addendum BEFORE any of the downloads below (it is not pushed until the project is finished; its SHA-256
is in `v2/DEVIATIONS.md` §6 and the analysis stops if the file has changed):

```powershell
git add ANALYSIS_PLAN_v2_ADDENDUM_2.md v2/ tests/
git commit -m "Registered Revision 2 (addendum 2) before its downloads and analyses"
```

Then:

```powershell
python tests/test_r2lib.py                      # checks the Revision 2 helpers and the addendum checksum
python v2/09_download_irrigation_maps.py        # Baber et al. (2026b) maps, ~60 MB (Zenodo)
python v2/10_download_dem.py                    # Copernicus DEM GLO-30 mean per pixel (~30-90 min)
python v2/11_download_s2_reservoir.py           # Sentinel-2 August 2024 over the reservoir bed (~1-3 h)
python v2/analysis/run_revision2.py             # all Revision 2 analyses; the placebo floodplains take longest
```

Results: `outputs/v2/r2_*.json`, summary `outputs/v2/r2_summary.json`. `r2_prepare.py` reads each irrigation map in
row bands (about 0.6 GB of memory per 30 m file).

## Exploratory checks and engine tests

```powershell
python v2/analysis/x1_review_diagnostics.py   # after run_all.py and run_revision.py -> outputs/v2/x1_review_diagnostics.json
python tests/test_v2lib.py                    # checks the estimation engine against direct calculations
```

`x1_review_diagnostics.py` is exploratory (written after all registered results were known; see `v2/DEVIATIONS.md` §5).

## Disk and time

About 4–6 GB on disk. Steps 1 and 2 can run while you do other work; the laptop must stay awake and online.
