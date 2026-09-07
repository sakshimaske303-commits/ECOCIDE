import json
import matplotlib.pyplot as plt
import numpy as np

BACKGROUND = "#0a1628"
GRID_COLOR = "#1e3a5f"
CLASSIC_COLOR = "#6c757d"
HAC_COLOR = "#00b4d8"
TEXT_COLOR = "#ffffff"
ZERO_LINE = "#e63946"

# Coefficients and 95% CIs read from outputs/model_results.json, which
# generate_model_results.py builds by re-fitting did_model.py, did_model_narrowed.py,
# placebo_test.py, and placebo_narrowed.py directly (classical OLS vs Newey-West HAC).
# Re-run generate_model_results.py first if the underlying NDVI data changes.
with open("outputs/model_results.json") as f:
    _results = json.load(f)

MODELS = [_results["main_did"], _results["narrowed_did"], _results["placebo_broad"], _results["placebo_narrowed"]]


def main():
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    n = len(MODELS)
    y_positions = np.arange(n)[::-1]

    for y, m in zip(y_positions, MODELS):
        y_classic = y + 0.15
        y_hac = y - 0.15

        c_lo, c_hi = m["classic_ci"]
        ax.plot([c_lo, c_hi], [y_classic, y_classic], color=CLASSIC_COLOR, linewidth=2.5, zorder=2)
        ax.plot(m["coef"], y_classic, "o", color=CLASSIC_COLOR, markersize=8, zorder=3)

        h_lo, h_hi = m["hac_ci"]
        ax.plot([h_lo, h_hi], [y_hac, y_hac], color=HAC_COLOR, linewidth=2.5, zorder=2)
        ax.plot(m["coef"], y_hac, "o", color=HAC_COLOR, markersize=8, zorder=3)

        ax.text(0.235, y_classic, f"p={m['classic_p']:.4f}", color=CLASSIC_COLOR,
                fontsize=9.5, va="center", ha="left")
        ax.text(0.235, y_hac, f"p={m['hac_p']:.4f}", color=HAC_COLOR,
                fontsize=9.5, va="center", ha="left")

    ax.axvline(0, color=ZERO_LINE, linewidth=1.2, linestyle="--", alpha=0.8, zorder=1)

    ax.set_yticks(y_positions)
    ax.set_yticklabels([m["label"] for m in MODELS], color=TEXT_COLOR, fontsize=12)
    ax.set_xlabel("did_term coefficient (95% CI)", color=TEXT_COLOR, fontsize=11)
    ax.set_xlim(-0.42, 0.42)
    ax.set_ylim(-0.6, n - 0.4)

    ax.tick_params(colors=TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(axis="x", color=GRID_COLOR, linewidth=0.6, alpha=0.6)

    legend_handles = [
        plt.Line2D([0], [0], color=CLASSIC_COLOR, linewidth=2.5, marker="o", label="Classical OLS"),
        plt.Line2D([0], [0], color=HAC_COLOR, linewidth=2.5, marker="o", label="Newey-West HAC"),
    ]
    legend = ax.legend(handles=legend_handles, loc="upper left", fontsize=11, frameon=True,
                        facecolor="#1a1a2e", edgecolor="none")
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.text(0.5, 0.96, "ROBUSTNESS: CLASSICAL vs. HAC STANDARD ERRORS", fontsize=17,
              fontweight="bold", color=TEXT_COLOR, ha="center")
    fig.text(0.5, 0.925, "Point estimates and 95% confidence intervals across all four causal-inference models",
              fontsize=11, color="#cccccc", ha="center")

    plt.figtext(0.5, 0.02, "ECOCIDE — did_model.py / did_model_narrowed.py / placebo_test.py / placebo_narrowed.py",
                ha="center", fontsize=8.5, color="#888888")

    plt.tight_layout(rect=[0, 0.04, 1, 0.90])
    plt.savefig("outputs/plots/robustness_check.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/robustness_check.png")


if __name__ == "__main__":
    main()
