"""Tests for data loaders."""
import numpy as np
import pandas as pd
import pytest

from factorlab.data.loaders import (
    load_french_factors,
    load_french_portfolios,
)

from conftest import FACTORS_CSV, PORTS_CSV


def test_parse_french_factors_shape():
    df = load_french_factors(FACTORS_CSV)
    assert list(df.columns) == ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]
    assert isinstance(df.index, pd.DatetimeIndex)
    # monthly sample Jul 1990 - Aug 2026
    assert len(df) == 434
    assert str(df.index[0].date()) == "1990-07-01"
    assert str(df.index[-1].date()) == "2026-08-01"


def test_parse_french_portfolios_shape():
    df = load_french_portfolios(PORTS_CSV)
    assert df.shape == (434, 25)
    assert "SMALL LoBM" in df.columns


def test_missing_sentinel_becomes_nan(tmp_path):
    p = tmp_path / "f.csv"
    p.write_text(
        ",Mkt-RF,SMB\n"
        "199001,1.5,-99.99\n"
        "199002,-0.5,0.3\n"
    )
    df = load_french_factors(p)
    assert np.isnan(df.loc["1990-01-01", "SMB"])
    assert df.loc["1990-01-01", "Mkt-RF"] == pytest.approx(1.5)
