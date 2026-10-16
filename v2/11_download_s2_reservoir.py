"""Step 11 (Registered Revision 2, R12) — Sentinel-2 L2A August 2024 NDVI over the former Kakhovka
reservoir bed, for the independent check of H3.

Source: Microsoft Planetary Computer, collection `sentinel-2-l2a` (no account needed). Scenes of
1–31 August 2024 with < 60 % cloud are read on the study's 23.17 m fine grid (v2/grid.py) in blocks;
clouds, shadow, cirrus, snow, saturated and no-data pixels are masked with the SCL band; each fine
pixel's August median NDVI is computed; then for each 231.66 m pixel the script stores the share of
fine pixels with a valid median and the share of those with NDVI > 0.3. Reflectances of processing
baseline 04.00 and later carry an offset of 1000, which is removed. Run ONLY after
ANALYSIS_PLAN_v2_ADDENDUM_2.md is committed. Resumable.

Output: data/v2/s2_aug2024_reservoir.nc (valid_frac, gt03_frac on the coarse grid window)

    python v2/11_download_s2_reservoir.py
"""
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
COL = "sentinel-2-l2a"
WINDOW = (33.30, 46.68, 35.25, 47.92)      # former reservoir (a1_layers: 33.40–35.15 E, 46.70–47.87 N) + margin
OUT = "data/v2/s2_aug2024_reservoir.nc"
PARTS = "data/v2/s2_parts"
SCL_OK = [2, 4, 5, 6, 7]                   # dark area, vegetation, bare, water, unclassified
F = grid.FINE_FACTOR


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


def offset_of(item):
    try:
        return 1000.0 if float(item.properties.get("s2:processing_baseline", "0")) >= 4.0 else 0.0
    except ValueError:
        return 0.0


def block(items, fine):
    signed = [planetary_computer.sign(i) for i in items]
    ds = load(signed, bands=["B04", "B08", "SCL"], geobox=fine, chunks={"x": 1000, "y": 1000},
              resampling={"SCL": "nearest", "*": "bilinear"}, groupby="solar_day")
    off = {}
    for i in items:
        off[str(np.datetime64(i.datetime.replace(tzinfo=None), "D"))] = offset_of(i)
    days = [str(np.datetime64(t, "D")) for t in ds.time.values]
    o = xr.DataArray([off.get(d, 0.0) for d in days], dims="time", coords={"time": ds.time})
    red = (ds.B04.astype("float32") - o).clip(min=0)
    nir = (ds.B08.astype("float32") - o).clip(min=0)
    ok = ds.SCL.isin(SCL_OK) & (ds.B04 > 0) & (ds.B08 > 0)
    ndvi = ((nir - red) / (nir + red)).where(ok & ((nir + red) > 0))
    med = ndvi.median("time", skipna=True).compute().values
    return med, len(days)


def main():
    if os.path.exists(OUT):
        print(OUT, "already exists — delete it to recompute.")
        return
    os.makedirs(PARTS, exist_ok=True)
    client = pystac_client.Client.open(STAC)
    items = list(client.search(collections=[COL], bbox=WINDOW, datetime="2024-08-01/2024-08-31",
                               query={"eo:cloud_cover": {"lt": 60}}).items())
    print(len(items), "Sentinel-2 scenes, August 2024, < 60 % cloud")
    sub, rc = window_geobox()
    ny, nx = sub.shape.y, sub.shape.x
    step = 100                                 # 100 coarse pixels = 1000 fine pixels per block side
    ndays = set()
    for r in range(0, ny, step):
        for c in range(0, nx, step):
            part = f"{PARTS}/block_{r:05d}_{c:05d}.npz"
            if os.path.exists(part):
                continue
            blk = sub[r:min(r + step, ny), c:min(c + step, nx)]
            fine = GeoBox.from_bbox(blk.boundingbox, crs=grid.CRS, resolution=grid.RES / F, tight=False)
            for attempt in range(1, 6):
                try:
                    med, nd = block(items, fine)
                    break
                except Exception as ex:  # noqa: BLE001
                    print(f"block {r},{c} attempt {attempt}: {ex}")
                    time.sleep(15 * attempt)
            else:
                sys.exit("Some blocks failed; re-run the script later.")
            ndays.add(nd)
            h, w = blk.shape.y, blk.shape.x
            m = med[:h * F, :w * F].reshape(h, F, w, F)
            valid = np.isfinite(m).sum(axis=(1, 3))
            gt = (m > 0.3).sum(axis=(1, 3))
            with np.errstate(invalid="ignore", divide="ignore"):
                np.savez_compressed(part, valid_frac=(valid / (F * F)).astype(np.float32),
                                    gt03_frac=np.where(valid > 0, gt / valid, np.nan).astype(np.float32))
            print("block", r, c, "done")
    vf = np.full((ny, nx), np.nan, np.float32)
    gf = np.full((ny, nx), np.nan, np.float32)
    for r in range(0, ny, step):
        for c in range(0, nx, step):
            z = np.load(f"{PARTS}/block_{r:05d}_{c:05d}.npz")
            h, w = z["valid_frac"].shape
            vf[r:r + h, c:c + w] = z["valid_frac"]
            gf[r:r + h, c:c + w] = z["gt03_frac"]
    ds = xr.Dataset({"valid_frac": (("y", "x"), vf), "gt03_frac": (("y", "x"), gf)},
                    coords={"y": sub.coords["y"].values, "x": sub.coords["x"].values},
                    attrs={"source": f"{COL} via Microsoft Planetary Computer, 1–31 Aug 2024, cloud < 60 %",
                           "scenes": len(items), "grid_rows_cols": list(rc),
                           "method": "SCL-masked median NDVI per 23.17 m fine pixel; shares per 231.66 m pixel"})
    ds.to_netcdf(OUT + ".part", encoding={v: {"zlib": True, "complevel": 4} for v in ds.data_vars})
    os.replace(OUT + ".part", OUT)
    print(f"Saved {OUT}. The folder {PARTS} can be deleted.")


if __name__ == "__main__":
    main()
