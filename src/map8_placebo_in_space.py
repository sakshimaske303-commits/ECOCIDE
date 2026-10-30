"""Placebo-in-space (randomization inference): each zone assigned 'treated'
in turn against the other four; numbers from outputs/model_results.json."""
import matplotlib.pyplot as plt
import numpy as np

import eco_style as st


def main():
    st.apply()
    R = st.results()["placebo_in_space"]
    units = sorted(R["units"].items(), key=lambda kv: kv[1]["coef"])
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ys = np.arange(len(units))[::-1]
    for y, (z, m) in zip(ys, units):
        c = st.TREATED if z == "kherson" else st.NEUTRAL
        ax.plot(m["ci"], [y, y], color=c, lw=2.6)
        ax.plot(m["coef"], y, "o", color=c, ms=7)
        ax.text(1.02, y, f"{m['coef']:+.3f}, p={m['p']:.3f}", transform=ax.get_yaxis_transform(), va="center", fontsize=8.5)
    ax.axvline(0, color="#333333", ls="--", lw=1)
    ax.set_yticks(ys)
    ax.set_yticklabels([st.ZONE_LABELS[z] + (" — actual" if z == "kherson" else "") for z, _ in units])
    ax.set_xlabel("DiD coefficient when the unit is assigned 'treated' vs the other four (95% CI, HAC)")
    ax.set_title(f"Placebo in space: Kherson ranks {R['rank_one_sided']}/5 one-sided (exact p={R['p_one_sided']:.2f}), "
                 f"{R['rank_two_sided']}/5 two-sided (p={R['p_two_sided']:.2f})", fontsize=10.5)
    st.save(fig, "outputs/plots/placebo_in_space.png")


if __name__ == "__main__":
    main()
