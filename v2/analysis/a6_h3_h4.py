"""A6 — H3 (reservoir bed, descriptive) and H4 (decomposition, descriptive); plan §2, §4.2, §9.

Output: outputs/v2/h3_h4_results.json
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402
import a4_h2 as H2  # noqa: E402

OUT = "outputs/v2"
RES_KM2 = (231.656358 / 1000) ** 2


def main():
    A = L.layers()
    names = json.load(open(f"{L.D}/derived/layers_meta.json"))["oblast_names"]
    kh = names.index("Kherson") + 1
    R = {}

    # ---------------- H3: former reservoir bed ----------------
    rb = A["reservoir"] & A["inbox"]
    idx = np.flatnonzero(rb.ravel())
    Y = L.load_outcomes(idx)                                   # Jul–Oct mean NDVI, ≥5 obs
    Yja = L.load_outcomes(idx, "ndvi_ja", "n_ja", min_obs=2)
    rows = []
    for k, y in enumerate(L.YEARS):
        v = Y[:, k]
        ok = np.isfinite(v)
        rows.append({"year": y, "pixels_with_valid_outcome": int(ok.sum()),
                     "mean_ndvi_jul_oct": float(np.nanmean(v)) if ok.any() else None,
                     "median_ndvi_jul_oct": float(np.nanmedian(v)) if ok.any() else None,
                     "share_ndvi_gt_0_3": float(np.nanmean(v[ok] > 0.3)) if ok.any() else None,
                     "share_ndvi_gt_0_5": float(np.nanmean(v[ok] > 0.5)) if ok.any() else None,
                     "area_km2_ndvi_gt_0_3": float(np.sum(v[ok] > 0.3) * RES_KM2),
                     "mean_ndvi_jul_aug": float(np.nanmean(Yja[:, k])) if np.isfinite(Yja[:, k]).any() else None})
    R["H3_reservoir_bed"] = {"pixels": int(rb.sum()), "area_km2": float(rb.sum() * RES_KM2), "by_year": rows,
                             "note": "WorldCover 2021 water >= 50 % pixels of the Kakhovka reservoir; no counterfactual (descriptive)."}

    # ---------------- H4: decomposition of Kherson Oblast 2021 -> 2024 ----------------
    base = A["universe"] & (A["oblast"] == kh)
    Hh = H2.load()
    irr, rain = H2.classify(Hh)
    # map H2 classification back to the grid
    irr_g = np.zeros(A["F"].size, bool)
    rain_g = np.zeros(A["F"].size, bool)
    irr_g[np.asarray(Hh["idx"])] = irr
    rain_g[np.asarray(Hh["idx"])] = rain
    irr_g, rain_g = irr_g.reshape(A["F"].shape), rain_g.reshape(A["F"].shape)
    Kz = A["zoneK"]
    cats = {
        "flooded (F)": base & A["F"],
        "former reservoir bed": A["reservoir"] & (A["oblast"] == kh) & A["inbox"],
        "Kakhovka zone, irrigated cropland": base & Kz & irr_g & ~A["F"],
        "Kakhovka zone, rainfed cropland": base & Kz & rain_g & ~A["F"],
    }
    used = np.zeros(A["F"].shape, bool)
    for m in cats.values():
        used |= m
    cats["all other land"] = base & ~used
    total_mask = used | cats["all other land"]
    Ototal = A["zoneO"]
    y0, y1 = L.YEARS.index(2021), L.YEARS.index(2024)

    def change(mask):
        i = np.flatnonzero(mask.ravel())
        Yc = L.load_outcomes(i, years=[2021, 2024])
        ok = np.isfinite(Yc).all(1)
        return (float(np.mean(Yc[ok, 1] - Yc[ok, 0])) if ok.any() else np.nan), int(ok.sum()), Yc

    # O reference changes: by dominant class, and irrigated / rainfed
    dom = A["dom"]
    Oref_class = {}
    for c in np.unique(dom[Ototal]):
        Oref_class[int(c)] = change(Ototal & (dom == c))[0]
    Oref_irr = change(Ototal & irr_g)[0]
    Oref_rain = change(Ototal & rain_g)[0]
    tot_px = int(total_mask.sum())
    dec = {}
    whole_change, whole_n, _ = change(total_mask)
    for name, m in cats.items():
        d, n, Yc = change(m)
        share = m.sum() / tot_px
        if name == "former reservoir bed":
            ref = 0.0
            ref_note = "no zone-O analogue (open water in 2021): raw change"
        elif "irrigated" in name:
            ref, ref_note = Oref_irr, "zone O irrigated cropland"
        elif "rainfed" in name:
            ref, ref_note = Oref_rain, "zone O rainfed cropland"
        else:
            # pixel-weighted average of zone-O change for the same dominant classes
            dm = dom[m]
            cls, cnt = np.unique(dm, return_counts=True)
            ref = float(sum(Oref_class.get(int(c), 0.0) * k for c, k in zip(cls, cnt)) / cnt.sum())
            ref_note = "zone O, same dominant WorldCover class mix"
        dec[name] = {"pixels": int(m.sum()), "area_share": float(share), "mean_change_2021_2024": d,
                     "zoneO_reference_change": ref, "relative_change": d - ref,
                     "contribution_to_oblast_relative_change": float(share * (d - ref)), "reference": ref_note,
                     "pixels_valid_both_years": n}
    R["H4_decomposition_Kherson"] = {
        "oblast_mean_change_2021_2024_all_valid_pixels": whole_change,
        "categories": dec,
        "sum_of_contributions": float(sum(v["contribution_to_oblast_relative_change"] for v in dec.values())),
        "note": "Area-weighted; each category's 2021->2024 change minus the same-class change in zone O. Descriptive.",
    }
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/h3_h4_results.json", "w") as fh:
        json.dump(R, fh, indent=1)
    print(json.dumps(R, indent=1)[:6000])


if __name__ == "__main__":
    main()
