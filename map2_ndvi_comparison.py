import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

BACKGROUND = "#0a1628"
GRID_COLOR = "#1e3a5f"
TREATMENT_COLOR = "#e63946"
CONTROL_COLOR = "#00b4d8"
TEXT_COLOR = "#ffffff"


def load_ndvi(zone_name):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = pd.to_datetime(entry["interval"]["from"][:7] + "-01")
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi})
    return pd.DataFrame(rows)


def main():
    kherson = load_ndvi("kherson")
    tulcea = load_ndvi("tulcea")

    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    ax.plot(kherson["date"], kherson["ndvi"], color=TREATMENT_COLOR, linewidth=2.5,
            marker="o", markersize=5, label="Kherson (Treatment — Conflict Zone)", zorder=3)
    ax.plot(tulcea["date"], tulcea["ndvi"], color=CONTROL_COLOR, linewidth=2.5,
            marker="o", markersize=5, label="Tulcea (Control — Non-Conflict)", zorder=3)

    treatment_date = pd.Timestamp("2023-06-01")
    ax.axvline(treatment_date, color="#ffffff", linestyle="--", linewidth=1.5, alpha=0.7)
    ax.text(treatment_date, ax.get_ylim()[1] if ax.get_ylim()[1] else 0.4, "Kakhovka Dam Destroyed",
            color="#ffffff", fontsize=10, fontweight="bold", ha="center", va="bottom")

    ax.set_title("NDVI: Treatment vs. Control Zone (2022–2024)\nMonthly Vegetation Index Comparison",
                 color=TEXT_COLOR, fontsize=18, fontweight="bold", pad=20)
    ax.set_ylabel("NDVI", color=TEXT_COLOR, fontsize=12)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    legend = ax.legend(loc="upper left", fontsize=11, frameon=True, facecolor="#1a1a2e", edgecolor="none")
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)

    plt.figtext(0.5, 0.02, "ECOCIDE — Source: Sentinel-2 (Copernicus Data Space Ecosystem)",
                ha="center", fontsize=9, color="#888888")

    plt.tight_layout()
    plt.savefig("outputs/plots/ndvi_comparison.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/ndvi_comparison.png")


if __name__ == "__main__":
    main()