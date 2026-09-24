"""Step 0 — checks that every package and data service needed by the v2
scripts is reachable from this computer. Run from the ECOCIDE folder:

    python v2/00_check_env.py
"""
import importlib
import os
import sys

import requests

PKGS = ["pystac_client", "planetary_computer", "odc.stac", "odc.geo", "rasterio",
        "rioxarray", "xarray", "netCDF4", "dask", "cdsapi", "geopandas", "pyarrow"]
SERVICES = {
    "Microsoft Planetary Computer (MODIS, WorldCover)": "https://planetarycomputer.microsoft.com/api/stac/v1/collections/modis-13Q1-061",
    "Copernicus Climate Data Store (ERA5-Land)": "https://cds.climate.copernicus.eu/api/catalogue/v1/collections/reanalysis-era5-land-monthly-means",
    "Overpass API (OpenStreetMap canals)": "https://overpass-api.de/api/status",
}

ok = True
print(f"Python {sys.version.split()[0]}")
for p in PKGS:
    try:
        m = importlib.import_module(p)
        print(f"  [ok]   {p} {getattr(m, '__version__', '')}")
    except Exception as e:  # noqa: BLE001
        ok = False
        print(f"  [MISSING] {p}: {e}")
for name, url in SERVICES.items():
    try:
        r = requests.get(url, timeout=30)
        print(f"  [{'ok' if r.status_code < 400 else 'HTTP ' + str(r.status_code)}] {name}")
        ok &= r.status_code < 400
    except Exception as e:  # noqa: BLE001
        ok = False
        print(f"  [FAILED] {name}: {e}")
cds = os.path.join(os.path.expanduser("~"), ".cdsapirc")
print(f"  [{'ok' if os.path.exists(cds) else 'MISSING'}] CDS key file {cds}"
      + ("" if os.path.exists(cds) else "  -> see v2/README_v2.md, step 3"))
print("\nAll good." if ok else "\nFix the items marked MISSING/FAILED before continuing.")
