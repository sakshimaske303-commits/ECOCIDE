"""R2-prepare — inputs for Registered Revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md).

Builds on the grid:
  * R9   irrigated fraction per pixel and year from the Baber et al. (2026b) 30 m maps (2019–2025),
         map coverage, mean 2019–2021 fraction, "contains a mapped field", distance to such pixels (km)
  * R8   new zone O: restricted zone O (R2) more than 30 km from the canal network and, in the two
         oblasts, more than 5 km from any pixel that contains a mapped field
  * R10  DEM mean elevation and relative height above the Dnipro main channel
  * R9   validation table: R1 classes against R9 classes on cropland of the two oblasts
Output: data/v2/derived/r2_layers.npz and r2_meta.json
"""
import glob
import json
import os
import re
import sys

import numpy as np
import rasterio
import xarray as xr
from rasterio.warp import Resampling, reproject
from rasterio.windows import Window
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import grid  # noqa: E402
import v2lib as L  # noqa: E402
import a1_layers as A1  # noqa: E402

RES = grid.RES
IRR_DIR = f"{L.D}/irrigation_baber"
DEM = f"{L.D}/dem_glo30_mean.nc"
TWO = ["Kherson", "Zaporizhia"]
FIELD_MIN = 0.05        # "contains a mapped field": irrigated fraction >= 5 % in at least one year 2019–2021


def semantics(path):
    """How a map stores 'irrigated'. Binary (values within {0, 1} apart from no-data) -> value 1;
    probabilities (float within [0, 1]) -> p >= 0.5. The Baber et al. files carry no no-data tag but use
    -999 outside the mapped area; a negative integer sentinel is therefore read as no-data. Anything else
    stops the run (a new rule would be a deviation that must be written down before continuing)."""
    with rasterio.open(path) as src:
        nd = src.nodata
        a = src.read(1, out_shape=(min(src.height, 2000), min(src.width, 2000)))
    v = a[np.isfinite(a)] if a.dtype.kind == "f" else a.ravel()
    if nd is not None:
        v = v[v != nd]
    u = np.unique(v)
    if nd is None and a.dtype.kind == "i" and u.size and u.min() < 0 and set(u[u < 0].tolist()) == {int(u.min())}:
        nd = int(u.min())
        u = u[u != nd]
    if u.size <= 2 and set(np.round(u, 6).tolist()) <= {0.0, 1.0}:
        return {"kind": "binary", "nodata": nd, "values": u.tolist()}
    if a.dtype.kind == "f" and u.min() >= 0 and u.max() <= 1:
        return {"kind": "probability", "nodata": nd, "range": [float(u.min()), float(u.max())]}
    sys.exit(f"{os.path.basename(path)}: values {u[:20].tolist()} (nodata {nd}) are neither 0/1 nor probabilities; "
             "stop and record a deviation before continuing.")


def to_grid(path, sem, shape, tr, rows=1024):
    """Irrigated fraction and map coverage on the analysis grid (area-weighted average). The 30 m map is
    read in row bands into two uint8 arrays (irrigated 0/1 with 255 = no data; covered 0/1) to keep memory low."""
    with rasterio.open(path) as src:
        nd = sem["nodata"]
        irr8 = np.empty((src.height, src.width), np.uint8)
        cov8 = np.empty((src.height, src.width), np.uint8)
        for r0 in range(0, src.height, rows):
            h = min(rows, src.height - r0)
            a = src.read(1, window=Window(0, r0, src.width, h))
            valid = np.isfinite(a) if a.dtype.kind == "f" else np.ones(a.shape, bool)
            if nd is not None:
                valid &= a != nd
            if a.dtype.kind == "i":
                valid &= a >= 0          # negative sentinels (-999) are no-data even where the sample missed them
            irr = (a == 1) if sem["kind"] == "binary" else (a >= 0.5)
            irr8[r0:r0 + h] = np.where(valid, irr, 255).astype(np.uint8)
            cov8[r0:r0 + h] = valid
        frac = np.full(shape, np.nan, np.float32)
        cov = np.zeros(shape, np.float32)
        kw = dict(src_transform=src.transform, src_crs=src.crs, dst_transform=tr, dst_crs=grid.CRS,
                  resampling=Resampling.average)
        reproject(irr8, frac, src_nodata=255, dst_nodata=np.nan, **kw)
        reproject(cov8, cov, **kw)
    del irr8, cov8
    return frac, cov


