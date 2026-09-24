"""A1 — static pixel layers on the v2 grid (ANALYSIS_PLAN_v2.md §4).

Builds, for every 231.66 m pixel of the grid:
  * inbox, ukraine, crimea, oblast code         (plan §3, §4.0)
  * WorldCover fractions, dominant class, pure  (§4.0)
  * flood fraction: UNOSAT 6–9 June composite, and max over every other
    June 2023 UNOSAT flood layer              (§4.1)
  * reservoir bed (Kakhovka)                  (§4.2)
  * Dnipro main channel, left/right bank      (§4.1)
  * Kakhovka canal network, zone K / zone O   (§4.3)
  * distances (km) to flooded land, reservoir, canal network
  * 10 km block id for clustering             (§6)

Output: data/v2/derived/layers.npz  (+ layers_meta.json)
"""
import json
import os
import sys
import time
import zipfile

import geopandas as gpd
import numpy as np
import rasterio.features as rf
import shapely
import xarray as xr
from pyproj import Transformer
from rasterio.transform import from_origin
from scipy import ndimage as ndi
from shapely.geometry import LineString, Point
from skimage.graph import route_through_array

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import grid  # noqa: E402

D = "data/v2"
OUT = f"{D}/derived"
ZIP = "data/ndwi/FL20230606UKR_SHP.zip"
GADM = "data/boundaries/gadm41_UKR.gpkg"
COMPOSITE = "ST3_20230606_20230607_20230609_ST2_20230608_ICEYE_20230607_FloodExtent_KhersonskaOblast.shp"
PREBREACH_WATER = "ST2_20230603_20230605_WaterExtent_KhersonskaOblast_UKR.shp"
CLASSES = ["tree", "shrub", "grass", "crop", "built", "bare", "snow", "water", "wetland", "mangrove", "moss"]
RES = grid.RES
KAKHOVKA_DAM = (33.37, 46.78)
ZAP_DAM = (35.08, 47.87)
ESTUARY_MOUTH = (31.55, 46.58)
RIGHT_SEED = (32.40, 46.75)   # Chornobaivka area, north-west of Kherson city (right bank)
LEFT_SEED = (33.00, 46.45)    # Oleshky sands (left bank)


def grid_frame():
    ref = xr.open_dataset(f"{D}/worldcover_2021_fractions.nc")
    x, y = ref.x.values, ref.y.values
    tr = from_origin(x[0] - RES / 2, y[0] + RES / 2, RES, RES)
    return ref, x, y, tr


def rasterize(geoms, shape, tr, all_touched=False, dtype="uint8", values=None):
    if values is None:
        shapes = [(g, 1) for g in geoms if g is not None and not g.is_empty]
    else:
        shapes = [(g, v) for g, v in zip(geoms, values) if g is not None and not g.is_empty]
    if not shapes:
        return np.zeros(shape, dtype)
    return rf.rasterize(shapes, out_shape=shape, transform=tr, all_touched=all_touched, dtype=dtype)


