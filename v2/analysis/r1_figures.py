"""R1-figures — event studies under Registered Revision 1 -> outputs/v2/figures/s2_fig7_revision_event_studies.png"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import eco_style as S  # noqa: E402
from a8_figures import event_panel, EST, GRID  # noqa: E402

OUT = "outputs/v2"


def main():
    S.apply()
    plt.rcParams["axes.axisbelow"] = True
    h1 = json.load(open(f"{OUT}/r1_h1_results.json"))
    h2 = json.load(open(f"{OUT}/r1_h2_results.json"))
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.3))
    event_panel(axs[0], h1["event_study"], f"H1 revised — matched\n({h1['matching']['matched_treated']} flooded pixels)")
    event_panel(axs[1], h1["robustness"]["1_no_matching"]["event_study"],
                f"H1 revised — no matching\n({h1['robustness']['1_no_matching']['n_treated_px']:,} flooded pixels)", color=GRID)
    event_panel(axs[2], h2["event_study"], "H2 revised — triple difference\n(2010–15 classification, steppe zone O, occupation)")
    for a in axs[1:]:
        a.set_ylabel("")
    S.save(fig, f"{OUT}/figures/s2_fig7_revision_event_studies.png")


if __name__ == "__main__":
    main()
