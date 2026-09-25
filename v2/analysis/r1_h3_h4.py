"""R1-H3/H4 — Registered Revision 1 (Addendum R5) for the descriptive hypotheses.

H3: reservoir-bed statistics on pixel-years whose annual water share is below 10 % ("land"),
    2017–2024 (years with water data), plus the land area per year.
H4: the 2021 -> 2024 decomposition with the R5 water rule applied, and irrigated / rainfed
    status from R1 (2010–2015) with the restricted comparison zone (R2).
Output: outputs/v2/r1_h3_h4_results.json
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

OUT = "outputs/v2"
RES_KM2 = (231.656358 / 1000) ** 2


def main():
    A = L.layers()
    R = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    rmeta = json.load(open(f"{L.D}/derived/r1_meta.json"))
    names = json.load(open(f"{L.D}/derived/layers_meta.json"))["oblast_names"]
    out = {"label": "registered revision (Addendum 1)", "water_years_used": rmeta["water_years_used"]}

    # H3
    rb = A["reservoir"] & A["inbox"]
    idx = np.flatnonzero(rb.ravel())
    Y = L.load_outcomes(idx)
    rows = []
    for k, y in enumerate(L.YEARS):
        W = R["water_annual"][k].ravel()[idx]
        if not np.isfinite(W).any():
            continue
        land = W < 10
        v = Y[:, k]
        ok = land & np.isfinite(v)
        rows.append({"year": y, "water_map_year": rmeta["water_years_used"].get(str(y)),
                     "land_pixels": int(land.sum()), "land_km2": float(land.sum() * RES_KM2),
                     "land_pixels_with_outcome": int(ok.sum()),
                     "mean_ndvi_jul_oct_land": float(np.nanmean(v[ok])) if ok.any() else None,
                     "share_land_ndvi_gt_0_3": float(np.mean(v[ok] > 0.3)) if ok.any() else None,
                     "km2_land_ndvi_gt_0_3": float(np.sum(v[ok] > 0.3) * RES_KM2)})
    out["H3_reservoir_bed_land_only"] = rows

    # H4
    kh = names.index("Kherson") + 1
    base = A["universe"] & (A["oblast"] == kh)
    irr, rain = R["irr_r1"], R["rain_r1"]
    Kz, O2 = A["zoneK"], R["zoneO_r2"]
    cats = {"flooded (F)": base & A["F"],
            "former reservoir bed": A["reservoir"] & (A["oblast"] == kh) & A["inbox"],
            "Kakhovka zone, irrigated cropland": base & Kz & irr & ~A["F"],
            "Kakhovka zone, rainfed cropland": base & Kz & rain & ~A["F"]}
    used = np.zeros(A["F"].shape, bool)
    for m in cats.values():
        used |= m
    cats["all other land"] = base & ~used
    k21, k24 = L.YEARS.index(2021), L.YEARS.index(2024)

    def change(mask):
        i = np.flatnonzero(mask.ravel())
        Yc = L.load_outcomes(i, years=[2021, 2024])
        for col, k in ((0, k21), (1, k24)):
            W = R["water_annual"][k].ravel()[i]
            W21 = R["water_annual"][k21].ravel()[i]
            bad = np.isfinite(W) & ((W > 10) | (np.abs(W - W21) > 10))
            Yc[bad, col] = np.nan
        ok = np.isfinite(Yc).all(1)
        return (float(np.mean(Yc[ok, 1] - Yc[ok, 0])) if ok.any() else float("nan")), int(ok.sum())

    dom = A["dom"]
    Oref_class = {int(c): change(O2 & (dom == c))[0] for c in np.unique(dom[O2])}
    Oref_irr, Oref_rain = change(O2 & irr)[0], change(O2 & rain)[0]
    tot = int((used | cats["all other land"]).sum())
    dec = {}
    for name, m in cats.items():
        d, n = change(m)
        if name == "former reservoir bed":
            ref, note = 0.0, "no zone-O analogue: raw change (land pixel-years only)"
        elif "irrigated" in name:
            ref, note = Oref_irr, "restricted zone O, irrigated (R1)"
        elif "rainfed" in name:
            ref, note = Oref_rain, "restricted zone O, rainfed (R1)"
        else:
            cls, cnt = np.unique(dom[m], return_counts=True)
            ref = float(sum(Oref_class.get(int(c), 0.0) * k for c, k in zip(cls, cnt)) / cnt.sum())
            note = "restricted zone O, same dominant-class mix"
        rel = d - ref if np.isfinite(d) else float("nan")
        dec[name] = {"pixels": int(m.sum()), "area_share": float(m.sum() / tot), "mean_change_2021_2024": d,
                     "zoneO_reference_change": ref, "relative_change": rel,
                     "contribution": float(m.sum() / tot * rel) if np.isfinite(rel) else None,
                     "pixels_valid_both_years": n, "reference": note}
    out["H4_decomposition_Kherson"] = {"categories": dec,
                                       "sum_of_contributions": float(sum(v["contribution"] or 0 for v in dec.values()))}
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/r1_h3_h4_results.json", "w"), indent=1)
    print(json.dumps(out, indent=1)[:5000])


if __name__ == "__main__":
    main()
