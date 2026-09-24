"""Step 5 — checks everything downloaded in steps 1–4 and writes two SMALL
files for Claude to inspect (they are safe to share; no credentials):

    data/v2/CHECK_REPORT.json   — what was downloaded, sizes, value ranges, gaps
    data/v2/sample_kherson.nc   — two MODIS composites + land cover, lower-Dnipro window only

    python v2/05_check_and_sample.py
"""
import glob
import json
import os
import sys

import numpy as np
import xarray as xr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid  # noqa: E402

D = "data/v2"
WINDOW = (32.2, 46.35, 33.8, 47.4)  # lower Dnipro + southern tip of the reservoir (lon/lat)


def window_xy():
    from odc.geo.geom import BoundingBox
    return BoundingBox(*WINDOW, crs="EPSG:4326").to_crs(grid.CRS)


def main():
    rep = {"grid": grid.describe()}
    files = sorted(glob.glob(f"{D}/modis/mod13q1_*.nc"))
    dates = [os.path.basename(f)[8:18] for f in files]
    rep["modis"] = {"n_files": len(files), "first": dates[:1], "last": dates[-1:],
                    "total_MB": round(sum(os.path.getsize(f) for f in files) / 1e6),
                    "per_year": {y: sum(d.startswith(str(y)) for d in dates) for y in range(2016, 2025)}}
    if os.path.exists(f"{D}/modis_assets.json"):
        expected = json.load(open(f"{D}/modis_assets.json"))["dates"]
        rep["modis"]["missing_dates"] = sorted(set(expected) - set(dates))
    bb = window_xy()
    samples = []
    if files:
        for f in [files[len(files) // 2], files[-1]]:
            ds = xr.open_dataset(f)
            rep["modis"].setdefault("examples", {})[os.path.basename(f)] = {
                "vars": {v: str(ds[v].dtype) for v in ds.data_vars},
                "ndvi_valid_frac": float(ds.ndvi.notnull().mean()),
                "ndvi_min_max": [float(ds.ndvi.min()), float(ds.ndvi.max())],
                "reliability_counts": {str(int(k)): int(c) for k, c in zip(*np.unique(ds.reliability.fillna(-9).values, return_counts=True))},
            }
            samples.append(ds.sel(x=slice(bb.left, bb.right), y=slice(bb.top, bb.bottom)))
    wc_path = f"{D}/worldcover_2021_fractions.nc"
    if os.path.exists(wc_path):
        wc = xr.open_dataset(wc_path)
        rep["worldcover"] = {"MB": round(os.path.getsize(wc_path) / 1e6), "vars": list(wc.data_vars),
                             "mean_valid_pct": float(wc.valid_pct.mean()),
                             "crop_pct_mean": float(wc.frac_crop.where(wc.frac_crop < 255).mean())}
        wcs = wc.sel(x=slice(bb.left, bb.right), y=slice(bb.top, bb.bottom))
    else:
        wcs = None
    era = glob.glob(f"{D}/era5land_monthly_2015_2024*")
    if era:
        try:
            e = xr.open_dataset([p for p in era if p.endswith(".nc")][0])
            rep["era5land"] = {"vars": list(e.data_vars), "dims": {k: int(v) for k, v in e.sizes.items()},
                               "coords": list(e.coords)}
        except Exception as ex:  # noqa: BLE001
            rep["era5land"] = {"files": era, "error": str(ex)}
    if os.path.exists(f"{D}/osm_canals.geojson"):
        g = json.load(open(f"{D}/osm_canals.geojson", encoding="utf-8"))
        names = {}
        for ft in g["features"]:
            nm = ft["properties"].get("name:uk") or ft["properties"].get("name")
            if nm:
                names[nm] = names.get(nm, 0) + 1
        rep["osm_canals"] = {"segments": len(g["features"]),
                             "top_names": sorted(names.items(), key=lambda kv: -kv[1])[:40]}
    with open(f"{D}/CHECK_REPORT.json", "w", encoding="utf-8") as fh:
        json.dump(rep, fh, indent=1, ensure_ascii=False, default=str)
    if samples:
        s = xr.concat(samples, dim="time")
        if wcs is not None:
            s = s.merge(wcs)
        s.to_netcdf(f"{D}/sample_kherson.nc", encoding={v: {"zlib": True, "complevel": 4} for v in s.data_vars})
    print(json.dumps(rep, indent=1, ensure_ascii=False, default=str)[:4000])
    print(f"\nWrote {D}/CHECK_REPORT.json and {D}/sample_kherson.nc")


if __name__ == "__main__":
    main()
