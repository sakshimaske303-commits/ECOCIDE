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

## Disk and time

About 4–6 GB on disk. Steps 1 and 2 can run while you do other work; the laptop must stay awake and online.
