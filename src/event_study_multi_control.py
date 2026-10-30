"""Quarterly event study on the Kherson minus four-county-mean gap.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    print("EVENT STUDY — Kherson minus mean of 4 controls (ref: Mar–May 2023)")
    for r in ec.event_study(data, controls=ec.CONTROLS):
        sig = "***" if r["p"] < 0.01 else "**" if r["p"] < 0.05 else "*" if r["p"] < 0.1 else ""
        print(f"  Q{r['quarter']:+d}  {r['months']:20s} coef={r['coef']:+.4f}  p={r['p']:.4f} {sig}")


if __name__ == "__main__":
    main()
