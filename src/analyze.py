#!/usr/bin/env python3
"""
Fama-French factor replication on European equities.

Data: Kenneth R. French Data Library (created with the 202608 Bloomberg database)
  - Europe 5 Factors (monthly): Mkt-RF, SMB, HML, RMW, CMA, RF
  - Europe 25 Portfolios formed on Size and Book-to-Market (monthly, value-weighted)

Steps:
  1. Parse the fixed-format CSV files (monthly blocks only).
  2. Summary statistics for the five factors (annualized).
  3. Time-series OLS regressions of 25 Size-B/M portfolio excess returns on
     the 3-factor and 5-factor models: alpha, loadings, t-stats, adj. R^2.
  4. Gibbons-Ross-Shanken (1989) F-test of joint alpha = 0 for each model.
  5. Save tables (results/tables) and figures (results/figures).
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
TABLES = Path(__file__).resolve().parent.parent / "results" / "tables"
FIGURES = Path(__file__).resolve().parent.parent / "results" / "figures"
TABLES.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)

MISSING = -99.99


def parse_factors(path):
    """Parse the monthly block of a French-library factor file."""
    lines = Path(path).read_text().splitlines()
    # find header row like ",Mkt-RF,SMB,HML,RMW,CMA,RF"
    start = next(i for i, l in enumerate(lines) if l.startswith(",Mkt-RF"))
    cols = [c.strip() for c in lines[start].split(",")[1:]]
    rows = []
    for l in lines[start + 1:]:
        if not l.strip():
            break
        parts = l.split(",")
        date = parts[0].strip()
        if not re.fullmatch(r"\d{6}", date):
            break
        vals = [float(p) for p in parts[1:1 + len(cols)]]
        rows.append([date] + vals)
    df = pd.DataFrame(rows, columns=["date"] + cols)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m")
    df = df.set_index("date").replace(MISSING, np.nan)
    return df


def parse_portfolios_vw_monthly(path):
    """Parse the value-weighted monthly block of the 25 Size-B/M portfolio file."""
    lines = Path(path).read_text().splitlines()
    start = next(i for i, l in enumerate(lines)
                 if l.strip() == "Average Value Weighted Returns -- Monthly")
    cols = [c.strip() for c in lines[start + 1].split(",")[1:]]
    rows = []
    for l in lines[start + 2:]:
        if not l.strip():
            break
        parts = l.split(",")
        date = parts[0].strip()
        if not re.fullmatch(r"\d{6}", date):
            break
        vals = [float(p) for p in parts[1:1 + len(cols)]]
        rows.append([date] + vals)
    df = pd.DataFrame(rows, columns=["date"] + cols)
    df["date"] = pd.to_datetime(df["date"], format="%Y%m")
    df = df.set_index("date").replace(MISSING, np.nan)
    return df


def summary_stats(factors):
    """Annualized mean, volatility, t-stat of mean, Sharpe ratio."""
    out = []
    for c in factors.columns:
        x = factors[c].dropna()
        mu_m, sd_m = x.mean(), x.std()
        n = len(x)
        out.append({
            "factor": c,
            "ann_mean_pct": mu_m * 12,
            "ann_vol_pct": sd_m * np.sqrt(12),
            "t_mean": mu_m / (sd_m / np.sqrt(n)),
            "sharpe": (mu_m / sd_m) * np.sqrt(12),
            "n_obs": n,
        })
    return pd.DataFrame(out).set_index("factor")


def grs_test(alphas, resid_cov, factor_means, factor_cov, T):
    """Gibbons-Ross-Shanken (1989) F-test of H0: all alphas = 0.

    alphas      : (N,)   intercepts from time-series regressions
    resid_cov   : (N,N)  residual covariance matrix
    factor_means: (K,)   sample means of factors
    factor_cov  : (K,K)  sample covariance of factors
    T           : int    number of time-series observations
    Returns (F-stat, p-value).
    """
    N, K = len(alphas), len(factor_means)
    a = np.asarray(alphas)
    S = np.asarray(resid_cov)
    mu = np.asarray(factor_means)
    Om = np.asarray(factor_cov)
    theta2 = float(a @ np.linalg.inv(S) @ a)
    sharpe2_f = float(mu @ np.linalg.inv(Om) @ mu)
    F = (T / N) * ((T - N - K) / (T - K - 1)) * theta2 / (1 + sharpe2_f)
    p = 1 - stats.f.cdf(F, N, T - N - K)
    return F, p


def run_regressions(Y, X, labels):
    """OLS of each column of Y on X (with intercept). Returns dict of result frames."""
    Xc = sm.add_constant(X)
    alphas, t_alphas, betas, t_betas, r2adj, resid = [], [], [], [], [], []
    for col in Y.columns:
        y = Y[col]
        fit = sm.OLS(y, Xc, missing="drop").fit()
        p = fit.params
        t = fit.tvalues
        alphas.append(p["const"]); t_alphas.append(t["const"])
        betas.append([p[c] for c in labels]); t_betas.append([t[c] for c in labels])
        r2adj.append(fit.rsquared_adj)
        resid.append(fit.resid)
    resid = pd.DataFrame(resid, index=Y.columns).T
    return {
        "alpha": pd.Series(alphas, index=Y.columns),
        "t_alpha": pd.Series(t_alphas, index=Y.columns),
        "beta": pd.DataFrame(betas, index=Y.columns, columns=labels),
        "t_beta": pd.DataFrame(t_betas, index=Y.columns, columns=labels),
        "r2adj": pd.Series(r2adj, index=Y.columns),
        "resid": resid,
    }


def main():
    factors = parse_factors(RAW / "Europe_5_Factors.csv")
    ports = parse_portfolios_vw_monthly(RAW / "Europe_25_Portfolios_ME_BE-ME.csv")

    # align on common monthly index, drop any missing rows
    data = factors.join(ports, how="inner").dropna()
    print(f"Sample: {data.index.min().date()} to {data.index.max().date()}  (T={len(data)})")

    fcols5 = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
    fcols3 = ["Mkt-RF", "SMB", "HML"]
    pcols = list(ports.columns)

    # ---- 1. factor summary stats ----
    summ = summary_stats(data[fcols5 + ["RF"]])
    summ.to_csv(TABLES / "factor_summary_stats.csv", float_format="%.3f")
    print(summ.round(2).to_string())

    # ---- 2. excess returns of test assets ----
    Y = data[pcols].sub(data["RF"], axis=0)
    Y.to_csv(TABLES.parent / "processed" / "excess_returns.csv") if False else None

    # ---- 3. regressions ----
    results = {}
    for name, fcols in [("ff3", fcols3), ("ff5", fcols5)]:
        res = run_regressions(Y, data[fcols], fcols)
        results[name] = res
        out = pd.DataFrame({
            "alpha_ann_pct": res["alpha"] * 12,
            "t_alpha": res["t_alpha"],
            **{f"b_{c}": res["beta"][c] for c in fcols},
            **{f"t_{c}": res["t_beta"][c] for c in fcols},
            "adj_R2": res["r2adj"],
        })
        out.to_csv(TABLES / f"regression_{name}.csv", float_format="%.3f")

    # ---- 4. GRS tests ----
    T = len(data)
    grs_rows = []
    for name, fcols in [("FF3", fcols3), ("FF5", fcols5)]:
        res = results[name.lower()]
        F, p = grs_test(res["alpha"], res["resid"].cov(),
                        data[fcols].mean(), data[fcols].cov(), T)
        grs_rows.append({"model": name, "N": len(pcols), "K": len(fcols), "T": T,
                         "GRS_F": F, "p_value": p})
    grs = pd.DataFrame(grs_rows).set_index("model")
    grs.to_csv(TABLES / "grs_test.csv", float_format="%.4f")
    print(grs.to_string())

    # ---- 5. figures ----
    plt.rcParams.update({"font.size": 10, "figure.dpi": 150})

    # 5a. cumulative factor returns
    fig, ax = plt.subplots(figsize=(9, 4.5))
    cum = (1 + data[fcols5] / 100).cumprod()
    for c in fcols5:
        ax.plot(cum.index, cum[c], label=c, lw=1.4)
    ax.set_title("Cumulative returns of European Fama-French 5 factors (Jul 1990 = 1)")
    ax.set_ylabel("Cumulative gross return")
    ax.legend(ncol=5, frameon=False)
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIGURES / "factor_cumulative.png"); plt.close(fig)

    # 5b. alphas: FF3 vs FF5 (annualized %)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    x = np.arange(len(pcols))
    w = 0.35
    ax.bar(x - w/2, results["ff3"]["alpha"] * 12, w, label="FF3 alpha")
    ax.bar(x + w/2, results["ff5"]["alpha"] * 12, w, label="FF5 alpha")
    ax.set_xticks(x); ax.set_xticklabels([c.replace(" ", "\n") for c in pcols], fontsize=7)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Annualized alpha (%)")
    ax.set_title("Annualized alphas: 25 European Size-B/M portfolios")
    ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(FIGURES / "alphas_ff3_ff5.png"); plt.close(fig)

    # 5c. HML time series (12m rolling mean) with zero line
    fig, ax = plt.subplots(figsize=(9, 4))
    hml_roll = data["HML"].rolling(12).mean()
    ax.plot(data.index, hml_roll, lw=1.4, color="darkred")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_title("HML (value premium), 12-month rolling mean, Europe")
    ax.set_ylabel("Monthly %")
    ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(FIGURES / "hml_rolling.png"); plt.close(fig)

    # 5d. average excess return vs size/value rank (heatmap-style bar)
    avg = Y.mean() * 12
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.bar(range(len(pcols)), avg.values, color="steelblue")
    ax.set_xticks(range(len(pcols)))
    ax.set_xticklabels([c.replace(" ", "\n") for c in pcols], fontsize=7)
    ax.set_ylabel("Annualized excess return (%)")
    ax.set_title("Average annualized excess returns: 25 European Size-B/M portfolios")
    fig.tight_layout(); fig.savefig(FIGURES / "avg_excess_returns.png"); plt.close(fig)

    print("tables ->", TABLES)
    print("figures ->", FIGURES)


if __name__ == "__main__":
    main()
