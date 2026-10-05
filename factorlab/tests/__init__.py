"""Time-series tests: OLS regressions and the GRS joint-alpha test."""
from factorlab.tests.grs import grs_test
from factorlab.tests.timeseries import RegressionResult, run_regressions

__all__ = ["RegressionResult", "grs_test", "run_regressions"]
