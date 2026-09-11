# Phase 2 — GADM Polygon Extraction + Pixel-Level Cloud Masking

## Why this has to run on your machine, not in the assistant's sandbox

This phase needs two things the assistant's cloud sandbox does not have:
your Sentinel Hub / Copernicus Data Space credentials (`.env` — `SH_CLIENT_ID`,
`SH_CLIENT_SECRET`), and `geopandas`/`shapely` (not installable in the
assistant's sandbox due to a network-restricted package registry there —
but you already have both, since your own `extract_boundaries.py` and
`water_loss_summary.py` already import `geopandas`). The assistant has
never read your `.env` file and does not need to; only the resulting NDVI
JSON output (not the credentials) needs to come back.

## What the 3 new scripts do

1. **`export_zone_geometries.py`** — reads the 5 boundary files you already
   have saved (`data/boundaries/kherson_oblast.gpkg`, `tulcea_county.gpkg`,
   `galati_county.gpkg`, `constanta_county.gpkg`, `braila_county.gpkg`),
   simplifies each polygon just enough that Sentinel Hub's API will accept
   it as a single request, and saves each as
   `data/boundaries/geometries/{zone}_geometry.json`.

2. **`download_ndvi_polygon.py`** — the actual fix. Same NDVI formula,
   same Sentinel-2 L2A source, same monthly aggregation, same
   Jan 2022–Nov 2024 window as the original `download_ndvi.py` /
   `download_ndvi_control_zones.py` — but now: (a) queries the real GADM
   polygon geometry for each zone instead of its bounding box, and (b) adds
   pixel-level cloud/cloud-shadow/cirrus/snow masking using the Sentinel-2
   Scene Classification (SCL) band, instead of relying only on the
   scene-level `maxCloudCoverage<=40` filter. Output goes to a **new**
   folder, `data/ndvi_v2/` — it does **not** touch or overwrite
   `data/ndvi/`, so the original bbox-based data stays intact as the
   Phase-1 baseline.

3. **`compare_ndvi_versions.py`** — once step 2 finishes, run this to see
   old vs. new mean NDVI and valid-pixel-fraction side by side for every
   zone/month, with any month whose mean shifted by more than 0.02 NDVI
   flagged for your attention.

## Steps to run

```bash
# from the ECOCIDE project root, in the same environment you already use
# to run download_ndvi.py etc.

python export_zone_geometries.py
#   -> prints vertex counts before/after simplification for all 5 zones.
#   If any zone's polygon still looks huge, that's fine for now — the next
#   step will tell you definitively whether Sentinel Hub accepts it.

python download_ndvi_polygon.py
#   -> calls Sentinel Hub once per zone. Takes a few minutes.
#   If a zone FAILS with a 400 or a timeout mentioning geometry complexity:
#     1. open export_zone_geometries.py
#     2. raise ONLY that zone's value in SIMPLIFY_TOLERANCE_DEG
#        (e.g. 0.002 -> 0.005)
#     3. re-run export_zone_geometries.py
#     4. re-run download_ndvi_polygon.py (it's fine to re-run for all 5;
#        it just re-downloads and overwrites data/ndvi_v2/*.json)

python compare_ndvi_versions.py
#   -> prints a month-by-month old-vs-new comparison for all 5 zones.
```

## What to send back

Once `data/ndvi_v2/` has all 5 files (`kherson_ndvi_monthly.json`,
`tulcea_ndvi_monthly.json`, `galati_ndvi_monthly.json`,
`constanta_ndvi_monthly.json`, `braila_ndvi_monthly.json`), tell the
assistant — it will pick those files up the same way it has been reading
files from your D: drive all session (no credentials involved, just the
resulting NDVI numbers), and will re-run the entire existing analysis
pipeline (primary DiD, both placebos, event study, four-county panel,
placebo-in-space, multiple-testing correction, control-only spillover
check, lag-length and functional-form robustness, low-coverage-month
check) against the new data, using the same manual HAC/OLS engine already
validated against your original `did_model.py` results this session.

## Do NOT do this yet

Do not rename/move `data/ndvi_v2` to `data/ndvi` (i.e. do not promote the
new data to primary) until the assistant has run the full comparison and
told you whether the headline result survives. If it does, the paper's
numbers get updated in place, using `ECO_RESULTS_RECONCILIATION.md` to
make sure every occurrence in every file is caught. If the new pixel-clean
data moves the result materially, that becomes a real finding to report
honestly — not something to quietly revert from.
