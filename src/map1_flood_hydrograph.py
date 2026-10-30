"""Flood-extent observations after the Kakhovka Dam breach, one point per
UNOSAT layer, labelled by sensor. File name kept for continuity; this is a
set of separate satellite observations, not a hydrograph (discharge series)
and not a single continuous time series: sensors differ in resolution,
analysis extent and cloud obstruction (see outputs/flood_extent_table.csv)."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

import eco_flood as ef
import eco_style as st

MARKERS = {"Sentinel-3": ("s", "#1F77B4"), "ICEYE (SAR)": ("D", "#C0392B"),
           "Sentinel-2": ("^", "#2CA02C"), "Sentinel-1 (SAR)": ("o", "#9467BD")}


def main():
    st.apply()
    rows, comp = ef.table()
    fig, ax = plt.subplots(figsize=(9.5, 5))
    for r in rows:
        mk, c = MARKERS[r["sensor"]]
        d = pd.Timestamp(r["date"])
        ax.plot(d, r["flood_km2"], mk, color=c, ms=9, label=r["sensor"])
        note = f"{r['flood_km2']:.1f} km²"
        if r["cloud_km2"] > 1000:
            note += f"\n({r['cloud_km2']/r['analysis_extent_km2']:.0%} of extent cloud-obscured)"
        ax.annotate(note, (d, r["flood_km2"]), xytext=(8, 4), textcoords="offset points", fontsize=8)
    ax.axhline(comp["flood_km2"], color="#555555", ls=":", lw=1.2)
    ax.text(pd.Timestamp("2023-06-10"), comp["flood_km2"] + 8,
            f"UNOSAT cumulative 6–9 June composite: {comp['flood_km2']:.0f} km²", fontsize=8, color="#333333")
    ax.axvline(pd.Timestamp("2023-06-06"), color="#333333", ls="--", lw=1)
    h, l = ax.get_legend_handles_labels()
    uniq = dict(zip(l, h))
    ax.legend(uniq.values(), uniq.keys(), loc="center right", fontsize=8.5, title="Sensor", title_fontsize=8.5)
    ax.set_ylim(0, 700)
    ax.set_ylabel("Mapped flood extent (km²)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.set_title("UNOSAT flood-extent observations after the dam breach, June 2023")
    fig.text(0.01, -0.05, "Each point is a separate UNOSAT layer with its own sensor, resolution and analysis extent; "
             "values are not directly comparable across sensors.\nSource: UNOSAT FL20230606UKR (preliminary, not field-validated).",
             fontsize=7.5, color="#555555")
    st.save(fig, "outputs/plots/flood_hydrograph.png")


if __name__ == "__main__":
    main()
