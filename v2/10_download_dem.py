"""Step 10 (Registered Revision 2, R10) — Copernicus DEM GLO-30, mean elevation per analysis pixel.

Source: Microsoft Planetary Computer, collection `cop-dem-glo-30` (no account needed). The 30 m DEM
is averaged onto the 231.66 m grid of v2/grid.py, block by block. Run ONLY after
ANALYSIS_PLAN_v2_ADDENDUM_2.md is committed. Resumable.

Output: data/v2/dem_glo30_mean.nc (variable elev_m, float32, metres; NaN = no data)

    python v2/10_download_dem.py
"""
import os
import sys
import time

import numpy as np
import planetary_computer
import pystac_client
import xarray as xr
from odc.stac import load

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid  # noqa: E402

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
COL = "cop-dem-glo-30"
OUT = "data/v2/dem_glo30_mean.nc"
PARTS = "data/v2/dem_parts"


def main():
    if os.path.exists(OUT):
        print(OUT, "already exists — delete it to re-download.")
        return
    os.makedirs(PARTS, exist_ok=True)
    client = pystac_client.Client.open(STAC)
    items = list(client.search(collections=[COL], bbox=grid.BBOX_LONLAT).items())
    print(len(items), "DEM tiles")
    coarse = grid.coarse_geobox()
    ny, nx = coarse.shape.y, coarse.shape.x
    step = 400
    for r in range(0, ny, step):
        for c in range(0, nx, step):
            part = f"{PARTS}/block_{r:05d}_{c:05d}.nc"
            if os.path.exists(part):
                continue
            sub = coarse[r:min(r + step, ny), c:min(c + step, nx)]
            for attempt in range(1, 6):
                try:
                    signed = [planetary_computer.sign(i) for i in items]
                    d = load(signed, bands=["data"], geobox=sub, resampling="average", chunks={"x": 400, "y": 400},
                             stac_cfg={COL: {"assets": {"data": {"data_type": "float32", "nodata": -32767}}}})["data"]
                    d = (d.isel(time=0, drop=True) if "time" in d.dims else d).astype("float32")
                    d = d.where(d > -1000)
                    xr.Dataset({"elev_m": d}).to_netcdf(part + ".part")
                    os.replace(part + ".part", part)
                    print("block", r, c, "done")
                    break
                except Exception as ex:  # noqa: BLE001
                    print(f"block {r},{c} attempt {attempt}: {ex}")
                    time.sleep(15 * attempt)
            else:
                sys.exit("Some blocks failed; re-run the script later.")
    ds = xr.combine_by_coords([xr.open_dataset(os.path.join(PARTS, f)) for f in sorted(os.listdir(PARTS))
                               if f.endswith(".nc")])
    ds = ds.sortby("y", ascending=False).sortby("x")
    for v in [v for v in ds.coords if v not in ("x", "y")]:
        ds = ds.drop_vars(v)
    assert ds.elev_m.shape == (ny, nx), ds.elev_m.shape
    ds.attrs.update({"source": f"{COL} via Microsoft Planetary Computer", "method": "mean of 30 m cells per 231.66 m pixel",
                     "grid": "v2/grid.py"})
    ds.to_netcdf(OUT + ".part", encoding={"elev_m": {"zlib": True, "complevel": 4}})
    os.replace(OUT + ".part", OUT)
    e = ds.elev_m.values
    print(f"Saved {OUT}; elevation {np.nanmin(e):.0f}–{np.nanmax(e):.0f} m; {np.isnan(e).mean() * 100:.1f}% no data. "
          f"The folder {PARTS} can be deleted.")


if __name__ == "__main__":
    main()
