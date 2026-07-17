import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

dates = [
    datetime(2023, 6, 6),
    datetime(2023, 6, 8),
    datetime(2023, 6, 9),
    datetime(2023, 6, 13),
    datetime(2023, 6, 21),
]
areas = [122.50, 260.92, 464.18, 179.92, 21.17]

BACKGROUND = "#0a1628"
GRID_COLOR = "#1e3a5f"
LINE_COLOR = "#e63946"
FILL_COLOR = "#e6394633"
TEXT_COLOR = "#ffffff"
ACCENT = "#00b4d8"

fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor(BACKGROUND)
ax.set_facecolor(BACKGROUND)

ax.plot(dates, areas, color=LINE_COLOR, linewidth=3, marker="o", markersize=10,
        markerfacecolor=ACCENT, markeredgecolor="white", markeredgewidth=1.5, zorder=3)
ax.fill_between(dates, areas, color=FILL_COLOR, zorder=1)

for date, area in zip(dates, areas):
    ax.annotate(f"{area:.1f} km²", (date, area), textcoords="offset points",
                xytext=(0, 15), ha="center", color=TEXT_COLOR, fontsize=11, fontweight="bold")

ax.axvline(datetime(2023, 6, 6), color=ACCENT, linestyle="--", linewidth=1.5, alpha=0.6)
ax.text(datetime(2023, 6, 6), max(areas) * 1.08, "Dam Destroyed", color=ACCENT,
        fontsize=10, fontweight="bold", ha="center")

ax.set_title("Kakhovka Dam Flood Extent Progression\nDownstream Floodplain, June 2023",
             color=TEXT_COLOR, fontsize=18, fontweight="bold", pad=20)
ax.set_ylabel("Flood Extent (km²)", color=TEXT_COLOR, fontsize=12)

ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
ax.tick_params(colors=TEXT_COLOR, labelsize=10)
ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
for spine in ax.spines.values():
    spine.set_color(GRID_COLOR)

plt.figtext(0.5, 0.02, "ECOCIDE — Source: UNOSAT Multi-Sensor Flood Mapping (ICEYE, Landsat-9, SkySat, WorldView-3, MODIS)",
            ha="center", fontsize=9, color="#888888")

plt.tight_layout()
plt.savefig("outputs/plots/flood_hydrograph.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
plt.close()
print("Saved: outputs/plots/flood_hydrograph.png")