"""Quarterly event-study figure; numbers read from outputs/model_results.json
(run generate_model_results.py first)."""
import matplotlib.pyplot as plt

import eco_style as st


def main():
    st.apply()
    R = st.results()
    rows = R["event_study"]["quarters"]
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for r in rows:
        col = st.TREATED if r["p"] < 0.05 else st.NEUTRAL
        ax.errorbar(r["quarter"], r["coef"], yerr=[[r["coef"] - r["ci"][0]], [r["ci"][1] - r["coef"]]],
                    fmt="o", color=col, ecolor=col, capsize=3, ms=6)
        if r["bonferroni"]:
            ax.annotate("†", (r["quarter"], r["ci"][1]), xytext=(0, 3), textcoords="offset points", ha="center")
    ax.plot(-1, 0, marker="s", color="black", ms=6)
    ax.axhline(0, color="#333333", lw=0.8)
    ax.axvline(-0.5, color="#333333", ls="--", lw=1)
    ax.set_xticks([r["quarter"] for r in rows] + [-1])
    ax.set_xticklabels([f"{r['quarter']:+d}\n{r['months'].split('–')[0]}" for r in rows] + ["-1\nref"], fontsize=7.5)
    ax.set_xlabel("Quarter relative to June 2023 (quarter 0 = Jun–Aug 2023; reference = Mar–May 2023)")
    ax.set_ylabel("Kherson − Tulcea NDVI gap\n(relative to reference quarter)")
    ax.set_title("Quarterly event study, Kherson vs Tulcea")
    ax.plot([], [], "o", color=st.TREATED, label="p < 0.05 (HAC, t)")
    ax.plot([], [], "o", color=st.NEUTRAL, label="p ≥ 0.05")
    ax.plot([], [], "s", color="black", label="reference quarter")
    ax.legend(loc="lower left", fontsize=8.5)
    fig.text(0.01, -0.06, f"† survives Bonferroni correction across 11 quarters (p < {R['event_study']['bonferroni_threshold']:.5f}). "
             "95% CIs, Newey-West HAC (maxlags=3).", fontsize=7.5, color="#555555")
    st.save(fig, "outputs/plots/event_study.png")


if __name__ == "__main__":
    main()
