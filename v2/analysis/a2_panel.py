"""A2 — pixel sets and annual outcome panels for H1 (flood) and H2 (irrigation).

Implements plan §4.1, §4.3 and §5 on top of A1's layers. Output:
  data/v2/derived/h1_pixels.npz   flooded + candidate control pixels, outcomes, weather
  data/v2/derived/h2_pixels.npz   zone K + zone O cropland pixels, outcomes, weather, Jul–Aug NDVI 2017–2021
"""
import json
import sys
import os

import numpy as np
from scipy import ndimage as ndi

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

OUT = f"{L.D}/derived"


def outcomes(idx):
    o = {
        "ndvi_jo": L.load_outcomes(idx, "ndvi_jo", "n_jo"),
        "evi_jo": L.load_outcomes(idx, "evi_jo", "n_jo"),
        "ndvi_ja": L.load_outcomes(idx, "ndvi_ja", "n_ja", min_obs=2),
        "ndvi_ao": L.load_outcomes(idx, "ndvi_ao", "n_ao", min_obs=8),
        "ndvi_ao_p90": L.load_outcomes(idx, "ndvi_ao_p90", "n_ao", min_obs=8),
    }
    return o


def main():
    A = L.layers()
    shape = A["F"].shape
    res = 231.656358
    built_px = A["built"] >= 50
    dist_built = ndi.distance_transform_edt(~built_px) * res / 1000
    rr, cc = np.indices(shape)
    X = (A["lon"] * 0).astype(np.float64)  # placeholder to keep memory small
    del X
    meta = {}

    # ---------------- H1 ----------------
    base = A["universe"] & (A["bank"] > 0)
    F = base & A["F"]
    F25 = base & A["universe"] & (A["flood"] >= 0.25) & (A["water"] < 20)   # robustness: 25% threshold
    cand = base & ~A["any_june"] & (A["water"] < 20) & ~A["reservoir"] & ~A["channel"]
    C15 = cand & (A["distF"] >= 2) & (A["distF"] <= 15)
    C25 = cand & (A["distF"] >= 5) & (A["distF"] <= 25)
    keep = F | F25 | C15 | C25
    idx = np.flatnonzero(keep.ravel())
    o = outcomes(idx)
    P, T = L.weather(A["lon"].ravel()[idx], A["lat"].ravel()[idx])
    np.savez_compressed(
        f"{OUT}/h1_pixels.npz", idx=idx, F=F.ravel()[idx], F25=F25.ravel()[idx], C15=C15.ravel()[idx], C25=C25.ravel()[idx],
        bank=A["bank"].ravel()[idx], dom=A["dom"].ravel()[idx], pure=A["pure"].ravel()[idx],
        flood=A["flood"].ravel()[idx], distF=A["distF"].ravel()[idx], dist_built=dist_built.ravel()[idx],
        block=A["block"].ravel()[idx], row=rr.ravel()[idx], col=cc.ravel()[idx],
        lon=A["lon"].ravel()[idx], lat=A["lat"].ravel()[idx], P=P, T=T, **o)
    nvalid = np.isfinite(o["ndvi_jo"]).sum(1)
    meta["h1"] = {"F_px": int(F.sum()), "C15_px": int(C15.sum()), "C25_px": int(C25.sum()),
                  "F_fixed_panel": int(((nvalid >= L.MIN_YEARS) & F.ravel()[idx]).sum()),
                  "C15_fixed_panel": int(((nvalid >= L.MIN_YEARS) & C15.ravel()[idx]).sum())}

    # ---------------- H2 ----------------
    keep2 = A["zoneK"] | A["zoneO"]
    idx2 = np.flatnonzero(keep2.ravel())
    ja_pre = L.load_outcomes(idx2, "ndvi_ja", "n_ja", min_obs=2, years=[2017, 2018, 2019, 2020, 2021])
    o2 = outcomes(idx2)
    P2, T2 = L.weather(A["lon"].ravel()[idx2], A["lat"].ravel()[idx2])
    np.savez_compressed(
        f"{OUT}/h2_pixels.npz", idx=idx2, K=A["zoneK"].ravel()[idx2], O=A["zoneO"].ravel()[idx2],
        oblast=A["oblast"].ravel()[idx2], dist_built=dist_built.ravel()[idx2], block=A["block"].ravel()[idx2],
        row=rr.ravel()[idx2], col=cc.ravel()[idx2], lon=A["lon"].ravel()[idx2], lat=A["lat"].ravel()[idx2],
        dist_net=A["dist_net"].ravel()[idx2], dist_res=A["dist_res"].ravel()[idx2],
        ja_pre=ja_pre, P=P2, T=T2, **o2)
    meta["h2"] = {"K_px": int(A["zoneK"].sum()), "O_px": int(A["zoneO"].sum())}
    with open(f"{OUT}/panel_meta.json", "w") as fh:
        json.dump(meta, fh, indent=1)
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
