"""R2-H3/H4 — Registered Revision 2 for the descriptive hypotheses (ANALYSIS_PLAN_v2_ADDENDUM_2.md).

R12 (H3 check): 2024 area with NDVI > 0.3 on the former reservoir bed, MODIS (Revision 1 land pixel-years)
     against Sentinel-2 August 2024 median NDVI, on the same bed pixels.
H4:  Kherson Oblast change 2016–2018 mean -> 2023–2024 mean by category, weather-adjusted with the R9 model,
     relative to the area of the new zone O, with 95 % block-bootstrap intervals.
Output: outputs/v2/r2_h3_h4_results.json
"""
import json
import os
import sys

import numpy as np
import xarray as xr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
import r1_h1 as R1H1  # noqa: E402
import r2lib as R2L  # noqa: E402

OUT = "outputs/v2"
RES_KM2 = (R2L.RES / 1000) ** 2
YRS = np.array(L.YEARS)
B_DRAWS = 999
STEPPE = ["Odessa", "Mykolayiv", "Kherson", "Zaporizhia"]   # = r1_prepare.STEPPE (Revision 1, R2)


def h3_check(A, R1):
    path = f"{L.D}/s2_aug2024_reservoir.nc"
    if not os.path.exists(path):
        return {"skipped": f"{path} missing — run v2/11_download_s2_reservoir.py"}
    s2 = xr.open_dataset(path)
    r0, r1, c0, c1 = s2.attrs["grid_rows_cols"]
    shape = A["F"].shape
    vf = np.full(shape, np.nan, np.float32)
    gf = np.full(shape, np.nan, np.float32)
    vf[r0:r1, c0:c1] = s2.valid_frac.values
    gf[r0:r1, c0:c1] = s2.gt03_frac.values
    bed = A["reservoir"] & A["inbox"]
    idx = np.flatnonzero(bed.ravel())
    k24 = L.YEARS.index(2024)
    y24 = L.load_outcomes(idx, years=[2024])[:, 0]
    W = R1["water_annual"][k24].ravel()[idx]
    land = np.isfinite(W) & (W < 10)
    s2ok = np.nan_to_num(vf.ravel()[idx]) >= 0.5
    same = land & np.isfinite(y24) & s2ok
    modis_km2 = float(np.sum(y24[same] > 0.3) * RES_KM2)
    s2_km2 = float(np.nansum(gf.ravel()[idx][same]) * RES_KM2)
    return {"bed_pixels": int(bed.sum()), "same_pixels": int(same.sum()), "same_pixels_km2": float(same.sum() * RES_KM2),
            "modis_km2_ndvi_gt_0_3": modis_km2, "sentinel2_km2_ndvi_gt_0_3": s2_km2,
            "ratio_s2_to_modis": s2_km2 / modis_km2 if modis_km2 > 0 else None,
            "s2_scenes": int(s2.attrs.get("scenes", 0)),
            "note": "MODIS: July–October mean NDVI 2024, land pixel-years (water share < 10 %); Sentinel-2: August "
                    "2024 median NDVI per 23 m cell; both on the same bed pixels with S2 coverage >= 50 %"}


def changes(idx, R1):
    """Change per pixel: mean(2023, 2024) - mean(2016–2018), R5 water rule applied."""
    Y = R1H1.water_rule(L.load_outcomes(idx), R1, idx)
    b, p = np.isin(YRS, R2L.BASE), np.isin(YRS, L.POST)
    with np.errstate(invalid="ignore"):
        return np.nanmean(Y[:, p], 1) - np.nanmean(Y[:, b], 1)


