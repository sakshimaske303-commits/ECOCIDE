# Archive: early exploration (not used in any result)

These files come from the first, exploratory phase of the project (see the Development Log). They are kept
for transparency. No script, figure, table or number in the papers, the dashboard or `outputs/` depends on them.

## `exploratory/` — scripts

| Script | What it did | Why it was set aside |
|---|---|---|
| `download_ndwi.py`, `download_ndwi_split.py`, `download_ndwi_weekly.py` | Sentinel-2 NDWI water index over the floodplain and reservoir | Flood extent taken from UNOSAT maps instead |
| `download_sar_water.py`, `download_sar_water_v2.py`, `download_water_fraction.py` | Sentinel-1 radar water masks and water fraction | Same reason |
| `water_loss_summary.py` | Summary of the water-index series | Same reason |
| `download_ndvi.py`, `download_ndvi_control_zones.py` | First Study 1 NDVI download over bounding boxes | Replaced by polygon extraction (`download_ndvi_polygon_v3.py`) |
| `compare_ndvi_versions.py` | Month-by-month comparison of the NDVI extraction versions | One-off check, result recorded in the Development Log |
| `create_world_files.py`, `create_world_file_after.py` | World files to place true-colour images in QGIS | Figures now built in Python |
| `fix_map_resize.py` | Resize patch for an early folium map | Map rebuilt |
| `check_romania_level1.py`, `check_zip_content.py`, `filter_boundaries.py` | Print GADM names and the contents of the UNOSAT zip | One-off inspection |

The scripts expect to be run from the repository root with the root on the Python path, for example
`PYTHONPATH=. python archive/exploratory/download_ndwi.py`. The Sentinel Hub downloads need credentials in `.env`.

## `exploratory/ndwi_sar_outputs/` — their outputs

Monthly and weekly NDWI, radar water and water-fraction series for the flood corridor, the reservoir and Tulcea,
written by the scripts above.
