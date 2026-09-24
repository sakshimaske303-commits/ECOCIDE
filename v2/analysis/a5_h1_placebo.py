"""A5 — H1 randomization inference with placebo floodplains (plan §4.4, §6).

Floodplain pixels within 3 km of permanent river water along
  * the Southern Buh upstream of Mykolaiv,
  * the lower Dniester,
  * the Dnipro upstream of the Kakhovka reservoir (above the Zaporizhzhia dam),
are cut into 10 km river segments. Each segment is treated as if flooded and
analysed with exactly the H1 pipeline (matched, controls 2–15 km away on the
same side of the river, same model). Output: outputs/v2/h1_placebo.json
"""
import json
import os
import sys
import time

import numpy as np
from pyproj import Transformer
from scipy import ndimage as ndi
from skimage.graph import route_through_array

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grid  # noqa: E402
import v2lib as L  # noqa: E402
import a3_h1 as H1  # noqa: E402

RES = grid.RES
OUT = "outputs/v2"
RIVERS = {  # downstream end -> upstream end (lon, lat)
    "Southern Buh": [(31.99, 47.00), (31.33, 47.57), (30.85, 48.05), (29.25, 48.67)],
    "Lower Dniester": [(30.25, 46.40), (29.95, 46.60), (29.62, 46.84)],
    "Dnipro above Zaporizhzhia": [(35.09, 47.89), (35.05, 48.45), (34.62, 48.52), (33.45, 49.07)],
}
SEG_KM = 10.0
FP_KM = 3.0


