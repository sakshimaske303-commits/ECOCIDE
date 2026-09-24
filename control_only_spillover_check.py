"""Control-only divergence check (Kherson excluded).

Each Romanian county is treated in turn against the other three at the real
June 2023 cutoff. A significant result shows that county diverged on its own;
it does NOT identify why (spillover, markets, weather, land use...). The file
name is kept for continuity; the paper calls this the control-divergence check.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    print("CONTROL-ONLY DIVERGENCE CHECK (Kherson excluded)")
    for z in ec.CONTROLS:
        r = ec.did(data, treated=z, controls=[c for c in ec.CONTROLS if c != z])
        flag = "  <-- p<0.05" if r["p"] < 0.05 else ""
        print(f"  {z:10s} vs other 3: coef={r['coef']:+.4f}  HAC p={r['p']:.3f}{flag}")


if __name__ == "__main__":
    main()
