"""R1-prepare — inputs for Registered Revision 1 (ANALYSIS_PLAN_v2_ADDENDUM_1.md).

Builds on the grid:
  * R1  irrigated / rainfed from July–August NDVI 2010–2015
  * R2  restricted comparison zone (steppe oblasts) + Dnipropetrovsk sensitivity
  * R3  raion (GADM level 2) code
  * R4  occupation per year (VIINA control if available, else the registered fallback),
        conflict intensity per year (VIINA or UCDP events within 5 km, 1 Mar–31 Oct),
        distance to the Dnipro main channel (km)
  * R5  annual water share 2017–2024 (Impact Observatory), where available
Output: data/v2/derived/r1_layers.npz and r1_meta.json
"""
import glob
import json
import os
import sys
import zipfile

import geopandas as gpd
import numpy as np
import pandas as pd
import xarray as xr
from pyproj import Transformer
from scipy import ndimage as ndi
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import grid  # noqa: E402
import v2lib as L  # noqa: E402
import a1_layers as A1  # noqa: E402

RES = grid.RES
STEPPE = ["Odessa", "Mykolayiv", "Kherson", "Zaporizhia"]
YEARS_ALL = list(range(2016, 2025))


def ja_2010_2015(shape):
    out = []
    for y in range(2010, 2016):
        ds = xr.open_dataset(f"{L.D}/annual/annual_{y}.nc")
        v = ds["ndvi_ja"].values / 10000.0
        n = ds["n_ja"].values
        out.append(np.where(n >= 2, v, np.nan).astype(np.float32))
        ds.close()
    return np.stack(out)


def occupation_fallback(A, tr, names):
    """Registered fallback (Addendum R4): 2022 = all of Kherson Oblast + Zaporizhzhia Oblast
    south of 47.45 N; 2023–2024 = Kherson Oblast left bank + Zaporizhzhia Oblast south of 47.45 N."""
    kh = A["oblast"] == names.index("Kherson") + 1
    zp = A["oblast"] == names.index("Zaporizhia") + 1
    zp_s = zp & (A["lat"] < 47.45)
    region = kh & ~A["channel"]
    lab, _ = ndi.label(region, structure=ndi.generate_binary_structure(2, 1))
    seed = A1.snap_to(region, A1.rc_of(A1.LEFT_SEED, tr))
    left = lab == lab[seed]
    occ = np.zeros((len(YEARS_ALL),) + A["F"].shape, bool)
    for k, y in enumerate(YEARS_ALL):
        if y == 2022:
            occ[k] = kh | zp_s
        elif y >= 2023:
            occ[k] = left | zp_s
    return occ, {"left_bank_kherson_px": int(left.sum()), "zaporizhzhia_south_px": int(zp_s.sum())}


def viina_events():
    """VIINA events 2022–2024: settlement- or street-level location (GEO_PRECISION ADM3/STREET)
    and classified as war-related (t_mil >= 0.5)."""
    d = f"{L.D}/conflict"
    frames = []
    for y in (2022, 2023, 2024):
        fi, fl = f"{d}/event_info_latest_{y}.zip", f"{d}/event_labels_latest_{y}.zip"
        if not (os.path.exists(fi) and os.path.exists(fl)):
            return None
        info = pd.read_csv(zipfile.ZipFile(fi).open(f"event_info_latest_{y}.csv"),
                           usecols=["event_id", "date", "longitude", "latitude", "GEO_PRECISION"])
        lab = pd.read_csv(zipfile.ZipFile(fl).open(f"event_labels_latest_{y}.csv"), usecols=["event_id", "t_mil"])
        m = info.merge(lab, on="event_id", how="inner")
        m = m[m.GEO_PRECISION.isin(["ADM3", "STREET"]) & (m.t_mil >= 0.5)]
        frames.append(m)
    ev = pd.concat(frames, ignore_index=True)
    dt = pd.to_datetime(ev["date"].astype(str), format="%Y%m%d", errors="coerce")
    ok = dt.notna()
    return ev.loc[ok, "longitude"].values, ev.loc[ok, "latitude"].values, dt[ok].values


