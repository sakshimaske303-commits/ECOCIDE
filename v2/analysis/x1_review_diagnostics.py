"""X1 — review diagnostics (EXPLORATORY; not part of either registered plan).

Written on 16 October 2026, after the pre-registered and the registered-revision
results were known, in response to an external review. It does not change any
registered estimate or verdict. It quantifies two problems with interpreting
H2 (irrigation) and H4 (decomposition):

  D1  July–October rainfall and mean temperature in the Kakhovka canal zone
      (zone K) and in the steppe comparison zone of the revision (zone O, R2),
      2016–2024, from the same ERA5-Land cells the models use (v2lib.weather).
  D2  How closely the H2 event-study coefficients for 2016–2021 follow zone-K
      rainfall (Pearson r), and the 2022–2024 values that a straight line fitted
      to 2016–2021 would give. Illustrative only: six points, and 2023 lies
      outside the 2016–2021 rainfall range.
  D3  For each placebo district of the revision (R3): the share of its cropland
      that lies in zone K and the median distance from its zone-O cropland to
      the Kakhovka canal network; and the randomization p recomputed without the
      districts that adjoin the network.

Needs data/v2/derived/layers.npz and r1_layers.npz (run v2/analysis/run_all.py
and run_revision.py first).

    python v2/analysis/x1_review_diagnostics.py

Output: outputs/v2/x1_review_diagnostics.json
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2lib as L  # noqa: E402

OUT = "outputs/v2"
ADJ_SHARE_K = 0.01      # district counted as adjoining the network if >= 1 % of its cropland is in zone K
ADJ_MEDIAN_KM = 20.0    # ... or if its zone-O cropland lies a median <= 20 km from the network


def zone_weather(mask, A):
    """Pixel-mean July–October rainfall (mm) and temperature (°C) per year over a mask."""
    i = np.flatnonzero(mask.ravel())
    P, T = L.weather(A["lon"].ravel()[i], A["lat"].ravel()[i])
    return {y: {"precip_mm": float(P[:, k].mean()), "temp_c": float(T[:, k].mean())}
            for k, y in enumerate(L.YEARS)}


def rain_fit(coefs, rain):
    """Pearson r of event-study coefficients (2021 = 0) with rainfall over 2016–2021,
    and the 2022–2024 values implied by a straight-line fit (illustrative)."""
    pre = [2016, 2017, 2018, 2019, 2020, 2021]
    x = np.array([rain[y] for y in pre])
    yv = np.array([0.0 if y == 2021 else coefs[y] for y in pre])
    slope, icept = np.polyfit(x, yv, 1)
    out = {"pearson_r_2016_2021": float(np.corrcoef(x, yv)[0, 1]),
           "slope_per_100mm": float(slope * 100),
           "rain_range_2016_2021_mm": [float(x.min()), float(x.max())],
           "post": {}}
    for y in (2022, 2023, 2024):
        pred = float(icept + slope * rain[y])
        out["post"][str(y)] = {"rain_mm": float(rain[y]), "observed": float(coefs[y]),
                               "line_fit_value": pred, "observed_minus_fit": float(coefs[y] - pred)}
    return out


def main():
    A = L.layers()
    R = dict(np.load(f"{L.D}/derived/r1_layers.npz"))
    rmeta = json.load(open(f"{L.D}/derived/r1_meta.json"))
    raion_names = rmeta["raion_names"]
    zK, zO2 = A["zoneK"], R["zoneO_r2"]
    out = {"label": "exploratory review diagnostics (not registered; written after all registered results were known)"}

    # D1 weather
    wK, wO = zone_weather(zK, A), zone_weather(zO2, A)
    out["D1_weather_jul_oct"] = {"zone_K": wK, "zone_O_revision": wO,
                                 "wettest_year_zone_K": int(max(wK, key=lambda y: wK[y]["precip_mm"])),
                                 "driest_year_zone_K": int(min(wK, key=lambda y: wK[y]["precip_mm"]))}
    rain = {y: wK[y]["precip_mm"] for y in L.YEARS}

    # D2 event studies vs rainfall
    d2 = {}
    for name, f in (("preregistered", "h2_results.json"), ("revision", "r1_h2_results.json")):
        es = json.load(open(f"{OUT}/{f}"))["event_study"]["coefs"]
        coefs = {r["year"]: r["coef"] for r in es}
        d2[name] = rain_fit(coefs, rain)
    out["D2_h2_event_study_vs_zoneK_rain"] = d2

    # D3 placebo districts of the revision
    r1h2 = json.load(open(f"{OUT}/r1_h2_results.json"))
    b0 = r1h2["main"]["beta"]
    crop = A["universe"] & (A["crop"] >= 60)
    rows, keep = {}, []
    for name, v in r1h2["placebo_raions"]["units"].items():
        rid = raion_names.index(name) + 1
        m = R["raion"] == rid
        ncrop = int((crop & m).sum())
        share_k = float((zK & m).sum() / ncrop) if ncrop else float("nan")
        d = A["dist_net"][zO2 & m]
        med = float(np.median(d)) if d.size else float("nan")
        adj = bool(share_k >= ADJ_SHARE_K or med <= ADJ_MEDIAN_KM)
        rows[name] = {"beta": v["beta"], "cropland_px": ncrop, "share_cropland_in_zone_K": share_k,
                      "median_km_zoneO_to_network": med, "adjoins_network": adj}
        if not adj:
            keep.append(v["beta"])
    out["D3_placebo_districts"] = {
        "rule_adjoining": f"share of cropland in zone K >= {ADJ_SHARE_K:.0%} or median zone-O distance to network <= {ADJ_MEDIAN_KM:g} km",
        "units": rows,
        "beta_real": b0,
        "p_one_sided_all": r1h2["placebo_raions"]["p_randomization_one_sided"],
        "n_placebos_not_adjoining": len(keep),
        "p_one_sided_not_adjoining": (1 + sum(x <= b0 for x in keep)) / (1 + len(keep)),
    }
    os.makedirs(OUT, exist_ok=True)
    json.dump(out, open(f"{OUT}/x1_review_diagnostics.json", "w"), indent=1)

    print("Zone K July–October rainfall (mm):", {y: round(rain[y]) for y in L.YEARS})
    for k, v in d2.items():
        print(f"H2 {k}: r = {v['pearson_r_2016_2021']:+.2f};",
              {y: (round(p['observed'], 3), round(p['line_fit_value'], 3)) for y, p in v["post"].items()})
    for k, v in sorted(rows.items(), key=lambda kv: kv[1]["beta"]):
        print(f"  {k:40s} beta={v['beta']:+.3f} inK={v['share_cropland_in_zone_K']:.0%} "
              f"median={v['median_km_zoneO_to_network']:.1f} km adjoining={v['adjoins_network']}")
    D3 = out["D3_placebo_districts"]
    print("RI p all:", round(D3["p_one_sided_all"], 3), " without adjoining districts:",
          round(D3["p_one_sided_not_adjoining"], 3), f"({D3['n_placebos_not_adjoining']} placebos)")


if __name__ == "__main__":
    main()
