"""Loads the results files the dashboard reads its numbers from. No statistical
number is typed into any page.

  R      Study 1 (Kherson vs Romania): outputs/model_results.json (generate_model_results.py)
  S2     Study 2, pre-registered:      outputs/v2/study2_summary.json (v2/analysis/run_all.py)
  R1     Study 2, registered revision: outputs/v2/r1_summary.json (v2/analysis/run_revision.py)
  H1R    Study 2, H1 details:          outputs/v2/h1_results.json (v2/analysis/a3_h1.py)
  X1     Study 2, exploratory checks:  outputs/v2/x1_review_diagnostics.json (v2/analysis/x1_review_diagnostics.py)
  FLOOD  UNOSAT flood table:          outputs/flood_extent_table.json (flood_progression.py)"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return json.load(f)


R = _load("outputs/model_results.json")
FLOOD = _load("outputs/flood_extent_table.json")
S2 = _load("outputs/v2/study2_summary.json")
R1 = _load("outputs/v2/r1_summary.json")
H1R = _load("outputs/v2/h1_results.json")
X1 = _load("outputs/v2/x1_review_diagnostics.json") if os.path.exists(
    os.path.join(ROOT, "outputs/v2/x1_review_diagnostics.json")) else None
NAMES = {"kherson": "Kherson", "tulcea": "Tulcea", "galati": "Galați", "braila": "Brăila", "constanta": "Constanța"}


def p(x):
    return "<0.001" if x < 0.001 else f"{x:.3f}"


def pv(x):
    """'p < 0.001' or 'p = 0.037' for inline text."""
    return "p < 0.001" if x < 0.001 else f"p = {x:.3f}"


def c(m, d=4):
    return f"{m['coef']:+.{d}f}"


def ci(m):
    return f"[{m['ci'][0]:+.3f}, {m['ci'][1]:+.3f}]"


def flood_row(date):
    return next(r for r in FLOOD["layers"] if r["date"] == date)


def sig(x):
    return "significant at 5%" if x < 0.05 else "not significant at 5%"
