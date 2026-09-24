"""Step 1 — MODIS Terra MOD13Q1 v6.1 (16-day, 250 m) NDVI/EVI, 2016–2024.

Source: Microsoft Planetary Computer, collection `modis-13Q1-061`
(no account needed). Every 16-day composite is reprojected (nearest
neighbour) onto the common grid in v2/grid.py and saved as one small
NetCDF file:  data/v2/modis/mod13q1_YYYY-MM-DD.nc

The script is resumable: files that already exist are skipped, so if the
internet drops just run it again.

    python v2/01_download_modis.py              # everything (≈207 composites)
    python v2/01_download_modis.py --test       # one composite only, to check setup
    python v2/01_download_modis.py --years 2023 2024
"""
import argparse
import json
import os
import sys
import time
from collections import defaultdict

import planetary_computer
import pystac_client
from odc.stac import load

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import grid  # noqa: E402

STAC = "https://planetarycomputer.microsoft.com/api/stac/v1"
COLLECTION = "modis-13Q1-061"
OUT = "data/v2/modis"
WANT = {  # our variable name -> substring of the asset key, dtype, nodata
    "ndvi": ("250m_16_days_NDVI", "int16", -3000),
    "evi": ("250m_16_days_EVI", "int16", -3000),
    "reliability": ("250m_16_days_pixel_reliability", "int8", -1),
    "doy": ("250m_16_days_composite_day_of_the_year", "int16", -1),
}


def resolve_assets(item):
    keys = list(item.assets)
    found = {}
    for var, (sub, _, _) in WANT.items():
        match = [k for k in keys if k == sub] or [k for k in keys if sub.lower() in k.lower()]
        if not match:
            raise KeyError(f"No asset matching '{sub}'. Available: {keys}")
        found[var] = match[0]
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="*", type=int, default=list(range(2016, 2025)))
    ap.add_argument("--test", action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    grid.describe(os.path.join("data", "v2", "grid.json"))
    gbox = grid.coarse_geobox()

    client = pystac_client.Client.open(STAC)
    items = []
    for y in args.years:
        s = client.search(collections=[COLLECTION], bbox=grid.BBOX_LONLAT, datetime=f"{y}-01-01/{y}-12-31")
        items += [it for it in s.items() if it.id.upper().startswith("MOD13Q1")]  # Terra only
    by_date = defaultdict(list)
    for it in items:
        by_date[it.datetime.strftime("%Y-%m-%d")].append(it)
    dates = sorted(by_date)
    print(f"{len(items)} Terra items, {len(dates)} composites, tiles per composite: "
          f"{sorted({len(v) for v in by_date.values()})}")
    if not dates:
        sys.exit("No items found — check internet / STAC access.")

    assets = resolve_assets(by_date[dates[0]][0])
    print("Asset keys:", assets)
    with open(os.path.join("data", "v2", "modis_assets.json"), "w") as fh:
        json.dump({"assets": assets, "dates": dates, "tiles": {d: [i.id for i in by_date[d]] for d in dates}}, fh, indent=1)
    cfg = {COLLECTION: {"assets": {assets[v]: {"data_type": WANT[v][1], "nodata": WANT[v][2]} for v in WANT}}}

    if args.test:
        dates = dates[:1]
    for n, d in enumerate(dates, 1):
        path = os.path.join(OUT, f"mod13q1_{d}.nc")
        if os.path.exists(path):
            continue
        for attempt in range(1, 6):
            try:
                t0 = time.time()
                signed = [planetary_computer.sign(i) for i in by_date[d]]
                ds = load(signed, bands=[assets[v] for v in WANT], geobox=gbox, groupby="solar_day",
                          chunks={"x": 1024, "y": 1024}, resampling="nearest", stac_cfg=cfg)
                ds = ds.rename({assets[v]: v for v in WANT})
                for v, (_, dt, nd) in WANT.items():
                    ds[v].attrs.update({"_FillValue_source": nd, "source_asset": assets[v]})
                ds.attrs.update({"source": f"{COLLECTION} (Terra), Microsoft Planetary Computer",
                                 "composite_start": d, "grid": "v2/grid.py", "items": ",".join(i.id for i in by_date[d]),
                                 "scale_ndvi_evi": 0.0001})
                enc = {v: {"zlib": True, "complevel": 4, "_FillValue": WANT[v][2],
                           "chunksizes": (1, 512, 512)} for v in WANT}
                tmp = path + ".part"
                ds.to_netcdf(tmp, encoding=enc)
                os.replace(tmp, path)
                print(f"[{n}/{len(dates)}] {d}  saved ({os.path.getsize(path)/1e6:.0f} MB, {time.time()-t0:.0f}s)")
                break
            except Exception as e:  # noqa: BLE001
                print(f"[{n}/{len(dates)}] {d}  attempt {attempt} failed: {e}")
                if os.path.exists(path + ".part"):
                    os.remove(path + ".part")
                time.sleep(20 * attempt)
        else:
            print(f"  giving up on {d} for now — re-run the script later to retry.")
    done = len([f for f in os.listdir(OUT) if f.endswith(".nc")])
    print(f"\nDone. {done} composite files in {OUT}.")


if __name__ == "__main__":
    main()
