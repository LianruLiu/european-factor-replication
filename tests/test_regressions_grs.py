"""Tests for time-series regressions and the GRS test.

Reference values come from the committed replication outputs
(results/tables/) produced by this same codebase.
"""
import numpy as np
import pandas as pd
import pytest

from factorlab.models.specs import FF3, FF5
from factorlab.tests import grs_test, run_regressions


@pytest.fixture(scope="module")
def ff3_res(aligned):
    fcols = ["Mkt-RF", "SMB", "HML"]
    Y = aligned[[c for c in aligned.columns if c not in
                 ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]]]
    Y = Y.sub(aligned["RF"], axis=0)
    return run_regressions(Y, aligned[fcols], FF3), Y


def test_ff3_small_growth_alpha(ff3_res):
    res, _ = ff3_res
    # committed results/tables/regression_ff3.csv: -5.165
    assert res.alpha["SMALL LoBM"] * 12 == pytest.approx(-5.165, abs=5e-3)
    assert res.t_alpha["SMALL LoBM"] == pytest.approx(-4.942, abs=1e-2)


def test_ff3_loadings_monotone_in_hml(ff3_res):
    res, _ = ff3_res
    # HML loading rises with book-to-market inside the smallest-size quintile
    small = [c for c in res.beta.index if c.startswith("SMALL")]
    hml_betas = res.beta.loc[small, "HML"].values
    assert all(np.diff(hml_betas) > 0)


def test_grs_reproduces_committed_values(ff3_res, aligned):
    res, _ = ff3_res
    F, p = grs_test(res.alpha, res.resid, aligned[FF3.factors])
    # committed results/tables/grs_test.csv: F=3.046066, p=0.000002
    assert F == pytest.approx(3.046066, rel=1e-4)
    assert p < 1e-5


def test_grs_zero_alphas_give_zero():
    rng = np.random.default_rng(1)
    E = pd.DataFrame(rng.normal(size=(200, 5)))
    F_ = pd.DataFrame(rng.normal(size=(200, 3)))
    Fstat, p = grs_test(pd.Series(np.zeros(5)), E, F_)
    assert Fstat == pytest.approx(0.0, abs=1e-12)
    assert p == pytest.approx(1.0)


def test_hac_keeps_coefficients(aligned):
    fcols = FF5.factors
    pcols = [c for c in aligned.columns if c not in
             ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]]
    Y = aligned[pcols].sub(aligned["RF"], axis=0)
    plain = run_regressions(Y, aligned[fcols], FF5)
    hac = run_regressions(Y, aligned[fcols], FF5,
                          cov_type="HAC", cov_kwds={"maxlags": 6})
    pd.testing.assert_frame_equal(plain.beta, hac.beta)
    # standard errors (hence t-stats) do change
    assert not np.allclose(plain.t_alpha.values, hac.t_alpha.values)
