import geopandas as gpd
import matplotlib.pyplot as plt

BACKGROUND = "#0a1628"
TREATMENT_COLOR = "#e63946"
CONTROL_COLOR = "#00b4d8"
TEXT_COLOR = "#ffffff"


def main():
    kherson = gpd.read_file("data/boundaries/kherson_oblast.gpkg")
    tulcea = gpd.read_file("data/boundaries/tulcea_county.gpkg")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 9))
    fig.patch.set_facecolor(BACKGROUND)

    for ax, gdf, color, label in [
        (ax1, kherson, TREATMENT_COLOR, "KHERSON OBLAST, UKRAINE\n(Treatment — Conflict Zone)"),
        (ax2, tulcea, CONTROL_COLOR, "TULCEA COUNTY, ROMANIA\n(Control — Non-Conflict)"),
    ]:
        ax.set_facecolor(BACKGROUND)
        gdf.plot(ax=ax, facecolor=color, edgecolor="white", linewidth=1.5, alpha=0.6)
        bounds = gdf.total_bounds
        pad_x = (bounds[2] - bounds[0]) * 0.15
        pad_y = (bounds[3] - bounds[1]) * 0.15
        ax.set_xlim(bounds[0] - pad_x, bounds[2] + pad_x)
        ax.set_ylim(bounds[1] - pad_y, bounds[3] + pad_y)
        ax.set_axis_off()
        ax.set_title(label, color=TEXT_COLOR, fontsize=15, fontweight="bold", pad=15)

    fig.text(0.5, 0.96, "ECOCIDE — STUDY AREA", fontsize=26, fontweight="bold",
              color=TEXT_COLOR, ha="center")
    fig.text(0.5, 0.91, "Difference-in-Differences Design: Kakhovka Dam Destruction (6 June 2023)",
              fontsize=13, color="#cccccc", ha="center")

    plt.figtext(0.5, 0.02, "ECOCIDE — Boundaries: GADM v4.1",
                ha="center", fontsize=9, color="#888888")

    plt.tight_layout(rect=[0, 0.03, 1, 0.88])
    plt.savefig("outputs/plots/study_area_overview.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/study_area_overview.png")


if __name__ == "__main__":
    main()