"""Primary Difference-in-Differences model: Kherson (treatment) vs Tulcea (control).

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    r = ec.did(data)
    print("PRIMARY DiD — Kherson vs Tulcea, event month June 2023")
    print("  ", ec.fmt(r))
    print(f"  R² (gap series) = {r['r2']:.3f}")
    s = ec.did(data, month_fe=True)
    print("SAME MODEL + zone-specific month-of-year effects (seasonality check)")
    print("  ", ec.fmt(s))
    # transparency export: the exact monthly series the model is fitted to
    g = ec.gap_series(data, "kherson", ["tulcea"])
    g["post"] = (g["date"] >= ec.EVENT_DATE).astype(int)
    g.to_csv("data/did_panel_ndvi.csv", index=False)
    print("Saved: data/did_panel_ndvi.csv")


if __name__ == "__main__":
    main()
