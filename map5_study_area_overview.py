import geopandas as gpd
import matplotlib.pyplot as plt

BACKGROUND = "#0a1628"
TREATMENT_COLOR = "#e63946"
CONTROL_COLOR = "#00b4d8"
CONTROL_NULL_COLOR = "#6c757d"  # Constanța — the control that doesn't reproduce the effect
TEXT_COLOR = "#ffffff"

ZONES = [
    ("kherson_oblast.gpkg", TREATMENT_COLOR, "KHERSON OBLAST, UKRAINE\n(Treatment — Conflict Zone)"),
    ("tulcea_county.gpkg", CONTROL_COLOR, "TULCEA COUNTY, ROMANIA\n(Control — Primary)"),
    ("galati_county.gpkg", CONTROL_COLOR, "GALAȚI COUNTY, ROMANIA\n(Control)"),
    ("braila_county.gpkg", CONTROL_COLOR, "BRĂILA COUNTY, ROMANIA\n(Control)"),
    ("constanta_county.gpkg", CONTROL_NULL_COLOR, "CONSTANȚA COUNTY, ROMANIA\n(Control — Null Result)"),
]


def main():
    fig, axes = plt.subplots(1, 5, figsize=(26, 7.5))
    fig.patch.set_facecolor(BACKGROUND)

    for ax, (fname, color, label) in zip(axes, ZONES):
        gdf = gpd.read_file(f"data/boundaries/{fname}")
        ax.set_facecolor(BACKGROUND)
        gdf.plot(ax=ax, facecolor=color, edgecolor="white", linewidth=1.5, alpha=0.6)
        bounds = gdf.total_bounds
        pad_x = (bounds[2] - bounds[0]) * 0.15
        pad_y = (bounds[3] - bounds[1]) * 0.15
        ax.set_xlim(bounds[0] - pad_x, bounds[2] + pad_x)
        ax.set_ylim(bounds[1] - pad_y, bounds[3] + pad_y)
        ax.set_axis_off()
        ax.set_title(label, color=TEXT_COLOR, fontsize=12.5, fontweight="bold", pad=12)

    fig.text(0.5, 0.99, "ECOCIDE — STUDY AREA", fontsize=26, fontweight="bold",
              color=TEXT_COLOR, ha="center")
    fig.text(0.5, 0.945,
              "Difference-in-Differences Design: Kakhovka Dam Destruction (6 June 2023) — "
              "1 treatment zone, 4-control panel",
              fontsize=13, color="#cccccc", ha="center")

    plt.figtext(0.5, 0.015, "ECOCIDE — Boundaries: GADM v4.1",
                ha="center", fontsize=9, color="#888888")

    plt.tight_layout(rect=[0, 0.03, 1, 0.82])
    plt.savefig("outputs/plots/study_area_overview.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/study_area_overview.png")


if __name__ == "__main__":
    main()