def main():
    A = L.layers()
    R1 = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    meta = json.load(open(f"{L.D}/derived/layers_meta.json"))
    names = meta["oblast_names"]
    tr = A1.from_origin(meta["transform"][2], meta["transform"][5], RES, RES)
    shape = A["F"].shape
    out, info = {}, {"files": {}}

    # ---- R9 irrigated fractions
    files = sorted(glob.glob(f"{IRR_DIR}/*.tif"))
    if not files:
        sys.exit(f"No maps in {IRR_DIR}; run v2/09_download_irrigation_maps.py first.")
    for p in files:
        y = int(re.search(r"(20\d\d)", os.path.basename(p)).group(1))
        sem = semantics(p)
        frac, cov = to_grid(p, sem, shape, tr)
        out[f"irrfrac_{y}"] = frac.astype(np.float16)
        out[f"irrcov_{y}"] = cov.astype(np.float16)
        info["files"][os.path.basename(p)] = {"year": y, **sem,
                                              "irrigated_km2_on_grid": float(np.nansum(frac * cov) * RES * RES / 1e6)}
        print(y, sem, round(info["files"][os.path.basename(p)]["irrigated_km2_on_grid"]), "km2", flush=True)
    for y in (2019, 2020, 2021):
        if f"irrfrac_{y}" not in out:
            sys.exit(f"map for {y} missing")
    fr = np.stack([out[f"irrfrac_{y}"].astype(np.float32) for y in (2019, 2020, 2021)])
    cv = np.stack([out[f"irrcov_{y}"].astype(np.float32) for y in (2019, 2020, 2021)])
    covered = (cv >= 0.5).all(0)
    out["covered"] = covered
    out["irr_mean_1921"] = np.where(covered, np.nanmean(np.where(cv >= 0.5, fr, np.nan), axis=0), np.nan).astype(np.float32)
    out["irr_max_1921"] = np.where(covered, np.nanmax(np.where(cv >= 0.5, fr, np.nan), axis=0), np.nan).astype(np.float32)
    contains = np.nan_to_num(np.where(cv >= 0.5, fr, 0)).max(0) >= FIELD_MIN
    out["contains_field"] = contains
    out["dist_field_km"] = (ndi.distance_transform_edt(~contains) * RES / 1000).astype(np.float32)

    # ---- R8 new zone O
    two = np.isin(A["oblast"], [names.index(n) + 1 for n in TWO])
    out["two_oblasts"] = two
    out["zoneO_r8"] = R1["zoneO_r2"] & (A["dist_net"] > 30) & ~(two & (out["dist_field_km"] <= 5))

    # ---- R10 DEM, relative height above the Dnipro main channel
    if os.path.exists(DEM):
        e = xr.open_dataset(DEM).elev_m.values.astype(np.float32)
        assert e.shape == shape, (e.shape, shape)
        # pixels next to areas without DEM tiles (open sea) can average in the fill value; no land in the
        # study area lies below -10 m, so lower values are set to no-data
        info["dem_pixels_below_minus10m_set_to_nodata"] = int(np.nansum(e < -10))
        e[e < -10] = np.nan
        out["dem"] = e
        ch = A["channel"] & np.isfinite(e)
        _, (ir, ic) = ndi.distance_transform_edt(~ch, return_indices=True)
        out["relh_dnipro"] = (e - e[ir, ic]).astype(np.float32)
        info["dem"] = {"min": float(np.nanmin(e)), "max": float(np.nanmax(e)), "nodata_share": float(np.isnan(e).mean())}
    else:
        print(f"WARNING: {DEM} missing — run v2/10_download_dem.py before r2_h1.py")

    # ---- R9 validation: R1 classes vs R9 classes, cropland of the two oblasts
    crop = A["universe"] & (A["crop"] >= 60) & ~A["reservoir"] & ~A["F"] & ~A["any_june"] & ~A["channel"]
    base = crop & two & covered
    r9_irr = base & (out["irr_mean_1921"] >= 0.5)
    r9_never = base & (out["irr_max_1921"] < FIELD_MIN)
    r1c = {"R1 irrigated": R1["irr_r1"], "R1 rainfed": R1["rain_r1"], "R1 unclassified": ~(R1["irr_r1"] | R1["rain_r1"])}
    r9c = {"R9 irrigated (>= 50 %)": r9_irr, "R9 never irrigated (< 5 % every year)": r9_never,
           "R9 in between": base & ~r9_irr & ~r9_never}
    val = {}
    for ob in TWO:
        m = base & (A["oblast"] == names.index(ob) + 1)
        val[ob] = {a: {b: int((m & ma & mb).sum()) for b, mb in r9c.items()} for a, ma in r1c.items()}
    info["validation_R1_vs_R9_pixels"] = val
    info["counts"] = {"covered_cropland_two_oblasts": int(base.sum()), "r9_irrigated": int(r9_irr.sum()),
                      "r9_irrigated_canal_fed": int((r9_irr & (A["dist_net"] <= 30)).sum()),
                      "r9_irrigated_not_canal_fed": int((r9_irr & (A["dist_net"] > 30)).sum()),
                      "r9_never": int(r9_never.sum()),
                      "r9_never_gt5km": int((r9_never & (out["dist_field_km"] > 5)).sum()),
                      "r9_never_gt2km": int((r9_never & (out["dist_field_km"] > 2)).sum()),
                      "zoneO_r2": int(R1["zoneO_r2"].sum()), "zoneO_r8": int(out["zoneO_r8"].sum())}
    out["crop_r2"] = crop
    np.savez_compressed(f"{L.D}/derived/r2_layers.npz", **out)
    json.dump(info, open(f"{L.D}/derived/r2_meta.json", "w"), indent=1, default=str)
    print(json.dumps(info, indent=1, default=str))


if __name__ == "__main__":
    main()