def fraction(geom, shape, tr, factor=10):
    """Fraction (0–1) of each coarse pixel covered by geom, via a 10x finer grid,
    computed only in the window that contains geom."""
    if geom is None or geom.is_empty:
        return np.zeros(shape, np.float32)
    minx, miny, maxx, maxy = geom.bounds
    c0 = max(int((minx - tr.c) // RES) - 1, 0)
    c1 = min(int((maxx - tr.c) // RES) + 2, shape[1])
    r0 = max(int((tr.f - maxy) // RES) - 1, 0)
    r1 = min(int((tr.f - miny) // RES) + 2, shape[0])
    ftr = from_origin(tr.c + c0 * RES, tr.f - r0 * RES, RES / factor, RES / factor)
    out = np.zeros(shape, np.float32)
    rows_per = max(1, 200)  # process in row bands to bound memory
    for rr in range(r0, r1, rows_per):
        re_ = min(rr + rows_per, r1)
        btr = from_origin(tr.c + c0 * RES, tr.f - rr * RES, RES / factor, RES / factor)
        fshape = ((re_ - rr) * factor, (c1 - c0) * factor)
        fine = rf.rasterize([(geom, 1)], out_shape=fshape, transform=btr, dtype="uint8")
        frac = fine.reshape(re_ - rr, factor, c1 - c0, factor).mean(axis=(1, 3))
        out[rr:re_, c0:c1] = frac
    del ftr
    return out


def read_unosat(layer):
    return gpd.read_file(f"zip://{ZIP}!FL20230606UKR_SHP/{layer}").to_crs(grid.CRS)


def rc_of(lonlat, tr):
    x, y = Transformer.from_crs(4326, grid.CRS, always_xy=True).transform(*lonlat)
    return int((tr.f - y) // RES), int((x - tr.c) // RES)


def snap_to(mask, rc):
    """nearest True pixel of mask to (row, col)."""
    _, (ir, ic) = ndi.distance_transform_edt(~mask, return_indices=True)
    return int(ir[rc]), int(ic[rc])


def main():
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    wc, x, y, tr = grid_frame()
    shape = (len(y), len(x))
    meta = {"shape": shape, "transform": list(tr)[:6], "crs": grid.CRS, "notes": []}

    # ---------- lon/lat, study box ----------
    X, Y = np.meshgrid(x, y)
    lon, lat = Transformer.from_crs(grid.CRS, 4326, always_xy=True).transform(X, Y)
    w, s, e, n = grid.BBOX_LONLAT
    inbox = (lon >= w) & (lon <= e) & (lat >= s) & (lat <= n)
    del X, Y

    # ---------- admin ----------
    adm1 = gpd.read_file(GADM, layer="ADM_ADM_1").to_crs(grid.CRS)
    adm1 = adm1[adm1.GID_1 != "?"].reset_index(drop=True)
    names = list(adm1.NAME_1)
    oblast = rasterize(adm1.geometry, shape, tr, dtype="int16", values=list(range(1, len(adm1) + 1)))
    ukraine = oblast > 0
    crimea = np.isin(oblast, [names.index("Crimea") + 1, names.index("Sevastopol'") + 1])
    meta["oblast_names"] = names

    # ---------- WorldCover ----------
    fr = np.stack([wc[f"frac_{c}"].values.astype(np.float32) for c in CLASSES])  # percent
    valid_pct = wc.valid_pct.values.astype(np.float32)
    dom = fr.argmax(axis=0).astype(np.int8)
    dom_frac = fr.max(axis=0)
    pure = dom_frac >= 60
    water = fr[CLASSES.index("water")]
    crop = fr[CLASSES.index("crop")]
    built = fr[CLASSES.index("built")]
    universe = inbox & ukraine & ~crimea & (valid_pct >= 90)

    # ---------- flood ----------
    comp = read_unosat(COMPOSITE).union_all()
    flood = fraction(comp, shape, tr)
    zf = zipfile.ZipFile(ZIP)
    layers = sorted({n.split("/")[-1] for n in zf.namelist() if n.endswith("FloodExtent_KhersonskaOblast_UKR.shp")
                     or n.endswith("FloodExtent_KhersonskarOblast_UKR.shp") or "FloodExtent" in n and n.endswith(".shp")})
    other = [l for l in layers if l != COMPOSITE]
    any_other = np.zeros(shape, np.float32)
    for l in other:
        g = read_unosat(l).union_all()
        any_other = np.maximum(any_other, fraction(g, shape, tr))
    meta["flood_layers_other"] = other
    F = universe & (flood >= 0.5) & (water < 20)
    excl_partial = (flood >= 0.10) & (flood < 0.5)
    excl_other = (any_other > 0) & (flood < 0.10)
    any_june = np.maximum(flood, any_other) > 0

    # ---------- pre-breach water (UNOSAT 3–5 June) ----------
    pre = read_unosat(PREBREACH_WATER).union_all()
    prewater = fraction(pre, shape, tr)

    # ---------- reservoir bed (§4.2) ----------
    wat50 = water >= 50
    lab, _ = ndi.label(wat50 & (lon > 33.40) & (lon < 35.15) & (lat < 47.87) & (lat > 46.70))
    # the Kakhovka reservoir is the largest water body between the two dams
    sizes_w = np.bincount(lab.ravel())
    sizes_w[0] = 0
    reservoir = lab == int(sizes_w.argmax())
    meta["reservoir_km2"] = float(reservoir.sum() * RES * RES / 1e6)

    # ---------- Dnipro main channel and banks (§4.1) ----------
    riv = (prewater >= 0.5) | wat50
    dist_in = ndi.distance_transform_edt(riv)
    cost = np.where(riv, 1.0 / (1.0 + dist_in) ** 2, 1e4)
    a = snap_to(riv, rc_of((33.35, 46.765), tr))
    b = snap_to(riv, rc_of(ESTUARY_MOUTH, tr))
    zdam = snap_to(riv, rc_of(ZAP_DAM, tr))
    path1, _ = route_through_array(cost, a, b, fully_connected=False, geometric=True)
    path2, _ = route_through_array(cost, zdam, a, fully_connected=False, geometric=True)
    channel = np.zeros(shape, bool)
    for p in (path1, path2):
        r_, c_ = np.array(p).T
        channel[r_, c_] = True
    channel = ndi.binary_dilation(channel, structure=ndi.generate_binary_structure(2, 1))
    # downstream-of-dam channel pixels with their along-channel distance from the dam
    along = np.full(shape, np.nan, np.float32)
    pr, pc = np.array(path1).T
    steps = np.r_[0, np.cumsum(np.hypot(np.diff(pr), np.diff(pc)))] * RES / 1000
    along[pr, pc] = steps

    distF = ndi.distance_transform_edt(~F) * RES / 1000
    region = ukraine & (distF <= 30) & ~channel
    lab, nlab = ndi.label(region, structure=ndi.generate_binary_structure(2, 1))
    sizes = ndi.sum(np.ones(shape), lab, index=np.arange(1, nlab + 1))
    rs, ls = lab[snap_to(region, rc_of(RIGHT_SEED, tr))], lab[snap_to(region, rc_of(LEFT_SEED, tr))]
    assert rs != ls, "banks not separated — check channel"
    bank = np.zeros(shape, np.int8)  # 1 right, 2 left, 0 none
    bank[lab == rs] = 1
    bank[lab == ls] = 2
    small = (lab > 0) & (lab != rs) & (lab != ls)
    if small.any():  # small separate pieces: nearest main bank
        _, (ir, ic) = ndi.distance_transform_edt(bank == 0, return_indices=True)
        bank[small] = bank[ir[small], ic[small]]
    meta["bank_components"] = {"n": int(nlab), "right_px": int((lab == rs).sum()), "left_px": int((lab == ls).sum()),
                               "reassigned_small_px": int(small.sum())}

    # ---------- Kakhovka canal network (§4.3) ----------
    cg = gpd.read_file(f"{D}/osm_canals.geojson").to_crs(grid.CRS)
    res_shapes = [shapely.geometry.shape(g) for g, v in rf.shapes(reservoir.astype("uint8"), mask=reservoir, transform=tr)]
    res_poly = shapely.union_all(res_shapes)
    down5 = np.where((along <= 5))
    dn_pts = [Point(tr.c + (c + .5) * RES, tr.f - (r + .5) * RES) for r, c in zip(*down5)]
    dn_line = LineString(dn_pts) if len(dn_pts) > 1 else Point(0, 0)
    seed_zone = shapely.union_all([res_poly.buffer(2000), dn_line.buffer(2000)])
    geoms = cg.geometry.values
    tree = shapely.STRtree(geoms)
    inside = set(tree.query(seed_zone, predicate="intersects").tolist())
    # connectivity: segments within 50 m of each other, iterated to convergence
    frontier = set(inside)
    while frontier:
        new = set()
        for i in frontier:
            for j in tree.query(geoms[i], predicate="dwithin", distance=50).tolist():
                if j not in inside:
                    new.add(j)
        inside |= new
        frontier = new
    net = cg.iloc[sorted(inside)]
    meta["kakhovka_network"] = {"segments": int(len(net)), "km": float(net.length.sum() / 1000),
                                "all_segments": int(len(cg))}
    netr = rasterize(net.geometry, shape, tr, all_touched=True).astype(bool)
    dist_net = ndi.distance_transform_edt(~netr) * RES / 1000
    dist_res = ndi.distance_transform_edt(~reservoir) * RES / 1000
    is_crop = crop >= 60
    zoneK = universe & is_crop & (dist_net <= 5) & ~reservoir
    zoneO = universe & is_crop & (dist_res > 30) & (dist_net > 5)

    # ---------- blocks ----------
    bsz = int(round(10000 / RES))
    rr, cc = np.indices(shape)
    block = ((rr // bsz) * (shape[1] // bsz + 1) + cc // bsz).astype(np.int32)

    arrays = dict(lon=lon.astype(np.float32), lat=lat.astype(np.float32), inbox=inbox, ukraine=ukraine,
                  crimea=crimea, oblast=oblast, universe=universe, valid_pct=valid_pct.astype(np.uint8),
                  dom=dom, dom_frac=dom_frac.astype(np.uint8), pure=pure, water=water.astype(np.uint8),
                  crop=crop.astype(np.uint8), built=built.astype(np.uint8), flood=flood, any_other=any_other,
                  any_june=any_june, F=F, excl_partial=excl_partial, excl_other=excl_other, prewater=prewater,
                  reservoir=reservoir, channel=channel, bank=bank, distF=distF.astype(np.float32),
                  netr=netr, dist_net=dist_net.astype(np.float32), dist_res=dist_res.astype(np.float32),
                  zoneK=zoneK, zoneO=zoneO, block=block)
    np.savez_compressed(f"{OUT}/layers.npz", **arrays)
    net.to_file(f"{OUT}/kakhovka_canal_network.gpkg")
    meta.update({
        "classes": CLASSES,
        "counts_px": {"universe": int(universe.sum()), "F": int(F.sum()), "excl_partial": int(excl_partial.sum()),
                      "excl_other": int(excl_other.sum()), "reservoir": int(reservoir.sum()),
                      "zoneK": int(zoneK.sum()), "zoneO": int(zoneO.sum())},
        "F_km2": float(F.sum() * RES * RES / 1e6),
        "F_by_bank_px": {"right": int((F & (bank == 1)).sum()), "left": int((F & (bank == 2)).sum()),
                         "none": int((F & (bank == 0)).sum())},
        "seconds": round(time.time() - t0),
    })
    with open(f"{OUT}/layers_meta.json", "w") as fh:
        json.dump(meta, fh, indent=1, default=str)
    print(json.dumps({k: v for k, v in meta.items() if k not in ("transform",)}, indent=1, default=str))


if __name__ == "__main__":
    main()
