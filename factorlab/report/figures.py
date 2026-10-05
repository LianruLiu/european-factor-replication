"""Figure builders (PNG)."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from factorlab.tests.timeseries import RegressionResult


def make_figures(
    data: pd.DataFrame,
    factor_cols: list[str],
    excess_returns: pd.DataFrame,
    results: dict[str, RegressionResult],
    figs_dir: str | Path,
    hml_col: str = "HML",
    base_date_label: str = "",
    study_title: str = "",
    test_assets_label: str = "test-asset portfolios",
    region_label: str = "",
) -> None:
    """Reproduce the study's four standard figures."""
    figs_dir = Path(figs_dir)
    figs_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "figure.dpi": 150})
    pcols = list(excess_returns.columns)
    prefix = f"{study_title} " if study_title else ""

    # 1. cumulative factor returns
    fig, ax = plt.subplots(figsize=(9, 4.5))
    cum = (1 + data[factor_cols] / 100).cumprod()
    for c in factor_cols:
        ax.plot(cum.index, cum[c], label=c, lw=1.4)
    title = f"Cumulative returns of {prefix}Fama-French 5 factors"
    if base_date_label:
        title += f" ({base_date_label} = 1)"
    ax.set_title(title)
    ax.set_ylabel("Cumulative gross return")
    ax.legend(ncol=5, frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(figs_dir / "factor_cumulative.png"); plt.close(fig)

    # 2. alphas across models (annualized %)
    names = list(results)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    x = np.arange(len(pcols))
    w = 0.7 / max(len(names), 1)
    for i, name in enumerate(names):
        off = (i - (len(names) - 1) / 2) * w
        ax.bar(x + off, results[name].alpha * 12, w, label=f"{name} alpha")
    ax.set_xticks(x)
    ax.set_xticklabels([c.replace(" ", "\n") for c in pcols], fontsize=7)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Annualized alpha (%)")
    ax.set_title(f"Annualized alphas: {test_assets_label}")
    ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(figs_dir / "alphas_ff3_ff5.png"); plt.close(fig)

    # 3. HML 12-month rolling mean
    if hml_col in data.columns:
        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(data.index, data[hml_col].rolling(12).mean(),
                lw=1.4, color="darkred")
        ax.axhline(0, color="k", lw=0.8)
        region = f", {region_label}" if region_label else ""
        ax.set_title(f"{hml_col} (value premium), 12-month rolling mean{region}")
        ax.set_ylabel("Monthly %")
        ax.grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(figs_dir / "hml_rolling.png"); plt.close(fig)

    # 4. average annualized excess returns of test assets
    avg = excess_returns.mean() * 12
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(range(len(pcols)), avg.values, color="steelblue")
    ax.set_xticks(range(len(pcols)))
    ax.set_xticklabels([c.replace(" ", "\n") for c in pcols], fontsize=7)
    ax.set_ylabel("Annualized excess return (%)")
    ax.set_title(f"Average annualized excess returns: {test_assets_label}")
    fig.tight_layout(); fig.savefig(figs_dir / "avg_excess_returns.png"); plt.close(fig)
