"""Checks of the Registered Revision 2 helpers (v2/analysis/r2lib.py) on synthetic data.

    python tests/test_r2lib.py        (or: python -m pytest tests)

1. Event-study coefficients estimated with 2018 left out are correctly re-expressed relative to the
   2016–2018 mean and relative to 2021 (point estimates and standard errors).
2. A known effect in 2023–24 is recovered, and the pre-trend test does not reject under parallel trends.
3. The Addendum 2 checksum check passes on the approved file and fails on a changed one.
"""
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v2", "analysis"))
import v2lib as L  # noqa: E402
import r2lib as R2L  # noqa: E402

YEARS = list(range(2016, 2025))
EV = [y for y in YEARS if y != 2018]


def fit_event(rng, effect=-0.05, N=3000):
    unit = np.repeat(np.arange(N), 9)
    yr = np.tile(np.array(YEARS), N)
    treat = np.repeat(rng.random(N) < 0.3, 9).astype(float)
    clus = np.repeat(rng.integers(0, 40, N), 9)
    y = np.repeat(rng.normal(0.4, 0.05, N), 9) + 0.01 * (yr - 2016) + effect * treat * (yr >= 2023) \
        + rng.normal(0, 0.02, N * 9)
    X = np.column_stack([treat * (yr == t) for t in EV])
    g_year = np.unique(yr, return_inverse=True)[1]
    return L.fe_ols(y, X, [unit, g_year], np.ones(len(y)), clus, [f"F_x_{t}" for t in EV])


def test_transform_and_recovery():
    rng = np.random.default_rng(3)
    fit = fit_event(rng)
    out = R2L.event_summary(fit, EV)
    c = dict(zip(EV, fit["coef"]))
    c[2018] = 0.0
    base = (c[2016] + c[2017] + c[2018]) / 3
    rel = {r["year"]: r for r in out["relative_to_2016_2018_mean"]}
    rel21 = {r["year"]: r for r in out["relative_to_2021"]}
    for y in YEARS:
        assert abs(rel[y]["coef"] - (c[y] - base)) < 1e-12
        assert abs(rel21[y]["coef"] - (c[y] - c[2021])) < 1e-12
    # SE of (c_2023 - c_2021) from the vcov directly
    i, j = EV.index(2023), EV.index(2021)
    V = fit["vcov"]
    se = np.sqrt(V[i, i] + V[j, j] - 2 * V[i, j])
    assert abs(rel21[2023]["se"] - se) < 1e-12
    assert abs(rel[2023]["coef"] + 0.05) < 0.005 and abs(rel[2024]["coef"] + 0.05) < 0.005
    assert sum(abs(rel[y]["coef"]) < 0.005 for y in range(2016, 2023)) == 7
    assert out["pretrend_joint_p"] > 0.01


def test_checksum():
    root = os.path.join(HERE, "..")
    tmp = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(tmp, "v2"))
        shutil.copy(os.path.join(root, R2L.ADDENDUM), tmp)
        shutil.copy(os.path.join(root, R2L.DEVIATIONS), os.path.join(tmp, "v2"))
        cwd = os.getcwd()
        os.chdir(tmp)
        try:
            R2L.check_addendum()
            with open(R2L.ADDENDUM, "a", encoding="utf-8") as fh:
                fh.write("\nchanged\n")
            try:
                R2L.check_addendum()
                raise AssertionError("changed addendum was not detected")
            except SystemExit:
                pass
        finally:
            os.chdir(cwd)
    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    test_transform_and_recovery()
    print("1-2 event-study transformation and recovery: ok")
    test_checksum()
    print("3 Addendum 2 checksum check: ok")
