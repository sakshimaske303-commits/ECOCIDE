"""Bonferroni and Benjamini–Hochberg (1995) correction across the 11 event-study quarters.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    rows = ec.event_study(data)
    thr, bonf, bh = ec.bonferroni_bh([r["p"] for r in rows])
    print(f"{len(rows)} quarterly coefficients; Bonferroni threshold p < {thr:.5f}\n")
    print(f"{'quarter':>8s} {'months':>20s} {'coef':>9s} {'p':>8s}  raw  bonf  BH")
    for r, b1, b2 in zip(rows, bonf, bh):
        print(f"{r['quarter']:+8d} {r['months']:>20s} {r['coef']:+9.4f} {r['p']:8.4f}  "
              f"{'*' if r['p'] < 0.05 else ' ':>3s}  {'*' if b1 else ' ':>4s}  {'*' if b2 else ' ':>2s}")


if __name__ == "__main__":
    main()
