"""Helpers for Registered Revision 2 (ANALYSIS_PLAN_v2_ADDENDUM_2.md); the estimation engine is v2lib."""
import hashlib
import os
import re

import numpy as np
from scipy.stats import f as fdist

import v2lib as L

ADDENDUM = "docs/preregistration/ANALYSIS_PLAN_v2_ADDENDUM_2.md"
DEVIATIONS = "v2/DEVIATIONS.md"
BASE = [2016, 2017, 2018]
DEF = [2019, 2020, 2021]
EV_DROP = 2018                      # R7: event studies leave out 2018 and are reported relative to 2016–2018
RES = 231.656358


def sha256(path):
    """SHA-256 of the file with line endings normalised to LF (Windows checkouts may use CRLF)."""
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


def check_addendum():
    """Stops the run if ANALYSIS_PLAN_v2_ADDENDUM_2.md differs from the version whose SHA-256 is
    recorded in v2/DEVIATIONS.md §6 (the approved version)."""
    if not os.path.exists(ADDENDUM):
        raise SystemExit(f"{ADDENDUM} not found (run from the repository root).")
    text = open(DEVIATIONS, encoding="utf-8").read()
    m = re.search(r"Addendum 2 SHA-256[^`]*`([0-9a-f]{64})`", text)
    if not m:
        raise SystemExit("No Addendum 2 checksum in v2/DEVIATIONS.md §6.")
    now = sha256(ADDENDUM)
    if now != m.group(1):
        raise SystemExit(f"{ADDENDUM} changed after approval (SHA-256 {now[:12]}… ≠ {m.group(1)[:12]}…). "
                         "Record the change as a deviation before running.")
    return now


def conley_set(fit, j, xy, unit, cutoffs=(25, 50, 100), cell_m=4 * RES * 5):
    out = {}
    b = fit["coef"][j]
    for km in cutoffs:
        se = L.conley_se(fit, j, xy, unit, cutoff_m=km * 1000, cell_m=cell_m)
        out[f"{km}km"] = {"se": se, "p": float(2 * L.norm.sf(abs(b / se)))}
    return out


def event_summary(fit, ev_years, k0=0, df=None):
    """Event-study coefficients c_y (y in ev_years, 2018 left out) -> relative to the 2016–2018 mean
    and relative to 2021, joint pre-trend test (all pre-war years = 0 relative to 2018), and the
    Rambachan–Roth relative-magnitudes interval for 2023–24 (reference 2018)."""
    k = len(ev_years)
    c = fit["coef"][k0:k0 + k]
    V = fit["vcov"][k0:k0 + k, k0:k0 + k]
    idx = {y: i for i, y in enumerate(ev_years)}
    years = sorted(ev_years + [EV_DROP])

    def transform(ref_weights):
        M = np.zeros((len(years), k))
        for r, y in enumerate(years):
            if y in idx:
                M[r, idx[y]] += 1.0
            for yy, wgt in ref_weights.items():
                if yy in idx:
                    M[r, idx[yy]] -= wgt
        est = M @ c
        se = np.sqrt(np.maximum(np.diag(M @ V @ M.T), 0))
        return [{"year": y, "coef": float(est[r]), "se": float(se[r])} for r, y in enumerate(years)]

    pre = [y for y in ev_years if y <= 2021]
    pi = [idx[y] for y in pre]
    bp, Vp = c[pi], V[np.ix_(pi, pi)]
    Fs = float(bp @ np.linalg.solve(Vp, bp)) / len(pi)
    G = fit["G"] if df is None else df
    rr = L.rr_bounds(c, V, ev_years, ref=EV_DROP, pre=pre, post_targets=[2023, 2024])
    return {"relative_to_2016_2018_mean": transform({y: 1 / 3 for y in BASE}),
            "relative_to_2021": transform({2021: 1.0}),
            "pretrend_years": pre, "pretrend_joint_F": Fs, "pretrend_joint_p": float(fdist.sf(Fs, len(pi), G - 1)),
            "rambachan_roth_ref2018": rr}


def fixed_panel(Y, min_years):
    return np.isfinite(Y).sum(1) >= min_years
