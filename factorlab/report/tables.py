"""CSV table writers."""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from factorlab.tests.timeseries import RegressionResult


def write_summary_tables(
    factor_stats: pd.DataFrame,
    grs_rows: list[dict],
    tables_dir: str | Path,
) -> None:
    tables_dir = Path(tables_dir)
    tables_dir.mkdir(parents=True, exist_ok=True)
    factor_stats.to_csv(tables_dir / "factor_summary_stats.csv", float_format="%.3f")
    pd.DataFrame(grs_rows).set_index("model").to_csv(
        tables_dir / "grs_test.csv", float_format="%.4f")


def write_regression_table(
    res: RegressionResult, tables_dir: str | Path, periods_per_year: int = 12
) -> Path:
    """Per-model regression output: annualized alpha, loadings, t-stats, adj. R^2."""
    out = pd.DataFrame({
        "alpha_ann_pct": res.alpha * periods_per_year,
        "t_alpha": res.t_alpha,
        **{f"b_{c}": res.beta[c] for c in res.spec.factors},
        **{f"t_{c}": res.t_beta[c] for c in res.spec.factors},
        "adj_R2": res.r2adj,
    })
    path = Path(tables_dir) / f"regression_{res.spec.name.lower()}.csv"
    out.to_csv(path, float_format="%.3f")
    return path
