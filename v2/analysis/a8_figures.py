"""A8 — Study 2 figures (publication style, 300 dpi) -> outputs/v2/figures/"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import v2lib as L  # noqa: E402
import eco_style as S  # noqa: E402

OUT = "outputs/v2"
FIG = f"{OUT}/figures"
EST = "#C0392B"     # estimate / treated
REF = "#1F77B4"     # placebo / control
GRID = "#7F7F7F"


def event_panel(ax, es, title, color=EST):
    rows = es["coefs"]
    ys = [r["year"] for r in rows] + [2021]
    b = [r["coef"] for r in rows] + [0.0]
    se = [r["se"] for r in rows] + [0.0]
    o = np.argsort(ys)
    ys, b, se = np.array(ys)[o], np.array(b)[o], np.array(se)[o]
    ax.axhline(0, color="#333333", lw=0.8)
    ax.axvspan(2021.5, 2022.5, color="#EEEEEE", zorder=0)
    ax.axvspan(2022.5, 2024.6, color="#FBE9E7", zorder=0)
    ax.errorbar(ys, b, yerr=1.96 * se, fmt="o", color=color, ms=6, lw=2, capsize=0)
    ax.set_xticks(ys)
    ax.set_title(title, loc="left")
    ax.set_ylabel("Difference in Jul–Oct NDVI\n(relative to 2021)")
    ax.text(0.01, 0.03, f"pre-trend joint p = {es['pretrend_joint_p']:.2g}", transform=ax.transAxes, fontsize=8, color="#555555")
    ax.text(2022, ax.get_ylim()[1], "war", ha="center", va="top", fontsize=8, color="#555555")
    ax.text(2023.5, ax.get_ylim()[1], "after breach", ha="center", va="top", fontsize=8, color="#555555")


def main():
    S.apply()
    plt.rcParams["axes.axisbelow"] = True
    os.makedirs(FIG, exist_ok=True)
    h1 = json.load(open(f"{OUT}/h1_results.json"))
    h2 = json.load(open(f"{OUT}/h2_results.json"))
    pl = json.load(open(f"{OUT}/h1_placebo.json"))
    h34 = json.load(open(f"{OUT}/h3_h4_results.json"))

    # 1. exposure map
    A = L.layers()
    img = np.ones(A["F"].shape + (3,), np.float32)
    img[A["ukraine"]] = [0.93, 0.93, 0.93]
    img[A["crimea"]] = [0.85, 0.82, 0.86]
    img[A["zoneO"]] = [0.86, 0.86, 0.78]
    img[A["zoneK"]] = [0.62, 0.80, 0.58]
    img[A["netr"]] = [0.18, 0.45, 0.20]
    img[A["reservoir"]] = [0.27, 0.51, 0.85]
    img[A["F"]] = [0.75, 0.22, 0.17]
    try:
        pu = np.load(f"{L.D}/derived/placebo_units.npy")
        img[pu > 0] = [0.55, 0.35, 0.65]
    except FileNotFoundError:
        pass
    r0, r1, c0, c1 = 300, 2250, 0, 2700
    fig, ax = plt.subplots(figsize=(9, 6.8))
    ax.imshow(img[r0:r1, c0:c1], interpolation="nearest")
    ax.set_axis_off()
    km = 100 / (231.656358 / 1000)
    ax.plot([60, 60 + km], [r1 - r0 - 60] * 2, color="k", lw=3)
    ax.text(60 + km / 2, r1 - r0 - 80, "100 km", ha="center", fontsize=9)
    leg = [Patch(color=(0.75, 0.22, 0.17), label="Flooded 6–9 June 2023 (F, H1)"),
           Patch(color=(0.27, 0.51, 0.85), label="Kakhovka reservoir bed (H3)"),
           Patch(color=(0.62, 0.80, 0.58), label="Kakhovka canal zone, cropland (K, H2)"),
           Patch(color=(0.18, 0.45, 0.20), label="Kakhovka canal network (OSM)"),
           Patch(color=(0.86, 0.86, 0.78), label="Comparison cropland (zone O, H2)"),
           Patch(color=(0.55, 0.35, 0.65), label="Placebo floodplains (H1 inference)"),
           Patch(color=(0.85, 0.82, 0.86), label="Crimea (excluded)")]
    ax.legend(handles=leg, loc="upper left", fontsize=8, frameon=True, framealpha=0.9)
    ax.set_title("Study 2 exposure groups on the 231 m grid (EPSG:3035)", loc="left")
    S.save(fig, f"{FIG}/s2_fig1_exposure_map.png")

    # 2. H1 event studies (pre-registered matched sample; exploratory no-caliper)
    fig, axs = plt.subplots(1, 2, figsize=(11, 4.2), sharey=True)
    event_panel(axs[0], h1["event_study"], f"H1 flood — pre-registered matching\n({h1['matching']['matched_treated']:,} flooded pixels matched)")
    event_panel(axs[1], h1["exploratory"]["matched_no_caliper"]["event_study"],
                f"H1 flood — exploratory, no caliper\n({h1['exploratory']['matched_no_caliper']['matched_treated']:,} flooded pixels)", color=GRID)
    axs[1].set_ylabel("")
    S.save(fig, f"{FIG}/s2_fig2_h1_event_study.png")

    # 3. H2 event study
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    event_panel(ax, h2["event_study"], "H2 irrigation — triple difference\n(irrigated vs rainfed, zone K vs zone O)")
    S.save(fig, f"{FIG}/s2_fig3_h2_event_study.png")

    # 4. randomization inference
    fig, axs = plt.subplots(1, 2, figsize=(12, 3.8), gridspec_kw={"wspace": 0.55})
    pb = [v["matched"]["beta"] for v in pl["units"].values() if isinstance(v, dict) and "matched" in v and "beta" in v["matched"]]
    axs[0].hist(pb, bins=20, color=REF, edgecolor="white")
    axs[0].axvline(h1["main"]["beta"], color=EST, lw=2)
    axs[0].set_title(f"H1: {len(pb)} placebo floodplain segments\nrandomization p = {pl['matched']['p_one_sided']:.2f}", loc="left")
    axs[0].set_xlabel("Estimated effect on Jul–Oct NDVI")
    axs[0].set_ylabel("Placebo units")
    zz = {k: v["beta"] for k, v in h2["placebo_zones"]["units"].items() if "beta" in v}
    names = list(zz) + ["Kakhovka zone (real)"]
    vals = list(zz.values()) + [h2["main"]["beta"]]
    o = np.argsort(vals)
    axs[1].barh(np.array(names)[o], np.array(vals)[o],
                color=[EST if names[i].startswith("Kakhovka") else REF for i in o], height=0.6)
    axs[1].axvline(0, color="#333333", lw=0.8)
    axs[1].set_xlim(min(vals) * 1.15, max(max(vals) * 1.3, 0.01))
    axs[1].set_title(f"H2: placebo zones (oblasts of zone O)\nrandomization p = {h2['placebo_zones']['p_randomization_one_sided']:.2f}", loc="left")
    axs[1].set_xlabel("Estimated effect on Jul–Oct NDVI")
    S.save(fig, f"{FIG}/s2_fig4_randomization_inference.png")

    # 5. H3 reservoir bed
    rows = h34["H3_reservoir_bed"]["by_year"]
    yrs = [r["year"] for r in rows]
    fig, axs = plt.subplots(1, 2, figsize=(11, 3.8))
    axs[0].plot(yrs, [r["mean_ndvi_jul_oct"] for r in rows], "-o", color="#117A65", lw=2, ms=6)
    axs[0].set_title("Former reservoir bed: mean Jul–Oct NDVI", loc="left")
    axs[0].set_ylabel("NDVI")
    axs[1].bar(yrs, [r["area_km2_ndvi_gt_0_3"] for r in rows], color="#117A65", width=0.6)
    axs[1].set_title("Former reservoir bed: area with NDVI > 0.3 (km²)", loc="left")
    for a in axs:
        a.axvline(2022.5, color=EST, lw=1, ls="--")
        a.set_xticks(yrs)
    S.save(fig, f"{FIG}/s2_fig5_h3_reservoir_bed.png")

    # 6. H4 decomposition
    d = h34["H4_decomposition_Kherson"]["categories"]
    names = list(d)
    vals = [d[k]["contribution_to_oblast_relative_change"] for k in names]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.barh(names, vals, color=[EST if v < 0 else REF for v in vals], height=0.6)
    ax.axvline(0, color="#333333", lw=0.8)
    for i, v in enumerate(vals):
        ax.text(v + (0.0006 if v >= 0 else -0.0006), i, f"{v:+.4f}", va="center", ha="left" if v >= 0 else "right", fontsize=8)
    tot = h34["H4_decomposition_Kherson"]["sum_of_contributions"]
    ax.set_title(f"H4: contributions to Kherson Oblast's 2021→2024 Jul–Oct NDVI change\nrelative to zone O (total {tot:+.4f})", loc="left")
    ax.set_xlabel("Area-weighted contribution (NDVI units)")
    lim = max(abs(min(vals)), max(vals)) * 1.5
    ax.set_xlim(-lim, lim)
    S.save(fig, f"{FIG}/s2_fig6_h4_decomposition.png")


if __name__ == "__main__":
    main()