def viina_occupation(A, tr, shape):
    """Addendum R4 primary source: a pixel takes the VIINA control status (on 1 August) of the
    nearest settlement within 10 km; otherwise unoccupied. RU = occupied; UA and CONTESTED = not."""
    d = f"{L.D}/conflict"
    need = [f"{d}/control_latest_{y}.zip" for y in (2022, 2023, 2024)] + [f"{d}/gn_UA_tess.geojson"]
    if not all(os.path.exists(p) for p in need):
        return None, None
    g = json.load(open(f"{d}/gn_UA_tess.geojson", encoding="utf-8"))
    st = pd.DataFrame([{"geonameid": int(f["properties"]["geonameid"]), "lon": f["properties"]["longitude"],
                        "lat": f["properties"]["latitude"]} for f in g["features"]])
    sx, sy = Transformer.from_crs(4326, grid.CRS, always_xy=True).transform(st.lon.values, st.lat.values)
    tree = cKDTree(np.c_[sx, sy])
    rr, cc = np.indices(shape)
    px = np.c_[(tr.c + (cc.ravel() + .5) * RES), (tr.f - (rr.ravel() + .5) * RES)]
    dist, near = tree.query(px, distance_upper_bound=10000)
    has = np.isfinite(dist)
    occ = np.zeros((len(YEARS_ALL),) + shape, bool)
    info = {}
    for y in (2022, 2023, 2024):
        c = pd.read_csv(zipfile.ZipFile(f"{d}/control_latest_{y}.zip").open(f"control_latest_{y}.csv"),
                        usecols=["geonameid", "date", "status"])
        c = c[c.date == int(f"{y}0801")]
        ru = set(c.loc[c.status == "RU", "geonameid"].astype(int))
        flag = np.zeros(len(st), bool)
        flag[st.geonameid.isin(ru).values] = True
        o = np.zeros(px.shape[0], bool)
        o[has] = flag[near[has]]
        occ[YEARS_ALL.index(y)] = o.reshape(shape)
        info[str(y)] = {"settlements_RU_on_1_Aug": len(ru), "occupied_px_in_universe": int((o.reshape(shape) & A["universe"]).sum())}
    info["pixels_without_settlement_within_10km"] = int((~has).reshape(shape)[A["universe"]].sum())
    return occ, info


def conflict_points():
    """Return (lon, lat, date) of conflict events from whatever step 8 downloaded, and the source."""
    v = viina_events()
    if v is not None:
        return v, "VIINA (GEO_PRECISION ADM3/STREET, t_mil >= 0.5)"
    d = f"{L.D}/conflict"
    man_p = f"{d}/conflict_manifest.json"
    if not os.path.exists(man_p):
        return None, "missing"
    man = json.load(open(man_p))
    frames = []
    for f in man.get("files", []):
        p = os.path.join(d, f)
        try:
            if f.endswith(".zip"):
                z = zipfile.ZipFile(p)
                for n in z.namelist():
                    if n.endswith(".csv"):
                        frames.append(pd.read_csv(z.open(n), low_memory=False))
            elif f.endswith(".csv"):
                frames.append(pd.read_csv(p, low_memory=False))
        except Exception as ex:  # noqa: BLE001
            print("could not read", f, ex)
    if not frames:
        return None, man.get("source") or "none"
    df = pd.concat(frames, ignore_index=True)
    cols = {c.lower(): c for c in df.columns}
    lon = cols.get("longitude") or cols.get("lon") or cols.get("x")
    lat = cols.get("latitude") or cols.get("lat") or cols.get("y")
    date = cols.get("date") or cols.get("date_start") or cols.get("event_date")
    if not (lon and lat and date):
        print("conflict columns not recognised:", list(df.columns)[:40])
        return None, man.get("source")
    if "country" in cols:
        df = df[df[cols["country"]].astype(str).str.contains("Ukraine", case=False)]
    dt = pd.to_datetime(df[date].astype(str), errors="coerce", format="mixed")
    ok = dt.notna() & df[lon].notna() & df[lat].notna()
    return (df.loc[ok, lon].astype(float).values, df.loc[ok, lat].astype(float).values, dt[ok].values), man.get("source")


