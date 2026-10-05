"""Descriptive statistics for factor premia."""
from __future__ import annotations

import numpy as np
import pandas as pd


def premia_stats(factors: pd.DataFrame, periods_per_year: int = 12) -> pd.DataFrame:
    """Annualized mean, volatility, t-stat of the mean, and Sharpe ratio.

    Parameters
    ----------
    factors : DataFrame of monthly factor returns in percent.
    """
    out = []
    for col in factors.columns:
        x = factors[col].dropna()
        mu, sd = x.mean(), x.std()
        n = len(x)
        out.append({
            "factor": col,
            "ann_mean_pct": mu * periods_per_year,
            "ann_vol_pct": sd * np.sqrt(periods_per_year),
            "t_mean": mu / (sd / np.sqrt(n)),
            "sharpe": (mu / sd) * np.sqrt(periods_per_year),
            "n_obs": n,
        })
    return pd.DataFrame(out).set_index("factor")


def rolling_mean(series: pd.Series, window: int = 12) -> pd.Series:
    """Trailing rolling mean (e.g. 12-month rolling value premium)."""
    return series.rolling(window).mean()
