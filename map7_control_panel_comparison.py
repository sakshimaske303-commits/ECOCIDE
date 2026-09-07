import json
import matplotlib.pyplot as plt
import numpy as np

BACKGROUND = "#0a1628"
GRID_COLOR = "#1e3a5f"
INDIVIDUAL_COLOR = "#6c757d"
POOLED_COLOR = "#00b4d8"
NULL_COLOR = "#8a8a8a"
TEXT_COLOR = "#ffffff"
ZERO_LINE = "#e63946"

# did_term coefficients and HAC 95% CIs read from outputs/model_results.json, which
# generate_model_results.py builds by re-fitting did_model_multi_control.py directly
# (Kherson vs. each control individually, and the pooled four-control panel).
# Re-run generate_model_results.py first if the underlying NDVI data changes.
with open("outputs/model_results.json") as f:
    ROWS = json.load(f)["multi_control_rows"]


def main():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    n = len(ROWS)
    y_positions = np.arange(n)[::-1]

    for y, row in zip(y_positions, ROWS):
        color = POOLED_COLOR if row.get("pooled") else (NULL_COLOR if row["null"] else INDIVIDUAL_COLOR)
        lo, hi = row["ci"]
        ax.plot([lo, hi], [y, y], color=color, linewidth=3 if row.get("pooled") else 2.5, zorder=2)
        ax.plot(row["coef"], y, "o", color=color, markersize=10 if row.get("pooled") else 8, zorder=3)
        ax.text(0.075, y, f"p={row['p']:.4f}", color=color, fontsize=9.5, va="center", ha="left")

    ax.axvline(0, color=ZERO_LINE, linewidth=1.2, linestyle="--", alpha=0.8, zorder=1)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([r["label"] for r in ROWS], color=TEXT_COLOR, fontsize=11.5)
    ax.set_xlabel("did_term coefficient (95% CI, HAC standard errors)", color=TEXT_COLOR, fontsize=11)
    ax.set_xlim(-0.20, 0.16)
    ax.set_ylim(-0.6, n - 0.4)

    ax.tick_params(colors=TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.6, alpha=0.6)

    fig.text(0.5, 0.97, "MULTI-CONTROL ROBUSTNESS CHECK: DOES THE EFFECT HOLD AGAINST EACH CONTROL?", fontsize=14.5,
              fontweight="bold", color=TEXT_COLOR, ha="center")
    fig.text(0.5, 0.935,
              "Kherson vs. each of 4 Danube/Black Sea control counties individually, plus the pooled 4-control panel",
              fontsize=10.5, color="#cccccc", ha="center")

    plt.figtext(0.5, 0.02, "ECOCIDE — did_model_multi_control.py",
                ha="center", fontsize=8.5, color="#888888")

    plt.tight_layout(rect=[0, 0.04, 1, 0.90])
    plt.savefig("outputs/plots/control_panel_comparison.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/control_panel_comparison.png")


if __name__ == "__main__":
    main()
