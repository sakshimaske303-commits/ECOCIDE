"""Placebo in time for the pooled four-county panel (fake date June 2022).

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    r = ec.did(data, controls=ec.CONTROLS, event_date="2022-06-01", end="2023-06-01")
    print("POOLED PLACEBO TEST (fake treatment date: June 2022)")
    print("  ", ec.fmt(r))


if __name__ == "__main__":
    main()
