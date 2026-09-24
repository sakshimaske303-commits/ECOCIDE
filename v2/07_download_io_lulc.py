"""Step 7 (Registered Revision 1, R5) — annual water share per analysis pixel, 2017–2024,
from the Impact Observatory 10 m annual land use / land cover maps
(Microsoft Planetary Computer, collection `io-lulc-annual-v02`; no account needed).

Only the lower-Dnipro / reservoir window is processed (31.4–35.4 °E, 46.2–48.0 °N).
Output: data/v2/io_lulc/io_water_YYYY.nc with water_pct, floodveg_pct, valid_pct (0–100),
on the same 231.66 m grid (v2/grid.py). Resumable.

    python v2/07_download_io_lulc.py
"""
import json
import os
import sys
import time

import numpy as np
import planetary_computer
import pystac_client
import xarray as xr
from odc.geo.geobox import GeoBox
from odc.stac import load
from pyproj import Transformer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid  # noqa: E402

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
COL = "io-lulc-annual-v02"
OUT = "data/v2/io_lulc"
WINDOW = (31.4, 46.2, 35.4, 48.0)
# class codes documented for io-lulc-annual-v02; printed from the catalogue below to confirm
WATER, FLOODVEG, CLOUD, NODATA = 1, 4, 10, 0


def window_geobox():
    c = grid.coarse_geobox()
    tr = Transformer.from_crs(4326, grid.CRS, always_xy=True)
    w, s, e, n = WINDOW
    xs, ys = tr.transform([w, w, e, e], [s, n, s, n])
    inv = ~c.affine
    cols, rows = zip(*[inv * (x, y) for x, y in zip(xs, ys)])
    r0, r1 = max(int(min(rows)), 0), min(int(max(rows)) + 1, c.shape.y)
    c0, c1 = max(int(min(cols)), 0), min(int(max(cols)) + 1, c.shape.x)
    return c[r0:r1, c0:c1], (r0, r1, c0, c1)


def main():
    os.makedirs(OUT, exist_ok=True)
    client = pystac_client.Client.open(STAC)
    col = client.get_collection(COL)
    meta = {k: v for k, v in col.extra_fields.items() if "class" in k.lower() or "item_assets" in k.lower()}
    print("Collection class metadata (check that 1 = water, 4 = flooded vegetation, 10 = clouds):")
    print(json.dumps(meta, indent=1, default=str)[:3000])
    sub, rc = window_geobox()
    step = 400
    ny, nx = sub.shape.y, sub.shape.x
    cfg = {COL: {"assets": {"data": {"data_type": "uint8", "nodata": 0}}}}
    f = grid.FINE_FACTOR
    for year in range(2017, 2025):
        path = f"{OUT}/io_water_{year}.nc"
        if os.path.exists(path):
            print(year, "exists")
            continue
        items = list(client.search(collections=[COL], bbox=WINDOW, datetime=f"{year}-01-01/{year}-12-31").items())
        if not items:
            print(year, ": no items in the catalogue (not published)")
            continue
        parts = []
        for r in range(0, ny, step):
            row = []
            for c in range(0, nx, step):
                blk = sub[r:min(r + step, ny), c:min(c + step, nx)]
                fine = GeoBox.from_bbox(blk.boundingbox, crs=grid.CRS, resolution=grid.RES / f, tight=False)
                for attempt in range(1, 6):
                    try:
                        signed = [planetary_computer.sign(i) for i in items]
                        lc = load(signed, bands=["data"], geobox=fine, chunks={"x": 2000, "y": 2000},
                                  resampling="nearest", stac_cfg=cfg)["data"]
                        lc = (lc.isel(time=0, drop=True) if "time" in lc.dims else lc).values
                        break
                    except Exception as ex:  # noqa: BLE001
                        print(f"  {year} block {r},{c} attempt {attempt}: {ex}")
                        time.sleep(15 * attempt)
                else:
                    sys.exit("Failed; re-run the script later.")
                h, w = blk.shape.y, blk.shape.x
                lc = lc[:h * f, :w * f].reshape(h, f, w, f)
                valid = ((lc != NODATA) & (lc != CLOUD)).sum(axis=(1, 3))
                wat = (lc == WATER).sum(axis=(1, 3))
                fv = (lc == FLOODVEG).sum(axis=(1, 3))
                with np.errstate(invalid="ignore", divide="ignore"):
                    row.append(np.stack([np.where(valid > 0, 100 * wat / valid, 255),
                                         np.where(valid > 0, 100 * fv / valid, 255),
                                         100 * valid / (f * f)]))
            parts.append(np.concatenate(row, axis=2))
        arr = np.concatenate(parts, axis=1).round().astype(np.uint8)
        ds = xr.Dataset({"water_pct": (("y", "x"), arr[0]), "floodveg_pct": (("y", "x"), arr[1]),
                         "valid_pct": (("y", "x"), arr[2])},
                        coords={"y": sub.coords["y"].values, "x": sub.coords["x"].values},
                        attrs={"source": f"{COL} (Impact Observatory) via Microsoft Planetary Computer", "year": year,
                               "items": ",".join(i.id for i in items), "grid_rows_cols": list(rc),
                               "note": "percent of valid (non-cloud, non-nodata) 10 m cells; 255 = no valid cells"})
        ds.to_netcdf(path + ".part", encoding={v: {"zlib": True, "complevel": 5} for v in ds.data_vars})
        os.replace(path + ".part", path)
        print(f"{year}: {len(items)} tiles -> {path} ({os.path.getsize(path)/1e6:.1f} MB); "
              f"mean water % in window: {float(np.mean(arr[0][arr[0] < 255])):.1f}")


if __name__ == "__main__":
    main()
