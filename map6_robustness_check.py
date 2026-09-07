import json
import matplotlib.pyplot as plt
import numpy as np

BACKGROUND = "#0a1628"
GRID_COLOR = "#1e3a5f"
CLASSIC_COLOR = "#6c757d"
HAC_COLOR = "#00b4d8"
FAIL_COLOR = "#e63946"
TEXT_COLOR = "#ffffff"
ZERO_LINE = "#e63946"

# Which row is a disclosed validation failure (its own placebo becomes
# significant under HAC), so it gets flagged rather than read as a fifth
# equally-valid model alongside the other three
FAILED_LABELS = {"Placebo\n(narrowed baseline)"}

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
        failed = m["label"] in FAILED_LABELS

        c_lo, c_hi = m["classic_ci"]
        ax.plot([c_lo, c_hi], [y_classic, y_classic], color=CLASSIC_COLOR, linewidth=2.5, zorder=2)
        ax.plot(m["coef"], y_classic, "o", color=CLASSIC_COLOR, markersize=8, zorder=3)

        h_lo, h_hi = m["hac_ci"]
        hac_color = FAIL_COLOR if failed else HAC_COLOR
        ax.plot([h_lo, h_hi], [y_hac, y_hac], color=hac_color, linewidth=3 if failed else 2.5, zorder=2)
        ax.plot(m["coef"], y_hac, "o" if not failed else "X", color=hac_color,
                markersize=8 if not failed else 10, zorder=3)

        ax.text(0.235, y_classic, f"p={m['classic_p']:.4f}", color=CLASSIC_COLOR,
                fontsize=9.5, va="center", ha="left")
        ax.text(0.235, y_hac, f"p={m['hac_p']:.4f}" + ("  ✗ fails under HAC" if failed else ""),
                color=hac_color, fontsize=9.5, fontweight="bold" if failed else "normal",
                va="center", ha="left")

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
        plt.Line2D([0], [0], color=FAIL_COLOR, linewidth=3, marker="X", markersize=9,
                   label="HAC — disclosed validation failure"),
    ]
    legend = ax.legend(handles=legend_handles, loc="upper left", fontsize=11, frameon=True,
                        facecolor="#1a1a2e", edgecolor="none")
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    fig.text(0.5, 0.96, "ROBUSTNESS: CLASSICAL vs. HAC STANDARD ERRORS", fontsize=17,
              fontweight="bold", color=TEXT_COLOR, ha="center")
    fig.text(0.5, 0.925,
              "Point estimates and 95% CIs across four checks — the narrowed-baseline placebo (marked ✗) is a disclosed validation failure, not a fifth confirmed model",
              fontsize=10, color="#cccccc", ha="center")

    plt.figtext(0.5, 0.02, "ECOCIDE — did_model.py / did_model_narrowed.py / placebo_test.py / placebo_narrowed.py",
                ha="center", fontsize=8.5, color="#888888")

    plt.tight_layout(rect=[0, 0.04, 1, 0.90])
    plt.savefig("outputs/plots/robustness_check.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/robustness_check.png")


if __name__ == "__main__":
    main()