def rc_of(lon, lat, tr0, tr1):
    x, y = Transformer.from_crs(4326, grid.CRS, always_xy=True).transform(lon, lat)
    return int((tr1 - y) // RES), int((x - tr0) // RES)


def trace(water, pts, tr0, tr1):
    riv = water >= 50
    cost = np.where(water >= 50, 1.0, np.where(water >= 20, 4.0, np.where(water >= 5, 20.0, 200.0)))
    path = []
    snapped = []
    _, (ir, ic) = ndi.distance_transform_edt(~(water >= 30), return_indices=True)
    for lon, lat in pts:
        r, c = rc_of(lon, lat, tr0, tr1)
        snapped.append((int(ir[r, c]), int(ic[r, c])))
    for a, b in zip(snapped[:-1], snapped[1:]):
        p, _ = route_through_array(cost, a, b, fully_connected=True, geometric=True)
        path += p if not path else p[1:]
    del riv
    return np.array(path)


def main():
    t0 = time.time()
    A = L.layers()
    shape = A["F"].shape
    tr = json.load(open(f"{L.D}/derived/layers_meta.json"))["transform"]
    tr0, tr1 = tr[2], tr[5]
    water = A["water"].astype(np.float32)
    units = []  # (river, segment id, treated mask, side mask array)
    lab_all = np.zeros(shape, np.int32)
    side_all = np.zeros(shape, np.int8)
    seg_meta = {}
    uid = 0
    for river, pts in RIVERS.items():
        path = trace(water, pts, tr0, tr1)
        line = np.zeros(shape, bool)
        line[path[:, 0], path[:, 1]] = True
        # permanent river water: water >= 50 % pixels connected to the traced line, plus the line
        lab, _ = ndi.label((water >= 50) | line)
        ids = np.unique(lab[line])
        rw = np.isin(lab, ids[ids > 0]) & ((water >= 50) | line)
        # keep river water close to the line (avoid attaching distant lakes)
        dline = ndi.distance_transform_edt(~line) * RES / 1000
        rw &= dline <= 5
        drw = ndi.distance_transform_edt(~rw) * RES / 1000
        # along-river distance of each line pixel, and local direction
        steps = np.r_[0, np.cumsum(np.hypot(*np.diff(path, axis=0).T))] * RES / 1000
        seg_of_line = (steps // SEG_KM).astype(int)
        _, (ir, ic) = ndi.distance_transform_edt(~line, return_indices=True)
        pos = {(r, c): i for i, (r, c) in enumerate(path)}
        near_i = np.vectorize(lambda r, c: pos.get((r, c), -1), otypes=[int])
        # side of the river: sign of the cross product with the local downstream->upstream direction
        k = 5
        dirs = np.zeros((len(path), 2))
        for i in range(len(path)):
            a, b = path[max(i - k, 0)], path[min(i + k, len(path) - 1)]
            dirs[i] = b - a
        box = (drw <= 20)
        rr, cc = np.nonzero(box)
        ni = near_i(ir[rr, cc], ic[rr, cc])
        good = ni >= 0
        rr, cc, ni = rr[good], cc[good], ni[good]
        vr, vc = rr - path[ni, 0], cc - path[ni, 1]
        cross = dirs[ni, 0] * vc - dirs[ni, 1] * vr
        side = np.where(cross >= 0, 1, 2).astype(np.int8)
        segs = seg_of_line[ni]
        fp = A["universe"][rr, cc] & (drw[rr, cc] <= FP_KM) & (water[rr, cc] < 20) & ~A["any_june"][rr, cc] \
            & ~A["reservoir"][rr, cc]
        n_seg = seg_of_line.max() + 1
        for s in range(n_seg):
            for sd in (1, 2):
                tmask = fp & (segs == s) & (side == sd)
                if tmask.sum() < 50:
                    continue
                uid += 1
                lab_all[rr[tmask], cc[tmask]] = uid
                seg_meta[uid] = {"river": river, "segment": int(s), "side": int(sd), "treated_px": int(tmask.sum())}
        side_all[rr, cc] = np.where(side_all[rr, cc] == 0, side, side_all[rr, cc])
        # store floodplain mask (excluded from controls) and side per river
        seg_meta.setdefault("_rivers", {})[river] = {"path_km": float(steps[-1]), "segments": int(n_seg)}
        A[f"fp_{river}"] = (drw <= FP_KM)
        A[f"side_{river}"] = np.zeros(shape, np.int8)
        A[f"side_{river}"][rr, cc] = side
    print("placebo units:", uid, "built in", round(time.time() - t0), "s")

    # controls and panel per unit, then the H1 pipeline
    results = {}
    Yall = np.stack([L.load_outcomes(np.arange(shape[0] * shape[1]), years=[y])[:, 0] for y in L.YEARS], axis=1)
    for u in range(1, uid + 1):
        m = seg_meta[u]
        river = m["river"]
        T = lab_all == u
        dT = ndi.distance_transform_edt(~T) * RES / 1000 if T.any() else None
        C = A["universe"] & (dT >= 2) & (dT <= 15) & (A["water"] < 20) & ~A[f"fp_{river}"] & ~A["reservoir"] \
            & ~A["any_june"] & (A[f"side_{river}"] == m["side"])
        idx = np.flatnonzero((T | C).ravel())
        if (C.sum() < 100):
            results[u] = {**m, "skipped": "fewer than 100 control pixels"}
            continue
        Y = Yall[idx]
        P, Tm = L.weather(A["lon"].ravel()[idx], A["lat"].ravel()[idx])
        rr_, cc_ = np.unravel_index(idx, shape)
        Hp = {"ndvi_jo": Y, "P": P, "T": Tm, "bank": np.full(len(idx), m["side"]), "dom": A["dom"].ravel()[idx],
              "block": A["block"].ravel()[idx], "row": rr_, "col": cc_}
        treat = T.ravel()[idx]
        ctrl = C.ravel()[idx]
        try:
            w, d = H1.match(Hp, treat, ctrl)
            r = H1.estimate(Hp, treat, w) if d["matched_treated"] >= 10 else {"skipped": "fewer than 10 matched treated"}
            ones = (treat | ctrl).astype(float)
            r0 = H1.estimate(Hp, treat, ones)
        except Exception as ex:  # noqa: BLE001
            results[u] = {**m, "error": str(ex)}
            continue
        results[u] = {**m, "matched": {k: r[k] for k in ("beta", "se_cluster", "n_pixels")} if "beta" in r else r,
                      "no_matching": {k: r0[k] for k in ("beta", "se_cluster", "n_pixels")}}
        if u % 10 == 0:
            print(u, river, round(time.time() - t0), "s", flush=True)

    h1 = json.load(open(f"{OUT}/h1_results.json"))
    b_main = h1["main"]["beta"]
    b_nm = h1["robustness"]["1_no_matching"]["beta"]
    pm = [v["matched"]["beta"] for v in results.values() if isinstance(v, dict) and "matched" in v and "beta" in v["matched"]]
    pn = [v["no_matching"]["beta"] for v in results.values() if isinstance(v, dict) and "no_matching" in v]
    out = {
        "units": results, "rivers": seg_meta.get("_rivers"),
        "matched": {"n_placebos": len(pm), "beta_real": b_main,
                    "p_one_sided": (1 + sum(x <= b_main for x in pm)) / (1 + len(pm)),
                    "p_two_sided": (1 + sum(abs(x) >= abs(b_main) for x in pm)) / (1 + len(pm)),
                    "placebo_quantiles": np.quantile(pm, [0.05, 0.5, 0.95]).tolist() if pm else None},
        "no_matching": {"n_placebos": len(pn), "beta_real": b_nm,
                        "p_one_sided": (1 + sum(x <= b_nm for x in pn)) / (1 + len(pn)),
                        "p_two_sided": (1 + sum(abs(x) >= abs(b_nm) for x in pn)) / (1 + len(pn)),
                        "placebo_quantiles": np.quantile(pn, [0.05, 0.5, 0.95]).tolist() if pn else None},
        "seconds": round(time.time() - t0),
    }
    with open(f"{OUT}/h1_placebo.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    np.save(f"{L.D}/derived/placebo_units.npy", lab_all)
    print(json.dumps({k: v for k, v in out.items() if k != "units"}, indent=1, default=str))


if __name__ == "__main__":
    main()
