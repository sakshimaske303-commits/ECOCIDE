"""R2-H1-placebo — randomization inference for the Revision 2 H1 estimate (Addendum 2, R11).

The placebo floodplain segments of a5_h1_placebo.py (same rivers, 10 km segments, sides, controls 2–15 km
away), each analysed with the Revision 1 data rules (band fixed effects by distance to the placebo river,
conflict, water rule) and the R10 covariate matching: relative height above the placebo river line and
WorldCover shares. The unmatched estimate is also computed per unit.
Output: outputs/v2/r2_h1_placebo.json
"""
import json
import os
import sys
import time

import numpy as np
import xarray as xr
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grid  # noqa: E402
import v2lib as L  # noqa: E402
import a5_h1_placebo as A5  # noqa: E402
import r1_h1 as R1H1  # noqa: E402
import r2_h1 as R2H1  # noqa: E402
import r2lib as R2L  # noqa: E402

RES = grid.RES
OUT = "outputs/v2"


def main():
    t0 = time.time()
    if "--skip-check" not in sys.argv:
        R2L.check_addendum()
    A = L.layers()
    R1 = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    R2 = dict(np.load(f"{L.D}/derived/r2_layers.npz"))
    dem = R2["dem"]
    wc = xr.open_dataset(f"{L.D}/worldcover_2021_fractions.nc")
    WC = {c: wc[f"frac_{c}"].values for c in R2H1.WC_COV}
    wc.close()
    shape = A["F"].shape
    tr = json.load(open(f"{L.D}/derived/layers_meta.json"))["transform"]
    tr0, tr1 = tr[2], tr[5]
    water = A["water"].astype(np.float32)
    lab_all = np.zeros(shape, np.int32)
    seg_meta, extra = {}, {}
    uid = 0
    for river, pts in A5.RIVERS.items():          # unit construction exactly as in a5_h1_placebo.py
        path = A5.trace(water, pts, tr0, tr1)
        line = np.zeros(shape, bool)
        line[path[:, 0], path[:, 1]] = True
        lab, _ = ndi.label((water >= 50) | line)
        ids = np.unique(lab[line])
        rw = np.isin(lab, ids[ids > 0]) & ((water >= 50) | line)
        dline = ndi.distance_transform_edt(~line) * RES / 1000
        rw &= dline <= 5
        drw = ndi.distance_transform_edt(~rw) * RES / 1000
        steps = np.r_[0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))] * RES / 1000
        seg_of_line = (steps // A5.SEG_KM).astype(int)
        _, (ir, ic) = ndi.distance_transform_edt(~line, return_indices=True)
        pos = {(r, c): i for i, (r, c) in enumerate(path)}
        near_i = np.vectorize(lambda r, c: pos.get((r, c), -1), otypes=[int])
        k = 5
        dirs = np.zeros((len(path), 2))
        for i in range(len(path)):
            a, b = path[max(i - k, 0)], path[min(i + k, len(path) - 1)]
            dirs[i] = b - a
        rr, cc = np.nonzero(drw <= 20)
        ni = near_i(ir[rr, cc], ic[rr, cc])
        good = ni >= 0
        rr, cc, ni = rr[good], cc[good], ni[good]
        cross = dirs[ni, 0] * (cc - path[ni, 1]) - dirs[ni, 1] * (rr - path[ni, 0])
        side = np.where(cross >= 0, 1, 2).astype(np.int8)
        segs = seg_of_line[ni]
        fp = A["universe"][rr, cc] & (drw[rr, cc] <= A5.FP_KM) & (water[rr, cc] < 20) & ~A["any_june"][rr, cc] \
            & ~A["reservoir"][rr, cc]
        for s in range(seg_of_line.max() + 1):
            for sd in (1, 2):
                tmask = fp & (segs == s) & (side == sd)
                if tmask.sum() < 50:
                    continue
                uid += 1
                lab_all[rr[tmask], cc[tmask]] = uid
                seg_meta[uid] = {"river": river, "segment": int(s), "side": int(sd), "treated_px": int(tmask.sum())}
        sarr = np.zeros(shape, np.int8)
        sarr[rr, cc] = side
        # relative height above the placebo river line (R10 definition)
        ln = line & np.isfinite(dem)
        _, (jr, jc) = ndi.distance_transform_edt(~ln, return_indices=True)
        extra[river] = {"fp": drw <= A5.FP_KM, "side": sarr, "dline": dline.astype(np.float32),
                        "relh": (dem - dem[jr, jc]).astype(np.float32)}
    print("placebo units:", uid, round(time.time() - t0), "s", flush=True)

    Yall = np.stack([L.load_outcomes(np.arange(shape[0] * shape[1]), years=[y])[:, 0] for y in L.YEARS], axis=1)
    results = {}
    for u in range(1, uid + 1):
        m = seg_meta[u]
        ex = extra[m["river"]]
        T = lab_all == u
        dT = ndi.distance_transform_edt(~T) * RES / 1000
        C = A["universe"] & (dT >= 2) & (dT <= 15) & (A["water"] < 20) & ~ex["fp"] & ~A["reservoir"] \
            & ~A["any_june"] & (ex["side"] == m["side"])
        if C.sum() < 100:
            results[u] = {**m, "skipped": "fewer than 100 control pixels"}
            continue
        idx = np.flatnonzero((T | C).ravel())
        P, Tm = L.weather(A["lon"].ravel()[idx], A["lat"].ravel()[idx])
        r_, c_ = np.unravel_index(idx, shape)
        Hp = {"ndvi_jo": R1H1.water_rule(Yall[idx], R1, idx), "P": P, "T": Tm, "bank": np.full(len(idx), m["side"]),
              "dom": A["dom"].ravel()[idx], "block": A["block"].ravel()[idx], "row": r_, "col": c_,
              "band": (ex["dline"].ravel()[idx] // 2).astype(int),
              "CI": np.stack([R1["conflict"][k].ravel()[idx] for k in range(len(L.YEARS))], 1)}
        Z = [ex["relh"].ravel()[idx]]
        for c in R2H1.WC_COV:
            v = WC[c].ravel()[idx].astype(np.float32)
            Z.append(np.where(v == 255, np.nan, v))
        Z = np.column_stack(Z).astype(np.float64)
        treat, ctrl = T.ravel()[idx], C.ravel()[idx]
        try:
            w, d = R2H1.match_on(Z, Hp, treat, ctrl)
            r = R2H1.estimate(Hp, treat, w, full=False) if d["matched_treated"] >= 10 else {"skipped": "fewer than 10 matched"}
            r0 = R2H1.estimate(Hp, treat, (treat | ctrl).astype(float), full=False)
        except Exception as e:  # noqa: BLE001
            results[u] = {**m, "error": str(e)}
            continue
        results[u] = {**m, "matched": {k: r[k] for k in ("beta", "se_cluster", "n_pixels")} if "beta" in r else r,
                      "no_matching": {k: r0[k] for k in ("beta", "se_cluster", "n_pixels")}}
        if u % 10 == 0:
            print(u, m["river"], round(time.time() - t0), "s", flush=True)

    h1 = json.load(open(f"{OUT}/r2_h1_results.json"))
    out = {"units": results}
    pairs = [("no_matching", h1["unmatched"]["beta"])]
    if "beta" in h1.get("matched", {}):
        pairs.append(("matched", h1["matched"]["beta"]))
    for key, real in pairs:
        pb = [v[key]["beta"] for v in results.values() if key in v and "beta" in v[key]]
        out[key] = {"n_placebos": len(pb), "beta_real": real,
                    "p_one_sided": (1 + sum(x <= real for x in pb)) / (1 + len(pb)),
                    "p_two_sided": (1 + sum(abs(x) >= abs(real) for x in pb)) / (1 + len(pb)),
                    "placebo_quantiles": np.quantile(pb, [0.05, 0.5, 0.95]).tolist() if pb else None}
    out["seconds"] = round(time.time() - t0)
    json.dump(out, open(f"{OUT}/r2_h1_placebo.json", "w"), indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != "units"}, indent=1, default=str))


if __name__ == "__main__":
    main()
