import geopandas as gpd
import matplotlib.pyplot as plt

BACKGROUND = "#0a1628"
BOUNDARY_COLOR = "#2d6a4f"
FLOOD_COLORS = {
    "2023-06-06": "#fca311",
    "2023-06-09": "#e63946",
    "2023-06-21": "#00b4d8",
}
TEXT_COLOR = "#ffffff"

DATES = {
    "2023-06-06": "ST3_20230606_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-09": "ST3_20230609_FloodExtent_KhersonskaOblast_UKR.shp",
    "2023-06-21": "ST1_20230621_FloodExtent_KhersonskarOblast_UKR.shp",
}


def main():
    boundary = gpd.read_file("data/boundaries/kherson_oblast.gpkg")

    fig, ax = plt.subplots(figsize=(14, 12))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    boundary.plot(ax=ax, facecolor="none", edgecolor=BOUNDARY_COLOR, linewidth=1.5, zorder=1)

    for date, filename in DATES.items():
        path = f"data/ndwi/FL20230606UKR_SHP.zip!FL20230606UKR_SHP/{filename}"
        flood = gpd.read_file(path)
        flood.plot(ax=ax, facecolor=FLOOD_COLORS[date], edgecolor="white",
                   linewidth=0.5, alpha=0.75, zorder=3, label=date)

    # Zoom to the flood-affected corridor rather than the full oblast
    ax.set_xlim(31.9, 33.6)
    ax.set_ylim(46.2, 47.0)
    ax.set_axis_off()

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=FLOOD_COLORS[d], alpha=0.75, label=d)
        for d in DATES.keys()
    ]
    legend = ax.legend(handles=handles, loc="lower left", fontsize=11, frameon=True,
                        facecolor="#1a1a2e", edgecolor="none", title="Flood Extent Date")
    legend.get_title().set_color(TEXT_COLOR)
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.text(0.5, 0.94, "KAKHOVKA DAM FLOOD EXTENT", fontsize=24, fontweight="bold",
              color=TEXT_COLOR, ha="center")
    fig.text(0.5, 0.90, "Verified multi-sensor flood polygons, Kherson Oblast, Ukraine",
              fontsize=13, color="#cccccc", ha="center")

    plt.figtext(0.5, 0.02, "ECOCIDE — Source: UNOSAT Multi-Sensor Flood Mapping",
                ha="center", fontsize=9, color="#888888")

    plt.savefig("outputs/plots/flood_extent_map.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/flood_extent_map.png")


if __name__ == "__main__":
    main()