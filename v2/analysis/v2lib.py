"""Shared engine for the Study 2 analysis (ANALYSIS_PLAN_v2.md §5–§7).

Everything is written with numpy/scipy only so each step is transparent:
  * load_outcomes()      annual pixel outcomes with the ≥5-observation rule
  * weather()            July–October ERA5-Land precipitation (mm) and temperature (°C)
  * demean()             weighted multi-way fixed-effects projection (alternating projections)
  * fe_ols()             weighted OLS after FE projection, cluster-robust vcov
  * wild_cluster_p()     restricted wild cluster bootstrap (WCR), Rademacher, for one coefficient
  * conley_se()          spatial HAC (Bartlett kernel, 25 km) on cell-aggregated scores
  * holm()               Holm step-down adjustment
  * rr_bounds()          relative-magnitudes sensitivity (Rambachan & Roth 2023)
"""
import calendar
import os

import numpy as np
import xarray as xr
from scipy import sparse
from scipy.spatial import cKDTree
from scipy.stats import norm, t as tdist

D = "data/v2"
YEARS = list(range(2016, 2025))
PRE = [2016, 2017, 2018, 2019, 2020, 2021]
WAR = [2022]
POST = [2023, 2024]
MIN_OBS = 5          # plan §5: ≥ 5 valid July–October observations
MIN_YEARS = 7        # plan §5: fixed panel, ≥ 7 of 9 years


# ---------------------------------------------------------------- data
def layers():
    return dict(np.load(f"{D}/derived/layers.npz"))


def load_outcomes(idx, var="ndvi_jo", nvar="n_jo", min_obs=MIN_OBS, years=YEARS):
    """Matrix (len(idx) × len(years)) of an annual outcome at flat pixel indices idx.
    Values with fewer than min_obs valid observations are set to NaN."""
    out = np.full((len(idx), len(years)), np.nan, np.float32)
    for k, y in enumerate(years):
        ds = xr.open_dataset(f"{D}/annual/annual_{y}.nc")
        v = ds[var].values.ravel()[idx] / 10000.0
        if nvar is not None:
            n = ds[nvar].values.ravel()[idx]
            v = np.where(n >= min_obs, v, np.nan)
        out[:, k] = v
        ds.close()
    return out


def weather(lon, lat, years=YEARS):
    """July–October total precipitation (mm) and mean 2 m temperature (°C) of each
    pixel's ERA5-Land 0.1° cell (nearest land cell). Returns two (N × years) arrays."""
    e = xr.open_dataset(f"{D}/era5land_monthly_2015_2024.nc")
    tname = "valid_time" if "valid_time" in e.coords else "time"
    times = e[tname].values.astype("datetime64[M]").astype(object)
    elat, elon = e.latitude.values, e.longitude.values
    t2m, tp = e.t2m.values, e.tp.values
    land = np.isfinite(t2m[0])
    LA, LO = np.meshgrid(elat, elon, indexing="ij")
    tree = cKDTree(np.c_[LA[land], LO[land]])
    _, k = tree.query(np.c_[lat, lon])
    li, lo = np.where(land)
    ci, cj = li[k], lo[k]
    P = np.zeros((len(lon), len(years)), np.float32)
    T = np.zeros((len(lon), len(years)), np.float32)
    for n, y in enumerate(years):
        ps, ts = 0.0, 0.0
        for m in (7, 8, 9, 10):
            ti = [i for i, d in enumerate(times) if d.year == y and d.month == m][0]
            days = calendar.monthrange(y, m)[1]
            ps = ps + tp[ti][ci, cj] * days * 1000.0
            ts = ts + (t2m[ti][ci, cj] - 273.15) / 4
        P[:, n], T[:, n] = ps, ts
    return P, T


def long_format(Y, extra=None):
    """Stack an (N × T) matrix into long vectors; drop NaN outcomes."""
    N, T = Y.shape
    unit = np.repeat(np.arange(N), T)
    year = np.tile(np.arange(T), N)
    y = Y.ravel()
    ok = np.isfinite(y)
    out = {"y": y[ok].astype(np.float64), "unit": unit[ok], "t": year[ok]}
    if extra:
        for k, v in extra.items():
            out[k] = v.ravel()[ok].astype(np.float32)
    return out


