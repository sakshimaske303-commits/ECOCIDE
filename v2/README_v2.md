# ECOCIDE v2 — how to download the data (run on your own computer)

Everything here runs from the ECOCIDE folder in PowerShell. Replace `python` with your full path if needed:
`& C:\Users\shobh\AppData\Local\Programs\Python\Python312\python.exe`

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
3. Your profile page shows an API key. Create the file `C:\Users\shobh\.cdsapirc` (no extension) containing two lines:
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
```

## Step 5 — check and send

```powershell
python v2/05_check_and_sample.py
```

This writes `data/v2/CHECK_REPORT.json` and `data/v2/sample_kherson.nc`. Tell Claude when it is done; those two small files are all that is needed for the next round. The large files stay on your computer.

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

## Disk and time

About 4–6 GB on disk. Steps 1 and 2 can run while you do other work; the laptop must stay awake and online.
