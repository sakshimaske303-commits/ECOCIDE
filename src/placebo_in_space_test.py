"""Placebo in space / exact randomization inference across the five geographic units.

Each zone is assigned 'treated' status in turn against the other four
(Conley & Taber, 2011). With five units the smallest attainable exact
p-value is 1/5 = 0.20.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    res = {z: ec.did(data, treated=z, controls=[c for c in ec.ALL_ZONES if c != z]) for z in ec.ALL_ZONES}
    for z, r in res.items():
        tag = "  <- real treated unit" if z == "kherson" else ""
        print(f"  {z:10s} coef={r['coef']:+.4f}  HAC p={r['p']:.3f}{tag}")
    k = res["kherson"]["coef"]
    one = 1 + sum(1 for z in res if z != "kherson" and res[z]["coef"] < k)
    two = 1 + sum(1 for z in res if z != "kherson" and abs(res[z]["coef"]) > abs(k))
    print(f"\nKherson rank: one-sided {one}/5 (exact p={one/5:.2f}); two-sided {two}/5 (exact p={two/5:.2f})")


if __name__ == "__main__":
    main()
