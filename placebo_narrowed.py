"""Placebo for the narrowed baseline: fake date March 2023 within Jan–May 2023.

Same specification as did_model_narrowed.py (gap ~ post). Only 5 months are
available, so maxlags=1 and the result is fragile in either direction.

Uses the shared engine in eco_core.py (DiD on the monthly treated-minus-control
NDVI gap, Newey-West HAC maxlags=3, t-distribution) so this script prints
exactly the numbers reported in the paper and stored by
generate_model_results.py.
"""
import eco_core as ec

def main():
    data = ec.load_all()
    r = ec.did(data, event_date="2023-03-01", start="2023-01-01", end="2023-06-01", maxlags=1)
    print("PLACEBO TEST (narrowed window Jan–May 2023, fake date: March 2023)")
    print("  ", ec.fmt(r))


if __name__ == "__main__":
    main()
