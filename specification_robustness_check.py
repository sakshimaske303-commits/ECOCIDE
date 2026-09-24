"""Specification robustness for the primary model: HAC lag length (1–6) and log(NDVI).

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

import numpy as np


def main():
    data = ec.load_all()
    print("HAC LAG-LENGTH SENSITIVITY")
    for L in range(1, 7):
        r = ec.did(data, maxlags=L)
        print(f"  maxlags={L}: coef={r['coef']:+.4f}  p={r['p']:.3f}")
    r = ec.did(data, log=True)
    print("\nlog(NDVI):", ec.fmt(r), f"= {100*(np.exp(r['coef'])-1):.1f}% proportional change")


if __name__ == "__main__":
    main()
