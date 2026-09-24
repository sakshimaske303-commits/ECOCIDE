"""Monthly mean NDVI, Kherson vs Tulcea (descriptive; the DiD estimate is in
generate_model_results.py). Reads the same data/ndvi files as the models."""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

import eco_core as ec
import eco_style as st


def main():
    st.apply()
    data = ec.load_all()
    fig, ax = plt.subplots(figsize=(10, 4.8))
    for z in ["kherson", "tulcea"]:
        d = data[z]
        ax.plot(d["date"], d["ndvi"], marker="o", ms=3.5, lw=1.8, color=st.ZONE_COLORS[z],
                label=st.ZONE_LABELS[z] + (" — treatment" if z == "kherson" else " — primary control"))
    ev = pd.Timestamp("2023-06-06")
    ax.axvline(ev, color="#333333", ls="--", lw=1)
    ax.annotate("Kakhovka Dam destroyed\n6 June 2023", xy=(ev, ax.get_ylim()[1]), xytext=(6, -4),
                textcoords="offset points", va="top", fontsize=8.5)
    ax.set_ylabel("Monthly mean NDVI")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, fontsize=9)
    ax.set_title("Monthly NDVI, Kherson Oblast vs Tulcea County, Jan 2022 – Nov 2024")
    fig.text(0.01, -0.10, "Sentinel-2 L2A via Sentinel Hub Statistical API; GADM polygons; cloud, shadow, cirrus, snow and water masked; per-pixel monthly median on a 0.002° grid. "
             "Descriptive only.", fontsize=7.5, color="#555555")
    st.save(fig, "outputs/plots/ndvi_comparison.png")


if __name__ == "__main__":
    main()
