"""Loads the single results file every dashboard page reads its numbers from
(outputs/model_results.json, written by generate_model_results.py) and the
UNOSAT flood table (outputs/flood_extent_table.json, written by
flood_progression.py). No statistical number is typed into any page."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


R = _load("outputs/model_results.json")
FLOOD = _load("outputs/flood_extent_table.json")
NAMES = {"kherson": "Kherson", "tulcea": "Tulcea", "galati": "Galați", "braila": "Brăila", "constanta": "Constanța"}


def p(x):
    return "<0.001" if x < 0.001 else f"{x:.3f}"


def c(m, d=4):
    return f"{m['coef']:+.{d}f}"


def ci(m):
    return f"[{m['ci'][0]:+.3f}, {m['ci'][1]:+.3f}]"


def flood_row(date):
    return next(r for r in FLOOD["layers"] if r["date"] == date)


def sig(x):
    return "significant at 5%" if x < 0.05 else "not significant at 5%"
