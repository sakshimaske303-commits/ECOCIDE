"""Map of three UNOSAT flood-extent layers (6, 9 and 21 June 2023)."""
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import eco_flood as ef
import eco_style as st

STYLE = {"2023-06-09": ("#F4A582", 1), "2023-06-06": ("#CA0020", 2), "2023-06-21": ("#0571B0", 3)}


def main():
    st.apply()
    boundary = gpd.read_file(ef.BOUNDARY)
    fig, ax = plt.subplots(figsize=(9, 6.5))
    ax.grid(False)
    boundary.boundary.plot(ax=ax, color="#555555", lw=0.8, zorder=0)
    handles = []
    sensors = {d: s for d, _, s, _, _ in ef.LAYERS}
    layers = {d: l for d, l, _, _, _ in ef.LAYERS}
    for date in ["2023-06-09", "2023-06-06", "2023-06-21"]:   # largest first, so smaller layers stay visible
        c, z = STYLE[date]
        ef.read(layers[date]).to_crs(4326).plot(ax=ax, color=c, lw=0, zorder=z)
        handles.append(Patch(color=c, label=f"{date[8:]} June 2023 — {sensors[date]}"))
    ax.set_xlim(31.9, 33.6)
    ax.set_ylim(46.3, 47.0)
    ax.set_aspect(1 / 0.687)  # cos(46.6°) so degrees are shown at true shape
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    # 20 km scale bar at 46.6°N: 1° lon ≈ 76.6 km
    x0, y0 = 31.98, 46.34
    ax.plot([x0, x0 + 20 / 76.6], [y0, y0], color="black", lw=3)
    ax.text(x0 + 10 / 76.6, y0 + 0.012, "20 km", ha="center", fontsize=8)
    ax.annotate("N", xy=(33.52, 46.97), xytext=(33.52, 46.9), ha="center",
                arrowprops=dict(arrowstyle="-|>", color="black"), fontsize=10, fontweight="bold")
    ax.plot(33.37, 46.777, marker="*", color="black", ms=11, zorder=5)
    ax.annotate("Kakhovka Dam", (33.37, 46.777), xytext=(-10, 8), textcoords="offset points", ha="right", fontsize=8)
    handles.sort(key=lambda h: h.get_label())
    handles.append(Patch(facecolor="none", edgecolor="#555555", label="Kherson Oblast boundary (GADM 4.1)"))
    ax.legend(handles=handles, loc="lower right", fontsize=8.5, frameon=True)
    ax.set_title("UNOSAT flood-extent layers, lower Dnipro, June 2023")
    fig.text(0.01, 0.0, "Source: UNOSAT FL20230606UKR (preliminary, not field-validated). Layers come from different sensors "
             "and analysis extents.", fontsize=7.5, color="#555555")
    st.save(fig, "outputs/plots/flood_extent_map.png")


if __name__ == "__main__":
    main()