# ---------------------------------------------------------------- estimation
def demean(X, groups, w, tol=1e-10, maxit=2000):
    """Weighted projection of columns of X off several sets of fixed effects
    (method of alternating projections). groups: list of int arrays."""
    X = np.array(X, dtype=np.float64, copy=True)
    if X.ndim == 1:
        X = X[:, None]
    wsum = [np.bincount(g, weights=w) for g in groups]
    for _ in range(maxit):
        Xold = X.copy()
        for g, ws in zip(groups, wsum):
            for j in range(X.shape[1]):
                m = np.bincount(g, weights=w * X[:, j], minlength=len(ws))
                with np.errstate(invalid="ignore", divide="ignore"):
                    m = np.where(ws > 0, m / ws, 0.0)
                X[:, j] -= m[g]
        if np.max(np.abs(X - Xold)) < tol:
            break
    return X


def fe_projector(unit, lows, w):
    """Exact weighted projection off pixel FE (unit) plus a few LOW-dimensional FE sets
    (e.g. year x oblast): within-transform by pixel, then partial out the within-transformed
    low-dimensional dummies using their small Gram matrix built from pixel-by-group sums
    (Frisch–Waugh–Lovell). Returns a function x -> M x. Same result as demean(), exact."""
    nu = unit.max() + 1
    Wi = np.bincount(unit, weights=w, minlength=nu)
    Wi_safe = np.where(Wi > 0, Wi, 1.0)
    offs, gcols = 0, []
    for g in lows:
        gcols.append(g + offs)
        offs += g.max() + 1
    Gtot = offs
    Nw = sparse.csr_matrix((np.concatenate([w] * len(lows)), (np.concatenate([unit] * len(lows)), np.concatenate(gcols))),
                           shape=(nu, Gtot))
    DWD = np.zeros((Gtot, Gtot))
    for a in range(len(lows)):
        for b in range(len(lows)):
            na, nb = lows[a].max() + 1, lows[b].max() + 1
            c = np.bincount(lows[a] * nb + lows[b], weights=w, minlength=na * nb).reshape(na, nb)
            oa, ob = gcols[a][0] - lows[a][0], gcols[b][0] - lows[b][0]
            DWD[oa:oa + na, ob:ob + nb] = c
    Gram = DWD - np.asarray((Nw.T @ sparse.diags(1.0 / Wi_safe) @ Nw).todense())
    Ginv = np.linalg.pinv(Gram)

    def proj(x):
        x = np.asarray(x, dtype=np.float64)
        xm = np.bincount(unit, weights=w * x, minlength=nu) / Wi_safe
        Dx = np.zeros(Gtot)
        for gc in gcols:
            Dx += np.bincount(gc, weights=w * x, minlength=Gtot)
        th = Ginv @ (Dx - Nw.T @ xm)
        Dth = th[gcols[0]].copy()
        for gc in gcols[1:]:
            Dth += th[gc]
        dm = np.bincount(unit, weights=w * Dth, minlength=nu) / Wi_safe
        return x - xm[unit] - Dth + dm[unit]
    return proj


def demean_fast(X, unit, lows, w):
    X = np.asarray(X)
    if X.ndim == 1:
        X = X[:, None]
    P = fe_projector(unit, lows, w)
    return np.column_stack([P(X[:, j]) for j in range(X.shape[1])])


