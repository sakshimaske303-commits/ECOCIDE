import json
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import numpy as np

BACKGROUND = "#0a1628"
GRID_COLOR = "#1e3a5f"
SIG_COLOR = "#e63946"
NONSIG_COLOR = "#6c757d"
TEXT_COLOR = "#ffffff"
ACCENT = "#00b4d8"


def load_ndvi(zone_name, is_treatment):
    with open(f"data/ndvi/{zone_name}_ndvi_monthly.json") as f:
        data = json.load(f)
    rows = []
    for entry in data["data"]:
        date = entry["interval"]["from"][:7] + "-01"
        ndvi = entry["outputs"]["ndvi"]["bands"]["B0"]["stats"]["mean"]
        rows.append({"date": date, "ndvi": ndvi, "treatment": is_treatment})
    return pd.DataFrame(rows)


def main():
    kherson = load_ndvi("kherson", is_treatment=1)
    tulcea = load_ndvi("tulcea", is_treatment=0)

    df = pd.concat([kherson, tulcea], ignore_index=True)
    df["date"] = pd.to_datetime(df["date"])
    df["month_num"] = df["date"].dt.month.astype(str)

    treatment_date = pd.Timestamp("2023-06-01")
    rel_month = ((df["date"].dt.year - treatment_date.year) * 12 +
                 (df["date"].dt.month - treatment_date.month))
    df["rel_quarter"] = (rel_month // 3)

    quarters = sorted(df["rel_quarter"].unique())
    ref_quarter = -1
    quarters = [q for q in quarters if q != ref_quarter]

    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        df[col_name] = ((df["rel_quarter"] == q) & (df["treatment"] == 1)).astype(int)

    event_terms = " + ".join([f"evt_q{q}".replace("-", "neg") for q in quarters])
    formula = f"ndvi ~ treatment + C(month_num) + {event_terms}"
    model = smf.ols(formula, data=df).fit()

    plot_quarters, coefs, ci_lower, ci_upper, colors = [], [], [], [], []
    for q in quarters:
        col_name = f"evt_q{q}".replace("-", "neg")
        if col_name in model.params.index:
            coef = model.params[col_name]
            ci = model.conf_int().loc[col_name]
            pval = model.pvalues[col_name]
            plot_quarters.append(q)
            coefs.append(coef)
            ci_lower.append(coef - ci[0])
            ci_upper.append(ci[1] - coef)
            colors.append(SIG_COLOR if pval < 0.05 else NONSIG_COLOR)

    fig, ax = plt.subplots(figsize=(15, 8))
    fig.patch.set_facecolor(BACKGROUND)
    ax.set_facecolor(BACKGROUND)

    ax.errorbar(plot_quarters, coefs, yerr=[ci_lower, ci_upper], fmt="o", markersize=9,
                capsize=5, capthick=1.5, elinewidth=1.5, ecolor=ACCENT,
                markerfacecolor=SIG_COLOR, markeredgecolor="white", markeredgewidth=1)

    for q, c, col in zip(plot_quarters, coefs, colors):
        ax.plot(q, c, "o", markersize=9, color=col, markeredgecolor="white", markeredgewidth=1, zorder=5)

    ax.axhline(0, color="#ffffff", linestyle="-", linewidth=1, alpha=0.5)
    ax.axvline(0, color=ACCENT, linestyle="--", linewidth=1.5, alpha=0.7)
    ax.text(0, max(coefs) + max(ci_upper) + 0.02, "Dam Destroyed\n(Quarter 0)", color=ACCENT,
            fontsize=10, fontweight="bold", ha="center")

    ax.set_title("Event Study: Quarterly Treatment Effect on NDVI\nRelative to Kakhovka Dam Destruction (June 2023)",
                 color=TEXT_COLOR, fontsize=18, fontweight="bold", pad=20)
    ax.set_xlabel("Quarters Relative to Dam Destruction", color=TEXT_COLOR, fontsize=12)
    ax.set_ylabel("Treatment Effect on NDVI", color=TEXT_COLOR, fontsize=12)
    ax.tick_params(colors=TEXT_COLOR, labelsize=10)

    ax.grid(True, color=GRID_COLOR, linewidth=0.5, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)

    handles = [
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=SIG_COLOR, markersize=10, label="p < 0.05 (significant)"),
        plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=NONSIG_COLOR, markersize=10, label="Not significant"),
    ]
    legend = ax.legend(handles=handles, loc="lower left", fontsize=10, frameon=True, facecolor="#1a1a2e", edgecolor="none")
    for text in legend.get_texts():
        text.set_color(TEXT_COLOR)

    plt.figtext(0.5, 0.02, "ECOCIDE — Quarterly-binned event study, month fixed effects included",
                ha="center", fontsize=9, color="#888888")

    plt.tight_layout()
    plt.savefig("outputs/plots/event_study.png", dpi=220, facecolor=BACKGROUND, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/plots/event_study.png")


if __name__ == "__main__":
    main()