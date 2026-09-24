"""Sensitivity to low-coverage months (valid-pixel fraction below 15% or 25%).

The polygon extraction caps valid coverage at roughly the polygon-to-bounding-
box area ratio (≈43–66%), so a 50% threshold would flag ordinary months.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    print("ALL MONTHS:", ec.fmt(ec.did(data)))
    for thr in (0.15, 0.25):
        flagged = {z: list(data[z].loc[data[z]["valid_frac"] < thr, "date"].dt.strftime("%Y-%m")) for z in ec.ALL_ZONES}
        print(f"\nThreshold {thr:.0%}: flagged", {z: m for z, m in flagged.items() if m})
        print("  primary:", ec.fmt(ec.did(data, min_valid=thr)))
        print("  pooled: ", ec.fmt(ec.did(data, controls=ec.CONTROLS, min_valid=thr)))


if __name__ == "__main__":
    main()
