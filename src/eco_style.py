"""Shared figure style for all ECOCIDE static figures (publication style:
white background, 300 dpi, colour-blind-safe palette)."""
import json

import matplotlib as mpl
import matplotlib.pyplot as plt

DPI = 300
TREATED = "#C0392B"      # Kherson
CONTROL = "#1F77B4"      # primary control / HAC
NEUTRAL = "#7F7F7F"      # classical / non-significant
POOLED = "#117A65"
FLAG = "#D35400"
ZONE_COLORS = {
    "kherson": TREATED,
    "tulcea": "#1F77B4",
    "galati": "#2CA02C",
    "braila": "#9467BD",
    "constanta": "#8C564B",
}
ZONE_LABELS = {
    "kherson": "Kherson (UA)",
    "tulcea": "Tulcea (RO)",
    "galati": "Galați (RO)",
    "braila": "Brăila (RO)",
    "constanta": "Constanța (RO)",
}


def apply():
    mpl.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#333333",
        "axes.grid": True,
        "grid.color": "#DDDDDD",
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "legend.frameon": False,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
    })


def results():
    with open("outputs/model_results.json", encoding="utf-8") as f:
        return json.load(f)


def save(fig, path):
    fig.savefig(path)
    plt.close(fig)
    print("Saved:", path)
