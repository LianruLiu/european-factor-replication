"""Time-series OLS regressions of test-asset excess returns on factors."""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import statsmodels.api as sm

from factorlab.models.specs import ModelSpec


@dataclass
class RegressionResult:
    """Container for one model's time-series regressions (N test assets)."""

    spec: ModelSpec
    alpha: pd.Series        # intercepts (monthly, in the data's units)
    t_alpha: pd.Series
    beta: pd.DataFrame      # factor loadings, columns = spec.factors
    t_beta: pd.DataFrame
    r2adj: pd.Series        # adjusted R^2 per test asset
    resid: pd.DataFrame     # T x N residuals
    n_obs: int


def run_regressions(
    excess_returns: pd.DataFrame,
    factors: pd.DataFrame,
    spec: ModelSpec,
    cov_type: str = "nonrobust",
    cov_kwds: dict | None = None,
) -> RegressionResult:
    """OLS of each test-asset column on ``spec.factors`` (with intercept).

    ``cov_type="HAC"`` switches to Newey-West standard errors
    (pass e.g. ``cov_kwds={"maxlags": 6}``); the GRS test always uses the
    plain OLS residuals, as in Gibbons, Ross & Shanken (1989).
    """
    X = sm.add_constant(factors[spec.factors])
    kw = dict(cov_kwds or {})
    alphas, t_alphas, betas, t_betas, r2adj, resid = [], [], [], [], [], []
    for col in excess_returns.columns:
        fit = sm.OLS(excess_returns[col], X, missing="drop").fit(
            cov_type=cov_type, cov_kwds=kw or None)
        p, t = fit.params, fit.tvalues
        alphas.append(p["const"])
        t_alphas.append(t["const"])
        betas.append([p[c] for c in spec.factors])
        t_betas.append([t[c] for c in spec.factors])
        r2adj.append(fit.rsquared_adj)
        resid.append(fit.resid)
    idx = excess_returns.columns
    return RegressionResult(
        spec=spec,
        alpha=pd.Series(alphas, index=idx),
        t_alpha=pd.Series(t_alphas, index=idx),
        beta=pd.DataFrame(betas, index=idx, columns=spec.factors),
        t_beta=pd.DataFrame(t_betas, index=idx, columns=spec.factors),
        r2adj=pd.Series(r2adj, index=idx),
        resid=pd.DataFrame(resid, index=idx).T,
        n_obs=int(X.shape[0]),
    )
