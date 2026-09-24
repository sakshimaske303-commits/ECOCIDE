"""Four-county control panel: pooled DiD and Kherson against each control individually.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    print("POOLED DiD — Kherson vs mean of Tulcea, Galați, Constanța, Brăila")
    print("  ", ec.fmt(ec.did(data, controls=ec.CONTROLS)))
    print("  + zone-specific seasonality:", ec.fmt(ec.did(data, controls=ec.CONTROLS, month_fe=True)))
    print("\nPER-CONTROL (Kherson vs each control alone)")
    for z in ec.CONTROLS:
        print(f"  vs {z:10s}", ec.fmt(ec.did(data, controls=[z])))
    g = ec.gap_series(data, "kherson", ec.CONTROLS)
    g["post"] = (g["date"] >= ec.EVENT_DATE).astype(int)
    g.to_csv("data/did_panel_ndvi_multi_control.csv", index=False)
    print("Saved: data/did_panel_ndvi_multi_control.csv")


if __name__ == "__main__":
    main()