def main():
    if "--skip-check" not in sys.argv:
        R2L.check_addendum()
    A = L.layers()
    R1 = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    R2 = dict(np.load(f"{L.D}/derived/r2_layers.npz"))
    names = json.load(open(f"{L.D}/derived/layers_meta.json"))["oblast_names"]
    out = {"label": "registered revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md)", "H3_check_R12": h3_check(A, R1)}
    print("R12", out["H3_check_R12"], flush=True)

    # ---- H4 categories
    h2p = f"{OUT}/r2_h2_results.json"
    h2 = json.load(open(h2p)) if os.path.exists(h2p) else {}
    co = h2.get("main", {}).get("coefs")
    if co:
        g = {"P": co["Pc"], "T": co["Tc"], "P_irr": co["Pc"] + co["Pc_x_I"], "T_irr": co["Tc"] + co["Tc_x_I"]}
        out["weather_adjustment"] = {"source": "R9 main model coefficients (per 100 mm, per °C)", **g}
    else:
        g = None
        out["weather_adjustment"] = "none (R9 model not available)"
    kh = names.index("Kherson") + 1
    base = A["universe"] & (A["oblast"] == kh)
    crop = R2["crop_r2"] & R2["covered"]
    irr = crop & (R2["irr_mean_1921"] >= 0.5)
    never = crop & (R2["irr_max_1921"] < 0.05)
    cats = {"flooded (F)": base & A["F"],
            "former reservoir bed": A["reservoir"] & (A["oblast"] == kh) & A["inbox"],
            "R9 irrigated cropland": base & irr & ~A["F"],
            "R9 never-irrigated cropland": base & never & ~A["F"],
            "other cropland": base & R2["crop_r2"] & ~irr & ~never & ~A["F"]}
    used = np.zeros(A["F"].shape, bool)
    for m in cats.values():
        used |= m
    cats["all other land"] = base & ~used
    steppe = np.isin(A["oblast"], [names.index(n) + 1 for n in STEPPE])
    oarea = A["universe"] & steppe & (A["dist_res"] > 30) & (A["dist_net"] > 30) & ~A["any_june"] \
        & ~(R2["two_oblasts"] & (R2["dist_field_km"] <= 5))
    ocrop = oarea & R2["crop_r2"]

    def pix(mask, irrigated=False):
        i = np.flatnonzero(mask.ravel())
        d = changes(i, R1)
        if g is not None:
            P, T = L.weather(A["lon"].ravel()[i], A["lat"].ravel()[i])
            b, p = np.isin(YRS, R2L.BASE), np.isin(YRS, L.POST)
            dP = (P[:, p].mean(1) - P[:, b].mean(1)) / 100.0
            dT = T[:, p].mean(1) - T[:, b].mean(1)
            gp, gt = (g["P_irr"], g["T_irr"]) if irrigated else (g["P"], g["T"])
            d = d - (gp * dP + gt * dT)
        ok = np.isfinite(d)
        return d[ok], A["block"].ravel()[i][ok], A["dom"].ravel()[i][ok], int(mask.sum())

    data = {n: pix(m, irrigated=(n == "R9 irrigated cropland")) for n, m in cats.items()}
    oc_d, oc_b, _, _ = pix(ocrop)
    oa_d, oa_b, oa_dom, _ = pix(oarea)
    tot = sum(v[3] for v in data.values())

    rng = np.random.default_rng(20261016)
    NB = int(A["block"].max()) + 1

    def sums(d, b):
        return np.bincount(b, weights=d, minlength=NB), np.bincount(b, minlength=NB).astype(float)

    def mean_of(sn, mult):
        s_, n_ = sn
        if mult is None:
            return float(s_.sum() / n_.sum()) if n_.sum() else float("nan")
        den = mult @ n_
        return float((mult @ s_) / den) if den else float("nan")

    S_cat = {n: sums(v[0], v[1]) for n, v in data.items()}
    S_oc = sums(oc_d, oc_b)
    S_cls = {int(c): sums(oa_d[oa_dom == c], oa_b[oa_dom == c]) for c in np.unique(oa_dom)}

    def decomposition(km=None, om=None):
        oref_crop = mean_of(S_oc, om)
        oref_cls = {c: mean_of(v, om) for c, v in S_cls.items()}
        res = {}
        for n, (d, b, dom, npx) in data.items():
            mean = mean_of(S_cat[n], km)
            if n == "former reservoir bed":
                ref = 0.0
            elif "cropland" in n:
                ref = oref_crop
            else:
                cls, cnt = np.unique(dom, return_counts=True)
                ref = float(sum(np.nan_to_num(oref_cls.get(int(c), 0.0)) * k for c, k in zip(cls, cnt)) / max(cnt.sum(), 1))
            rel = mean - ref
            res[n] = {"mean_change": mean, "reference_change": ref, "relative_change": rel,
                      "contribution": npx / tot * rel if np.isfinite(rel) else 0.0}   # empty category -> 0
        return res

    point = decomposition()
    kb_all = np.unique(np.concatenate([v[1] for v in data.values()]))
    ob_all = np.unique(np.concatenate([oc_b, oa_b]))
    draws = {n: [] for n in point}
    total = []
    for _ in range(B_DRAWS):
        km = np.bincount(rng.choice(kb_all, len(kb_all), replace=True), minlength=NB).astype(float)
        om = np.bincount(rng.choice(ob_all, len(ob_all), replace=True), minlength=NB).astype(float)
        r = decomposition(km, om)
        for n in r:
            draws[n].append(r[n]["contribution"])
        total.append(sum(v["contribution"] for v in r.values()))
    cats_out = {}
    for n, v in point.items():
        lo, hi = np.nanpercentile(draws[n], [2.5, 97.5])
        cats_out[n] = {**v, "pixels": data[n][3], "pixels_valid": int(len(data[n][0])),
                       "note": "no valid pixels (e.g. open water before the breach); contribution set to 0"
                       if len(data[n][0]) == 0 else "",
                       "area_share": data[n][3] / tot, "contribution_ci95": [float(lo), float(hi)]}
    lo, hi = np.nanpercentile(total, [2.5, 97.5])
    ic = cats_out["R9 irrigated cropland"]["contribution_ci95"]
    out["H4_decomposition_Kherson"] = {
        "categories": cats_out, "sum_of_contributions": float(sum(v["contribution"] for v in point.values())),
        "sum_ci95": [float(lo), float(hi)], "bootstrap": {"draws": B_DRAWS, "blocks": "10 km", "kherson_blocks": int(len(kb_all)),
                                                           "zoneO_blocks": int(len(ob_all)), "area_shares": "fixed"},
        "descriptive_only": bool(ic[0] <= 0 <= ic[1])}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/r2_h3_h4_results.json", "w"), indent=1)
    print(json.dumps(out, indent=1)[:4000])


if __name__ == "__main__":
    main()
