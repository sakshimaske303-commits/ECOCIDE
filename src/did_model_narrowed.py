"""Narrowed-baseline DiD (secondary): pre-period restricted to Jan–May 2023.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    r = ec.did(data, start="2023-01-01")
    print("NARROWED-BASELINE DiD — Kherson vs Tulcea, Jan 2023 – Nov 2024")
    print("  ", ec.fmt(r))
    g = ec.gap_series(data, "kherson", ["tulcea"])
    g = g[g["date"] >= "2023-01-01"].copy()
    g["post"] = (g["date"] >= ec.EVENT_DATE).astype(int)
    g.to_csv("data/did_panel_ndvi_narrowed.csv", index=False)
    print("Saved: data/did_panel_ndvi_narrowed.csv")


if __name__ == "__main__":
    main()