def fe_ols(y, X, groups, w, cluster, names):
    """Weighted OLS of y on X with multi-way FE, cluster-robust (CR1) vcov.
    Returns dict with coef, se, t, p (t with G-1 df), vcov, and projected arrays."""
    Pj = fe_projector(groups[0], groups[1:], w)
    yt = Pj(y)
    Xt = np.empty((len(y), X.shape[1]), dtype=np.float64)
    for j in range(X.shape[1]):
        Xt[:, j] = Pj(X[:, j])
    del Pj
    k = Xt.shape[1]
    A = np.empty((k, k))
    c_y = np.empty(k)
    for a in range(k):
        xa = Xt[:, a] * w
        c_y[a] = xa @ yt
        for b_ in range(a, k):
            A[a, b_] = A[b_, a] = xa @ Xt[:, b_]
    Ainv = np.linalg.pinv(A)
    b = Ainv @ c_y
    e = yt - Xt @ b
    cl = np.unique(cluster, return_inverse=True)[1]
    G = cl.max() + 1
    S = np.zeros((G, X.shape[1]))
    for j in range(X.shape[1]):
        S[:, j] = np.bincount(cl, weights=w * Xt[:, j] * e, minlength=G)
    n, k = len(y), X.shape[1]
    c = G / (G - 1) * (n - 1) / max(n - k, 1)
    V = c * Ainv @ (S.T @ S) @ Ainv
    se = np.sqrt(np.diag(V))
    tt = b / se
    p = 2 * tdist.sf(np.abs(tt), G - 1)
    return {"names": names, "coef": b, "se": se, "t": tt, "p": p, "vcov": V, "G": int(G), "n": int(n),
            "yt": yt, "Xt": Xt, "e": e, "w": w, "cl": cl}


def wild_cluster_p(fit, j, B=9999, seed=20260924):
    """Restricted wild cluster bootstrap (WCR, Rademacher) p-value for H0: beta_j = 0.
    Other regressors and all FE are partialled out (Frisch–Waugh–Lovell)."""
    Xt, yt, w, cl = fit["Xt"], fit["yt"], fit["w"], fit["cl"]
    others = [i for i in range(Xt.shape[1]) if i != j]
    if others:
        O = Xt[:, others]
        Ow = O * w[:, None]
        P = np.linalg.pinv(O.T @ Ow)
        x = Xt[:, j] - O @ (P @ (Ow.T @ Xt[:, j]))
        yr = yt - O @ (P @ (Ow.T @ yt))       # restricted residual (beta_j = 0)
    else:
        x, yr = Xt[:, j], yt
    G = cl.max() + 1
    Sxy = np.bincount(cl, weights=w * x * yr, minlength=G)
    Sxx = np.bincount(cl, weights=w * x * x, minlength=G)
    den = Sxx.sum()
    # observed t (CR0 on the partialled regression, same small-sample factor as fe_ols)
    b = Sxy.sum() / den
    se = np.sqrt(np.sum((Sxy - b * Sxx) ** 2)) / den
    t_obs = b / se
    rng = np.random.default_rng(seed)
    tb = np.empty(B)
    for s in range(0, B, 1000):
        m = min(1000, B - s)
        v = rng.choice([-1.0, 1.0], size=(m, G))
        bs = (v @ Sxy) / den
        ses = np.sqrt(((v * Sxy[None, :] - bs[:, None] * Sxx[None, :]) ** 2).sum(axis=1)) / den
        tb[s:s + m] = bs / ses
    p_two = (1 + np.sum(np.abs(tb) >= abs(t_obs))) / (B + 1)
    p_lower = (1 + np.sum(tb <= t_obs)) / (B + 1)
    return {"t": float(t_obs), "p_two_sided": float(p_two), "p_one_sided_negative": float(p_lower), "B": B, "G": int(G)}


