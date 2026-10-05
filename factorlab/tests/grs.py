"""Gibbons-Ross-Shanken (1989) F-test of the joint hypothesis alpha = 0."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


def grs_test(
    alphas: pd.Series | np.ndarray,
    resid: pd.DataFrame | np.ndarray,
    factors: pd.DataFrame | np.ndarray,
) -> tuple[float, float]:
    """GRS F-test that all time-series intercepts are jointly zero.

    Parameters
    ----------
    alphas  : (N,) intercepts from the time-series regressions.
    resid   : (T, N) OLS residuals.
    factors : (T, K) factor returns used in the regressions.

    Returns
    -------
    (F_stat, p_value) with F ~ F(N, T - N - K) under H0.
    """
    a = np.asarray(alphas, dtype=float)
    E = np.asarray(resid, dtype=float)
    F_ = np.asarray(factors, dtype=float)
    T, N = E.shape
    K = F_.shape[1]
    S = np.cov(E, rowvar=False)          # (N, N) residual covariance
    mu = F_.mean(axis=0)                 # (K,) factor means
    Om = np.cov(F_, rowvar=False)        # (K, K) factor covariance
    theta2 = float(a @ np.linalg.inv(S) @ a)
    sharpe2_f = float(mu @ np.linalg.inv(Om) @ mu)
    F = (T / N) * ((T - N - K) / (T - K - 1)) * theta2 / (1 + sharpe2_f)
    p = float(1 - stats.f.cdf(F, N, T - N - K))
    return F, p
