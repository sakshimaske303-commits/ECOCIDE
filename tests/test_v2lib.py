"""Checks of the Study 2 estimation engine (v2/analysis/v2lib.py) on synthetic data.

    python tests/test_v2lib.py        (or: python -m pytest tests)

1. The fixed-effects projection gives exactly the same coefficients as an
   explicit dummy-variable (LSDV) regression.
2. The cluster-robust (CR1) standard errors equal a direct sandwich calculation.
3. Under a true null, the wild cluster bootstrap rejects at about the nominal 5 % rate.
4. Holm adjustment matches a hand calculation.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "v2", "analysis"))
import v2lib as L  # noqa: E402

N, T, G, S = 400, 9, 40, 4


def panel(rng, effect=0.3):
    unit = np.repeat(np.arange(N), T)
    t = np.tile(np.arange(T), N)
    strat = np.repeat(rng.integers(0, S, N), T)
    clus = np.repeat(rng.integers(0, G, N), T)
    F = np.repeat((rng.random(N) < 0.3).astype(float), T)
    post, war = (t >= 7).astype(float), (t == 6).astype(float)
    P = rng.normal(size=N * T)
    w = np.repeat(rng.uniform(0.5, 2, N), T)
    y = (np.repeat(rng.normal(size=N), T) + rng.normal(size=(S, T))[strat, t] + effect * F * post
         - 0.1 * F * war + 0.2 * P + rng.normal(size=(G, T))[clus, t] * 0.5 + rng.normal(size=N * T))
    X = np.column_stack([F * post, F * war, P])
    g2 = np.unique(strat * 100 + t, return_inverse=True)[1]
    return y, X, unit, g2, w, clus


def test_fe_equals_lsdv_and_cluster_se():
    rng = np.random.default_rng(0)
    y, X, unit, g2, w, clus = panel(rng)
    fit = L.fe_ols(y, X, [unit, g2], w, clus, ["b", "d", "p"])
    Z = np.column_stack([X, np.eye(N)[unit], np.eye(g2.max() + 1)[g2][:, 1:]])
    sw = np.sqrt(w)
    bb = np.linalg.lstsq(Z * sw[:, None], y * sw, rcond=None)[0]
    assert np.allclose(fit["coef"], bb[:3], atol=1e-8)
    e = y - Z @ bb
    Xt = fit["Xt"]
    Ai = np.linalg.inv((Xt * w[:, None]).T @ Xt)
    Sc = np.column_stack([np.bincount(clus, weights=w * Xt[:, j] * e, minlength=G) for j in range(3)])
    n, k = len(y), 3
    V = G / (G - 1) * (n - 1) / (n - k) * Ai @ Sc.T @ Sc @ Ai
    assert np.allclose(fit["se"], np.sqrt(np.diag(V)), rtol=1e-6)


def test_wild_bootstrap_size():
    rng = np.random.default_rng(1)
    rej, R = 0, 200
    for s in range(R):
        y, X, unit, g2, w, clus = panel(rng, effect=0.0)
        fit = L.fe_ols(y, X, [unit, g2], w, clus, ["b", "d", "p"])
        rej += L.wild_cluster_p(fit, 0, B=399, seed=s)["p_two_sided"] < 0.05
    assert 0.01 <= rej / R <= 0.10, rej / R


def test_holm():
    assert np.allclose(L.holm([0.5968, 0.0001]), [0.5968, 0.0002])
    assert np.allclose(L.holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])


if __name__ == "__main__":
    test_fe_equals_lsdv_and_cluster_se()
    test_wild_bootstrap_size()
    test_holm()
    print("all v2lib checks passed")
