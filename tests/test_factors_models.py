"""Tests for factor statistics and model specs."""
import numpy as np
import pandas as pd
import pytest

from factorlab.factors.stats import premia_stats, rolling_mean
from factorlab.models.specs import (
    FF3, FF5, CARHART4, CAPM, custom_model, from_config,
)


def test_premia_stats_against_manual():
    rng = np.random.default_rng(0)
    x = pd.Series(rng.normal(0.5, 2.0, size=120))
    df = pd.DataFrame({"F": x})
    s = premia_stats(df).loc["F"]
    assert s["ann_mean_pct"] == pytest.approx(x.mean() * 12)
    assert s["ann_vol_pct"] == pytest.approx(x.std() * np.sqrt(12))
    assert s["t_mean"] == pytest.approx(x.mean() / (x.std() / np.sqrt(120)))
    assert s["sharpe"] == pytest.approx(x.mean() / x.std() * np.sqrt(12))
    assert s["n_obs"] == 120


def test_rolling_mean():
    s = pd.Series([1.0, 2.0, 3.0, 4.0])
    assert rolling_mean(s, 2).tolist()[1:] == [1.5, 2.5, 3.5]


def test_presets():
    assert FF3.factors == ["Mkt-RF", "SMB", "HML"]
    assert FF5.factors == ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
    assert CARHART4.factors[-1] == "MOM"
    assert CAPM.k == 1


def test_custom_and_from_config():
    m = custom_model("MyModel", ["A", "B"])
    assert m.name == "MyModel" and m.k == 2
    specs = from_config({"X": ["A"], "Y": ["A", "B"]})
    assert [s.name for s in specs] == ["X", "Y"]
    with pytest.raises(ValueError):
        custom_model("Empty", [])