def main():
    A = L.layers()
    meta = json.load(open(f"{L.D}/derived/layers_meta.json"))
    names = meta["oblast_names"]
    tr = A1.from_origin(meta["transform"][2], meta["transform"][5], RES, RES)
    shape = A["F"].shape
    out, info = {}, {}

    # R1
    ja = ja_2010_2015(shape)
    out["irr_r1"] = ((ja >= 0.45).sum(0) >= 4)
    out["rain_r1"] = ((ja < 0.35).sum(0) >= 5)
    both = out["irr_r1"] & out["rain_r1"]
    out["irr_r1"] &= ~both
    out["rain_r1"] &= ~both

    # R2
    steppe = np.isin(A["oblast"], [names.index(n) + 1 for n in STEPPE])
    out["zoneO_r2"] = A["zoneO"] & steppe
    out["zoneO_r2_dnipro"] = A["zoneO"] & (steppe | (A["oblast"] == names.index("Dnipropetrovs'k") + 1))

    # R3 raions
    adm2 = gpd.read_file(A1.GADM, layer="ADM_ADM_2").to_crs(grid.CRS).reset_index(drop=True)
    out["raion"] = A1.rasterize(adm2.geometry, shape, tr, dtype="int16", values=list(range(1, len(adm2) + 1)))
    info["raion_names"] = [f"{a} / {b}" for a, b in zip(adm2.NAME_1, adm2.NAME_2)]

    # R4 distance to channel
    out["dist_channel_km"] = (ndi.distance_transform_edt(~A["channel"]) * RES / 1000).astype(np.float32)

    # R4 occupation: VIINA control if present, else fallback
    occ, occ_info = viina_occupation(A, tr, shape)
    if occ is not None:
        info["occupation_source"] = "VIINA territorial control, 1 August, nearest settlement within 10 km"
    else:
        occ, occ_info = occupation_fallback(A, tr, names)
        info["occupation_source"] = "fallback (Addendum R4)"
    out["occupied"] = occ
    info["occupation"] = occ_info

    # R4 conflict intensity
    pts, src = conflict_points()
    info["conflict_source"] = src
    ci = np.zeros((len(YEARS_ALL),) + shape, np.float32)
    if pts is not None:
        lon, lat, dt = pts
        x, y = Transformer.from_crs(4326, grid.CRS, always_xy=True).transform(lon, lat)
        dt = pd.to_datetime(dt)
        rr, cc = np.indices(shape)
        px = np.c_[(tr.c + (cc.ravel() + .5) * RES), (tr.f - (rr.ravel() + .5) * RES)]
        keep_px = np.flatnonzero((A["universe"] | A["reservoir"]).ravel())
        tree_px = cKDTree(px[keep_px])
        for k, yv in enumerate(YEARS_ALL):
            if yv < 2022:
                continue
            sel = (dt >= pd.Timestamp(yv, 3, 1)) & (dt <= pd.Timestamp(yv, 10, 31))
            if sel.sum() == 0:
                continue
            ev = np.c_[x[sel], y[sel]]
            cnt = np.zeros(len(keep_px), np.float32)
            for nb in tree_px.query_ball_point(ev, r=5000):
                cnt[nb] += 1
            layer = np.zeros(shape[0] * shape[1], np.float32)
            layer[keep_px] = np.log1p(cnt)
            ci[k] = layer.reshape(shape)
            info.setdefault("conflict_events_per_year", {})[str(yv)] = int(sel.sum())
    out["conflict"] = ci

    # R5 annual water share
    water = np.full((len(YEARS_ALL),) + shape, np.nan, np.float32)
    avail = {}
    for k, yv in enumerate(YEARS_ALL):
        cands = [yy for yy in range(2017, yv + 1) if os.path.exists(f"{L.D}/io_lulc/io_water_{yy}.nc")
                 and all(i.endswith(str(yy)) for i in xr.open_dataset(f"{L.D}/io_lulc/io_water_{yy}.nc").attrs["items"].split(","))]
        if yv < 2017 or not cands:
            continue
        use = max(cands)
        ds = xr.open_dataset(f"{L.D}/io_lulc/io_water_{use}.nc")
        r0, r1, c0, c1 = ds.attrs["grid_rows_cols"]
        w = ds.water_pct.values.astype(np.float32)
        w[w == 255] = np.nan
        water[k, r0:r1, c0:c1] = w
        avail[str(yv)] = use
    out["water_annual"] = water
    info["water_years_used"] = avail

    np.savez_compressed(f"{L.D}/derived/r1_layers.npz", **out)
    info["counts"] = {"irr_r1": int(out["irr_r1"].sum()), "rain_r1": int(out["rain_r1"].sum()),
                      "zoneK_irr": int((A["zoneK"] & out["irr_r1"]).sum()), "zoneK_rain": int((A["zoneK"] & out["rain_r1"]).sum()),
                      "zoneO_r2_irr": int((out["zoneO_r2"] & out["irr_r1"]).sum()),
                      "zoneO_r2_rain": int((out["zoneO_r2"] & out["rain_r1"]).sum())}
    json.dump(info, open(f"{L.D}/derived/r1_meta.json", "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in info.items() if k != "raion_names"}, indent=1, default=str))


if __name__ == "__main__":
    main()
