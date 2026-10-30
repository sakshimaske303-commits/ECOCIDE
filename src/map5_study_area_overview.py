"""Study-area map: treatment and control zones in their true positions."""
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import eco_style as st

ZONES = [
    ("kherson", "kherson_oblast.gpkg", "Kherson Oblast\n(treatment)"),
    ("tulcea", "tulcea_county.gpkg", "Tulcea\n(primary control)"),
    ("galati", "galati_county.gpkg", "Galați"),
    ("braila", "braila_county.gpkg", "Brăila"),
    ("constanta", "constanta_county.gpkg", "Constanța"),
]


def main():
    st.apply()
    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.grid(color="#EEEEEE")
    handles = []
    for z, f, label in ZONES:
        g = gpd.read_file(f"data/boundaries/{f}").to_crs(4326)
        g.plot(ax=ax, color=st.ZONE_COLORS[z], alpha=0.55, edgecolor="#333333", lw=0.6)
        c = g.union_all().representative_point()
        dy = -0.35 if z == "kherson" else 0
        ax.text(c.x, c.y + dy, label, ha="center", va="center", fontsize=8.5, fontweight="bold")
    ax.plot(33.37, 46.777, marker="*", color="black", ms=12)
    ax.annotate("Kakhovka Dam", (33.37, 46.777), xytext=(8, 8), textcoords="offset points", fontsize=8, bbox=dict(fc="white", ec="none", alpha=0.8, pad=1))
    ax.set_xlim(26.8, 35.5)
    ax.set_ylim(43.5, 48.0)
    ax.set_aspect(1 / 0.70)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    x0, y0 = 27.0, 43.7
    ax.plot([x0, x0 + 100 / 78.0], [y0, y0], color="black", lw=3)
    ax.text(x0 + 50 / 78.0, y0 + 0.08, "100 km", ha="center", fontsize=8)
    ax.set_title("Study area: Kherson Oblast (Ukraine) and four Romanian control counties")
    fig.text(0.01, 0.0, "Boundaries: GADM v4.1. Tulcea borders Ukraine's Odesa Oblast along the Danube.", fontsize=7.5, color="#555555")
    st.save(fig, "outputs/plots/study_area_overview.png")


if __name__ == "__main__":
    main()
