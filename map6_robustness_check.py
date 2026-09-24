"""Classical vs Newey-West HAC 95% CIs for the primary DiD, narrowed DiD and
their placebos; numbers read from outputs/model_results.json."""
import matplotlib.pyplot as plt
import numpy as np

import eco_style as st

MODELS = [
    ("main_did", "Primary DiD\n(Jan 2022 – Nov 2024)", False),
    ("placebo_broad", "Placebo, fake date Jun 2022", True),
    ("narrowed_did", "Narrowed-baseline DiD\n(Jan 2023 – Nov 2024)", False),
    ("placebo_narrowed", "Narrowed placebo,\nfake date Mar 2023 (5 months)", True),
]


def main():
    st.apply()
    R = st.results()
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ys = np.arange(len(MODELS))[::-1]
    for y, (key, label, is_placebo) in zip(ys, MODELS):
        m = R[key]
        ax.plot(m["classic_ci"], [y + 0.14] * 2, color=st.NEUTRAL, lw=2.2)
        ax.plot(m["coef"], y + 0.14, "o", color=st.NEUTRAL)
        failed = is_placebo and m["p"] < 0.05
        c = st.FLAG if failed else st.CONTROL
        ax.plot(m["ci"], [y - 0.14] * 2, color=c, lw=2.6)
        ax.plot(m["coef"], y - 0.14, "X" if failed else "o", color=c, ms=8 if failed else 6)
        ax.text(1.02, y + 0.14, f"classical p={m['classic_p']:.3f}", transform=ax.get_yaxis_transform(),
                va="center", fontsize=8, color=st.NEUTRAL)
        ax.text(1.02, y - 0.14, f"HAC p={m['p']:.3f}" + ("  placebo significant" if failed else ""),
                transform=ax.get_yaxis_transform(), va="center", fontsize=8, color=c)
    ax.axvline(0, color="#333333", ls="--", lw=1)
    ax.set_yticks(ys)
    ax.set_yticklabels([m[1] for m in MODELS])
    ax.set_xlabel("DiD coefficient (NDVI units), 95% CI")
    ax.plot([], [], color=st.NEUTRAL, lw=2.2, label="classical OLS")
    ax.plot([], [], color=st.CONTROL, lw=2.6, label="Newey-West HAC (t)")
    ax.plot([], [], color=st.FLAG, lw=2.6, marker="X", label="placebo significant under HAC")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=8.5)
    ax.set_title("Primary and narrowed-baseline estimates with their placebo tests")
    st.save(fig, "outputs/plots/robustness_check.png")


if __name__ == "__main__":
    main()
