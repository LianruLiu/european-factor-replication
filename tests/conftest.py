"""Shared fixtures for the factorlab test suite."""
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
RAW = REPO / "data" / "raw"
FACTORS_CSV = RAW / "Europe_5_Factors.csv"
PORTS_CSV = RAW / "Europe_25_Portfolios_ME_BE-ME.csv"
EXAMPLE_CONFIG = REPO / "examples" / "europe_ff3_ff5" / "config.yaml"


@pytest.fixture(scope="session")
def factors():
    from factorlab.data.loaders import load_french_factors
    return load_french_factors(FACTORS_CSV).loc["1990-07":"2026-08"]


@pytest.fixture(scope="session")
def portfolios():
    from factorlab.data.loaders import load_french_portfolios
    return load_french_portfolios(PORTS_CSV).loc["1990-07":"2026-08"]


@pytest.fixture(scope="session")
def aligned(factors, portfolios):
    return factors.join(portfolios, how="inner").dropna()
