"""Step 6 — turns the 204 MODIS 16-day files into one small file per year with
the seasonal outcomes defined in ANALYSIS_PLAN_v2.md, section 5.

A pixel observation is VALID if pixel reliability is 0 (good) or 1 (marginal)
and NDVI is not missing. It is assigned to a season by its own composite
day-of-year (the `doy` band), not by the composite's start date, so a
composite that starts on 26 June only contributes its pixels observed on or
after 1 July.

Per pixel and year it writes:
    ndvi_jo, n_jo    July–October mean NDVI and number of valid observations
    evi_jo           July–October mean EVI
    ndvi_ja, n_ja    July–August mean NDVI and count
    ndvi_ao, n_ao    April–October mean NDVI and count
    ndvi_ao_p90      April–October 90th percentile NDVI (for the 'cropped' indicator)
NDVI/EVI are stored as int16 × 10,000 (missing = -32768); counts as uint8.
The minimum-count rule (≥ 5 valid in July–October) is applied later, in the
analysis, so that it stays visible and adjustable in one place.

Output: data/v2/annual/annual_YYYY.nc (≈ 30–60 MB each). Resumable: an
existing year is skipped.

    python v2/06_annual_composites.py
    python v2/06_annual_composites.py --years 2023 2024
"""
import argparse
import datetime as dt
import glob
import os
import sys
import time

import numpy as np
import xarray as xr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SRC = "data/v2/modis"
OUT = "data/v2/annual"
FILL = -32768


def doy(y, m, d):
    return dt.date(y, m, d).timetuple().tm_yday


def windows(y):
    last = doy(y, 12, 31)
    return {
        "jo": (doy(y, 7, 1), doy(y, 10, 31)),
        "ja": (doy(y, 7, 1), doy(y, 8, 31)),
        "ao": (doy(y, 4, 1), doy(y, 10, 31)),
        "_last": last,
    }


def files_for_year(y):
    """Composites that can hold April–October pixels of year y."""
    out = []
    for f in sorted(glob.glob(os.path.join(SRC, "mod13q1_*.nc"))):
        d = dt.date.fromisoformat(os.path.basename(f)[8:18])
        if d.year == y and dt.date(y, 3, 15) <= d <= dt.date(y, 10, 31):
            out.append(f)
    return out


def to_i16(a):
    o = np.full(a.shape, FILL, dtype=np.int16)
    ok = np.isfinite(a)
    o[ok] = np.clip(np.round(a[ok]), -10000, 10000).astype(np.int16)
    return o


