"""Kherson vs each Romanian control individually and pooled; numbers read
from outputs/model_results.json."""
import matplotlib.pyplot as plt
import numpy as np

import eco_style as st


def draw(path):
    st.apply()
    R = st.results()
    rows = [(f"Kherson vs {st.ZONE_LABELS[z].split(' ')[0]}" + (" (primary)" if z == "tulcea" else ""), R["per_control"][z], st.NEUTRAL)
            for z in ["tulcea", "galati", "braila", "constanta"]]
    rows.append(("Kherson vs mean of all 4", R["pooled_did"], st.POOLED))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ys = np.arange(len(rows))[::-1]
    for y, (label, m, c) in zip(ys, rows):
        ax.plot(m["ci"], [y, y], color=c, lw=2.6)
        ax.plot(m["coef"], y, "o", color=c, ms=7)
        ax.text(1.02, y, f"{m['coef']:+.3f}, p={m['p']:.3f}", transform=ax.get_yaxis_transform(), va="center", fontsize=8.5)
    ax.axvline(0, color="#333333", ls="--", lw=1)
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows])
    ax.set_xlabel("DiD coefficient (NDVI units), 95% CI, Newey-West HAC (t)")
    ax.set_title("Kherson against each control county and the pooled panel")
    st.save(fig, path)


if __name__ == "__main__":
    draw("outputs/plots/control_panel_comparison.png")
