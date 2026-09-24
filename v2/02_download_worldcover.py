"""Step 2 — ESA WorldCover 2021 (v200, 10 m) land-cover fractions per analysis pixel.

Source: Microsoft Planetary Computer, collection `esa-worldcover`
(no account needed). The 10 m map is read on a grid 10x finer than the
analysis grid (~23 m) and aggregated, so every 231 m analysis pixel gets
the percentage of each land-cover class inside it.

Output: data/v2/worldcover_2021_fractions.nc  (variables frac_<class>, 0–100 %)

    python v2/02_download_worldcover.py
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid  # noqa: E402

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
OUT = "data/v2/worldcover_2021_fractions.nc"
CLASSES = {10: "tree", 20: "shrub", 30: "grass", 40: "crop", 50: "built", 60: "bare",
           70: "snow", 80: "water", 90: "wetland", 95: "mangrove", 100: "moss"}


def fractions(lc, coarse):
    """lc: fine-grid class map (0 = no data). Returns % of each class per coarse pixel."""
    f = grid.FINE_FACTOR
    out = {}
    valid = (lc > 0)
    nvalid = valid.coarsen(x=f, y=f).sum()
    for code, name in CLASSES.items():
        cnt = (lc == code).coarsen(x=f, y=f).sum()
        out[f"frac_{name}"] = (100 * cnt / nvalid.where(nvalid > 0)).round().fillna(255).astype("uint8")
    out["valid_pct"] = (100 * nvalid / (f * f)).round().astype("uint8")
    ds = xr.Dataset(out)
    ds = ds.assign_coords(x=coarse.coords["x"].values, y=coarse.coords["y"].values)
    return ds


def main():
    if os.path.exists(OUT):
        print(f"{OUT} already exists — delete it to re-download.")
        return
    parts_dir = os.path.join(os.path.dirname(OUT), "worldcover_parts")
    os.makedirs(parts_dir, exist_ok=True)
    client = pystac_client.Client.open(STAC)
    items = list(client.search(collections=["esa-worldcover"], bbox=grid.BBOX_LONLAT,
                               datetime="2021-01-01/2021-12-31").items())
    print(f"{len(items)} WorldCover 2021 tiles")
    coarse = grid.coarse_geobox()
    ny, nx = coarse.shape.y, coarse.shape.x
    step = 500  # coarse pixels per block side (~116 km); each block re-signs its URLs
    blocks = [(r, c) for r in range(0, ny, step) for c in range(0, nx, step)]
    cfg = {"esa-worldcover": {"assets": {"map": {"data_type": "uint8", "nodata": 0}}}}
    for k, (r, c) in enumerate(blocks, 1):
        part = os.path.join(parts_dir, f"block_{r:05d}_{c:05d}.nc")
        if os.path.exists(part):
            continue
        sub = coarse[r:min(r + step, ny), c:min(c + step, nx)]
        fine_sub = GeoBox.from_bbox(sub.boundingbox, crs=grid.CRS, resolution=grid.RES / grid.FINE_FACTOR, tight=False)
        for attempt in range(1, 6):
            try:
                t0 = time.time()
                signed = [planetary_computer.sign(i) for i in items]
                lc = load(signed, bands=["map"], geobox=fine_sub, chunks={"x": 2500, "y": 2500},
                          resampling="nearest", stac_cfg=cfg)["map"]
                lc = lc.isel(time=0, drop=True) if "time" in lc.dims else lc
                cx = xr.DataArray(np.zeros(sub.shape), dims=("y", "x"),
                                  coords={"y": sub.coords["y"].values, "x": sub.coords["x"].values})
                ds = fractions(lc, cx)
                ds.to_netcdf(part + ".part", encoding={v: {"zlib": True, "complevel": 4} for v in ds.data_vars})
                os.replace(part + ".part", part)
                print(f"[{k}/{len(blocks)}] block {r},{c} done ({time.time()-t0:.0f}s)")
                break
            except Exception as e:  # noqa: BLE001
                print(f"[{k}/{len(blocks)}] block {r},{c} attempt {attempt} failed: {e}")
                time.sleep(20 * attempt)
        else:
            print("Some blocks failed — re-run the script to retry them.")
            return
    ds = xr.combine_by_coords([xr.open_dataset(os.path.join(parts_dir, f)) for f in sorted(os.listdir(parts_dir)) if f.endswith(".nc")])
    ds = ds.sortby("y", ascending=False).sortby("x")
    ds.attrs.update({"source": "ESA WorldCover 2021 v200 via Microsoft Planetary Computer",
                     "method": "10 m map sampled on 23.17 m grid, class % per 231.66 m pixel; 255 = no data",
                     "grid": "v2/grid.py"})
    ds.to_netcdf(OUT + ".part", encoding={v: {"zlib": True, "complevel": 4} for v in ds.data_vars})
    os.replace(OUT + ".part", OUT)
    print(f"Saved {OUT} ({os.path.getsize(OUT)/1e6:.0f} MB). The folder {parts_dir} can be deleted.")


if __name__ == "__main__":
    main()
