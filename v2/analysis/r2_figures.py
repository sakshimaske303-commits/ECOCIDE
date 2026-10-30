"""R2-figures — Registered Revision 2 figures -> outputs/v2/figures/s2_fig8 … s2_fig11

  8  H1: flooded minus terrain-matched / all candidate land, relative to 2016–2018
  9  H2: canal-fed irrigated minus never-irrigated cropland, relative to 2016–2018, with July–October rainfall
 10  H4: contributions to Kherson Oblast's change with 95 % block-bootstrap intervals
 11  Irrigated fields of Baber et al. (2026b) on the grid, 2019–2021 mean and 2024 (needs r2_layers.npz)
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "src"))
import eco_style as S  # noqa: E402

OUT = "outputs/v2"
FIG = f"{OUT}/figures"
EST, GRID, REF = "#C0392B", "#7F7F7F", "#1F77B4"


def panel(ax, es, title, color=EST, label=None, offset=0.0):
    rows = es["relative_to_2016_2018_mean"]
    y = np.array([r["year"] for r in rows]) + offset
    b = np.array([r["coef"] for r in rows])
    se = np.array([r["se"] for r in rows])
    ax.axhline(0, color="#333333", lw=0.8)
    ax.axvspan(2015.6, 2018.5, color="#F3F3F3", zorder=0)
    ax.axvspan(2021.5, 2022.5, color="#EEEEEE", zorder=0)
    ax.axvspan(2022.5, 2024.6, color="#FBE9E7", zorder=0)
    ax.errorbar(y, b, yerr=1.96 * se, fmt="o", color=color, ms=6, lw=2, capsize=0, label=label)
    ax.set_xticks(range(2016, 2025))
    ax.set_title(title, loc="left")
    ax.set_ylabel("Difference in Jul–Oct NDVI\n(relative to 2016–2018 mean)")


def labels(ax):
    top = ax.get_ylim()[1]
    for x, t in ((2017, "baseline"), (2022, "war"), (2023.5, "after breach")):
        ax.text(x, top, t, ha="center", va="top", fontsize=8, color="#555555")


def main():
    S.apply()
    plt.rcParams["axes.axisbelow"] = True
    os.makedirs(FIG, exist_ok=True)
    h1 = json.load(open(f"{OUT}/r2_h1_results.json"))
    h2 = json.load(open(f"{OUT}/r2_h2_results.json"))
    h4 = json.load(open(f"{OUT}/r2_h3_h4_results.json"))["H4_decomposition_Kherson"]

    # 8. H1
    fig, ax = plt.subplots(figsize=(8.5, 4.3))
    n_m = h1["matched"]["n_treated_px"]
    panel(ax, h1["unmatched"]["event_study"], "", color=GRID,
          label=f"all flooded pixels, not matched ({h1['unmatched']['n_treated_px']:,})", offset=0.12)
    panel(ax, h1["matched"]["event_study"], "H1 flood — Registered Revision 2", color=EST,
          label=f"matched on terrain and land cover ({n_m:,} flooded pixels in the panel)", offset=-0.12)
    labels(ax)
    ax.legend(loc="lower left", fontsize=8, frameon=False)
    S.save(fig, f"{FIG}/s2_fig8_r2_flood.png")

    # 9. H2 with rainfall
    fig, (ax, axr) = plt.subplots(2, 1, figsize=(8.5, 6.2), sharex=True, gridspec_kw={"height_ratios": [2.3, 1]})
    s = h2["sample"]["pixels"]
    panel(ax, h2["event_study"], f"H2 irrigation — Registered Revision 2\ncanal-fed irrigated ({s['irrigated_canal_fed']:,}) "
          f"minus never-irrigated cropland ({s['never_irrigated']:,}), Baber et al. maps")
    labels(ax)
    xp = f"{OUT}/x1_review_diagnostics.json"
    if os.path.exists(xp):
        w = json.load(open(xp))["D1_weather_jul_oct"]["zone_K"]
        yrs = sorted(int(k) for k in w)
        axr.bar(yrs, [w[str(k)]["precip_mm"] for k in yrs], color="#9ECAE1", width=0.6)
        axr.set_ylabel("Jul–Oct rain,\ncanal zone (mm)")
    axr.set_xticks(range(2016, 2025))
    S.save(fig, f"{FIG}/s2_fig9_r2_irrigation.png")

    # 10. H4 with intervals
    cats = h4["categories"]
    names = list(cats)
    vals = [cats[n]["contribution"] for n in names] + [h4["sum_of_contributions"]]
    lo = [cats[n]["contribution_ci95"][0] for n in names] + [h4["sum_ci95"][0]]
    hi = [cats[n]["contribution_ci95"][1] for n in names] + [h4["sum_ci95"][1]]
    names = names + ["Kherson Oblast, total"]
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    yy = np.arange(len(names))[::-1]
    cols = [EST if v < 0 else REF for v in vals]
    cols[-1] = "#333333"
    ax.barh(yy, vals, color=cols, height=0.6)
    ax.errorbar(vals, yy, xerr=[np.array(vals) - np.array(lo), np.array(hi) - np.array(vals)], fmt="none",
                ecolor="#333333", lw=1.2)
    ax.set_yticks(yy)
    ax.set_yticklabels([n if cats.get(n, {}).get("pixels_valid", 1) else f"{n} (no pre-breach land)" for n in names])
    ax.axvline(0, color="#333333", lw=0.8)
    ax.set_xlabel("Contribution to the change in Jul–Oct NDVI, 2016–18 → 2023–24, relative to zone O")
    ax.set_title("H4 — Kherson Oblast, Registered Revision 2 (95 % block-bootstrap intervals)", loc="left")
    S.save(fig, f"{FIG}/s2_fig10_r2_h4.png")

    # 11. irrigated fields map (needs the derived layers)
    p = "data/v2/derived/r2_layers.npz"
    if os.path.exists(p):
        z = np.load(p)
        cov = z["covered"]
        rows, cols_ = np.where(cov)
        r0, r1, c0, c1 = rows.min(), rows.max() + 1, cols_.min(), cols_.max() + 1
        fig, axs = plt.subplots(1, 2, figsize=(12, 5.2))
        for a, key, t in ((axs[0], "irr_mean_1921", "Mean irrigated share, 2019–2021"),
                          (axs[1], "irrfrac_2024", "Irrigated share, 2024")):
            v = z[key].astype(np.float32)[r0:r1, c0:c1] if key in z.files else None
            if v is None:
                a.set_axis_off()
                continue
            img = np.where(cov[r0:r1, c0:c1], v, np.nan)
            im = a.imshow(img, cmap="YlGnBu", vmin=0, vmax=1, interpolation="nearest")
            a.set_title(t, loc="left")
            a.set_xticks([])
            a.set_yticks([])
        fig.colorbar(im, ax=axs, shrink=0.8, label="share of 30 m cells mapped as irrigated")
        fig.suptitle("Irrigated fields of Baber et al. (2026b) on the 231 m grid, Kherson and Zaporizhzhia oblasts",
                     x=0.01, ha="left")
        S.save(fig, f"{FIG}/s2_fig11_irrigated_fields.png")
    else:
        print(f"{p} not found: figure 11 skipped")


if __name__ == "__main__":
    main()