def process_year(y):
    path = os.path.join(OUT, f"annual_{y}.nc")
    if os.path.exists(path):
        print(f"{y}: exists, skipped")
        return
    fs = files_for_year(y)
    if not fs:
        print(f"{y}: no MODIS files found in {SRC}")
        return
    t0 = time.time()
    w = windows(y)
    ref = xr.open_dataset(fs[0])
    shape = ref.ndvi.shape[-2:]
    acc = {k: np.zeros(shape, np.float64) for k in ("s_jo", "e_jo", "s_ja", "s_ao")}
    cnt = {k: np.zeros(shape, np.uint8) for k in ("n_jo", "ej", "n_ja", "n_ao")}
    ao_stack = []
    used = []
    for f in fs:
        ds = xr.open_dataset(f)
        nd = ds.ndvi.values[0].astype(np.float32)
        ev = ds.evi.values[0].astype(np.float32)
        rl = ds.reliability.values[0]
        dy = ds.doy.values[0]
        ds.close()
        valid = np.isfinite(nd) & np.isfinite(rl) & (rl <= 1) & (rl >= 0) & np.isfinite(dy)
        dyi = np.where(np.isfinite(dy), dy, -1).astype(np.int32)
        m_jo = valid & (dyi >= w["jo"][0]) & (dyi <= w["jo"][1])
        m_ja = valid & (dyi >= w["ja"][0]) & (dyi <= w["ja"][1])
        m_ao = valid & (dyi >= w["ao"][0]) & (dyi <= w["ao"][1])
        acc["s_jo"][m_jo] += nd[m_jo]
        cnt["n_jo"][m_jo] += 1
        evv = m_jo & np.isfinite(ev)
        acc["e_jo"][evv] += ev[evv]
        cnt["ej"][evv] += 1
        acc["s_ja"][m_ja] += nd[m_ja]
        cnt["n_ja"][m_ja] += 1
        acc["s_ao"][m_ao] += nd[m_ao]
        cnt["n_ao"][m_ao] += 1
        if m_ao.any():
            layer = np.where(m_ao, nd, np.nan).astype(np.float32)
            ao_stack.append(layer)
        used.append(os.path.basename(f)[8:18])

    def mean(s, n):
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(n > 0, s / np.maximum(n, 1), np.nan)

    if ao_stack:
        st = np.stack(ao_stack)
        p90 = np.full(shape, np.nan, np.float32)
        rows = 256  # row blocks keep memory low
        for r in range(0, shape[0], rows):
            # fast NaN-aware 90th percentile (same 'linear' rule as numpy.nanpercentile)
            blk = np.sort(st[:, r:r + rows], axis=0)  # NaNs sort to the end
            n = np.isfinite(blk).sum(axis=0)
            pos = 0.9 * np.maximum(n - 1, 0)
            lo = np.floor(pos).astype(np.int64)
            hi = np.minimum(lo + 1, np.maximum(n - 1, 0))
            frac = (pos - lo).astype(np.float32)
            vlo = np.take_along_axis(blk, lo[None], axis=0)[0]
            vhi = np.take_along_axis(blk, hi[None], axis=0)[0]
            p90[r:r + rows] = np.where(n > 0, vlo + (vhi - vlo) * frac, np.nan)
        del st
    else:
        p90 = np.full(shape, np.nan, np.float32)

    dims = ("y", "x")
    out = xr.Dataset(
        {
            "ndvi_jo": (dims, to_i16(mean(acc["s_jo"], cnt["n_jo"]))),
            "n_jo": (dims, cnt["n_jo"]),
            "evi_jo": (dims, to_i16(mean(acc["e_jo"], cnt["ej"]))),
            "ndvi_ja": (dims, to_i16(mean(acc["s_ja"], cnt["n_ja"]))),
            "n_ja": (dims, cnt["n_ja"]),
            "ndvi_ao": (dims, to_i16(mean(acc["s_ao"], cnt["n_ao"]))),
            "n_ao": (dims, cnt["n_ao"]),
            "ndvi_ao_p90": (dims, to_i16(p90)),
        },
        coords={"y": ref.y.values, "x": ref.x.values},
        attrs={
            "year": y, "source_composites": ",".join(used),
            "valid_rule": "MOD13Q1 pixel reliability 0 or 1; season by pixel composite day-of-year",
            "windows_doy": f"jo={w['jo']}, ja={w['ja']}, ao={w['ao']}",
            "scale": "NDVI/EVI stored as value x 10000, fill -32768",
            "grid": "v2/grid.py (EPSG:3035, 231.656358 m)",
        },
    )
    ref.close()
    enc = {v: {"zlib": True, "complevel": 5, "chunksizes": (512, 512)} for v in out.data_vars}
    for v in ("ndvi_jo", "evi_jo", "ndvi_ja", "ndvi_ao", "ndvi_ao_p90"):
        enc[v]["_FillValue"] = FILL
    os.makedirs(OUT, exist_ok=True)
    tmp = path + ".part"
    out.to_netcdf(tmp, encoding=enc)
    os.replace(tmp, path)
    njo = cnt["n_jo"]
    print(f"{y}: {len(used)} composites -> {path} ({os.path.getsize(path)/1e6:.0f} MB, {time.time()-t0:.0f}s); "
          f"pixels with >=5 valid Jul-Oct obs: {(njo >= 5).mean()*100:.1f}% of grid")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", nargs="*", type=int, default=list(range(2016, 2025)))
    a = ap.parse_args()
    for y in a.years:
        process_year(y)
    print("\nDone. Tell Claude when finished; the files in data/v2/annual are what it needs next.")


if __name__ == "__main__":
    main()