def conley_se(fit, j, xy_unit, unit, cutoff_m=25000, cell_m=2316.56):
    """Conley spatial-HAC SE for coefficient j (Bartlett kernel, cutoff 25 km).
    Scores are summed over years within each pixel (any serial correlation allowed)
    and aggregated to ~2.3 km cells before the spatial sum, which keeps the
    computation feasible for millions of pixels."""
    Xt, e, w = fit["Xt"], fit["e"], fit["w"]
    k = Xt.shape[1]
    A = np.array([[(Xt[:, a] * w) @ Xt[:, b] for b in range(k)] for a in range(k)])
    Ainv = np.linalg.pinv(A)
    cells = np.floor(xy_unit / cell_m).astype(np.int64)
    cid, cinv = np.unique(cells[:, 0] * 10_000_000 + cells[:, 1], return_inverse=True)
    cobs = cinv[unit]
    C = len(cid)
    S = np.zeros((C, k))
    for q in range(k):
        S[:, q] = np.bincount(cobs, weights=w * Xt[:, q] * e, minlength=C)
    cxy = np.zeros((C, 2))
    cnt = np.bincount(cinv, minlength=C)
    cxy[:, 0] = np.bincount(cinv, weights=xy_unit[:, 0], minlength=C) / cnt
    cxy[:, 1] = np.bincount(cinv, weights=xy_unit[:, 1], minlength=C) / cnt
    tree = cKDTree(cxy)
    pairs = tree.sparse_distance_matrix(tree, cutoff_m, output_type="coo_matrix")
    # Bartlett (linearly declining) kernel: weight 1 - d/cutoff; the uniform kernel can
    # give a non-positive variance in small samples
    K = sparse.coo_matrix((1.0 - pairs.data / cutoff_m, (pairs.row, pairs.col)), shape=(C, C)).tocsr()
    K = K + sparse.identity(C, format="csr")  # zero-distance pairs (self) are dropped by the tree
    meat = S.T @ (K @ S)
    V = Ainv @ meat @ Ainv
    return float(np.sqrt(V[j, j]))


def holm(pvals):
    p = np.asarray(pvals, float)
    order = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * p[i]))
        adj[i] = run
    return adj


def rr_bounds(beta, V, years, ref, pre, post_targets, Mbars=(0.5, 1.0, 2.0), level=0.95, nsim=20000, seed=7):
    """Relative-magnitudes sensitivity (Rambachan & Roth 2023, Delta^RM(Mbar)).

    Event-study coefficients beta (on `years`, reference year excluded) with vcov V.
    The post-reference violation may change, per year, by at most Mbar times the
    largest year-to-year change of the pre-period coefficients. With the reference
    year normalised to 0, the violation in year t is bounded by (t - ref) * Mbar * Mpre.
    Target: average effect over post_targets.

    Returns, for each Mbar, the identified-set bounds at the point estimates and a
    robust confidence interval that ALSO accounts for sampling uncertainty in Mpre:
    lower = min over draws... implemented as [theta_hat - B(Mpre_hi) - z*se, theta_hat + B(Mpre_hi) + z*se],
    where Mpre_hi is the one-sided 95% upper bound of Mpre from a parametric bootstrap
    of the event-study coefficients (conservative)."""
    years = list(years)
    b = np.asarray(beta, float)
    idx = {y: i for i, y in enumerate(years)}
    pre_seq = sorted(pre + [ref])

    def mpre(bv):
        vals = [0.0 if y == ref else bv[idx[y]] for y in pre_seq]
        return np.max(np.abs(np.diff(vals)))

    l = np.zeros(len(years))
    for y in post_targets:
        l[idx[y]] = 1.0 / len(post_targets)
    theta = float(l @ b)
    se = float(np.sqrt(l @ V @ l))
    steps = np.mean([y - ref for y in post_targets])
    M_hat = mpre(b)
    rng = np.random.default_rng(seed)
    draws = rng.multivariate_normal(b, V, size=nsim)
    M_draws = np.array([mpre(d) for d in draws])
    M_hi = float(np.quantile(M_draws, 0.95))
    z = norm.ppf(1 - (1 - level) / 2)
    out = {"theta": theta, "se": se, "Mpre_hat": float(M_hat), "Mpre_upper95": M_hi, "steps": float(steps), "bounds": {}}
    for Mb in Mbars:
        bias_hat = steps * Mb * M_hat
        bias_hi = steps * Mb * M_hi
        out["bounds"][str(Mb)] = {
            "identified_set": [theta - bias_hat, theta + bias_hat],
            "robust_ci": [theta - bias_hi - z * se, theta + bias_hi + z * se],
            "excludes_zero": bool(theta + bias_hi + z * se < 0 or theta - bias_hi - z * se > 0),
        }
    return out
