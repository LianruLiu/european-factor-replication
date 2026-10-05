"""Study pipeline: config in, tables + figures + tearsheet out."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

from factorlab.config import load_config, resolve
from factorlab.data.loaders import load_french_factors, load_french_portfolios, load_csv
from factorlab.factors.stats import premia_stats
from factorlab.models.specs import from_config
from factorlab.report.figures import make_figures
from factorlab.report.tables import write_regression_table, write_summary_tables
from factorlab.report.tearsheet import write_tearsheet
from factorlab.tests.grs import grs_test
from factorlab.tests.timeseries import run_regressions

log = logging.getLogger("factorlab")


def run(config_path: str | Path, output_dir: str | Path | None = None) -> dict[str, Any]:
    """Run a full factor study from a YAML config file.

    Parameters
    ----------
    config_path : path to the study's ``config.yaml``.
    output_dir  : optional override for ``output.dir`` (useful in tests).

    Returns a dict with the computed tables (handy in notebooks).
    Raises ValueError with a clear message on bad configs or missing data.
    """
    cfg = load_config(config_path)
    root: Path = cfg["_root"]
    data_cfg, uni = cfg["data"], cfg["universe"]
    out_cfg = cfg.get("output", {})

    out_dir = Path(output_dir) if output_dir else resolve(out_cfg.get("dir", "results"), root)
    tables_dir = out_dir / "tables"
    figs_dir = out_dir / "figures"

    models = from_config(cfg["models"])

    # ---- 1. load data ----
    fmt = data_cfg.get("format", "french_library")
    fpath = resolve(data_cfg["factors"], root)
    ppath = resolve(data_cfg["portfolios"], root)
    for label, p in (("data.factors", fpath), ("data.portfolios", ppath)):
        if not p.exists():
            raise ValueError(f"{label}: file not found: {p}")
    if fmt == "french_library":
        factors = load_french_factors(fpath)
        ports = load_french_portfolios(ppath)
    elif fmt == "csv":
        factors = load_csv(fpath)
        ports = load_csv(ppath)
    else:
        raise ValueError(f"data.format must be 'french_library' or 'csv', got {fmt!r}")

    # ---- 2. sample window ----
    if data_cfg.get("start"):
        factors = factors.loc[data_cfg["start"]:]
        ports = ports.loc[data_cfg["start"]:]
    if data_cfg.get("end"):
        factors = factors.loc[:data_cfg["end"]]
        ports = ports.loc[:data_cfg["end"]]
    data = factors.join(ports, how="inner").dropna()
    if data.empty:
        raise ValueError("sample is empty after aligning factors and portfolios "
                         "(check data.start/data.end and file contents)")
    T = len(data)
    sample_label = (f"{data.index.min().date()} to {data.index.max().date()} "
                    f"(T={T})")
    log.info("Sample: %s", sample_label)

    fcols_all = uni["factors"]
    rf = uni["risk_free"]
    ta = uni.get("test_assets")
    pcols = (list(ports.columns) if (not ta or ta == "all")
             else [c for c in ports.columns if c in ta])
    if not pcols:
        raise ValueError("universe.test_assets selected no portfolios")

    # ---- 3. validate every column we are about to use ----
    needed = set(fcols_all) | {rf} | {f for spec in models for f in spec.factors}
    missing = sorted(c for c in needed if c not in data.columns)
    if missing:
        raise ValueError(
            "columns missing from data: " + ", ".join(missing) +
            ". Check universe.factors and models: against your files.")

    # ---- 3. factor summary stats ----
    stats = premia_stats(data[fcols_all])
    log.info("\n%s", stats.round(2).to_string())

    # ---- 4. test-asset excess returns ----
    Y = data[pcols].sub(data[rf], axis=0)

    # ---- 5. regressions per model ----
    tests_cfg = cfg.get("tests", {})
    cov_type = tests_cfg.get("cov_type", "nonrobust")
    cov_kwds = tests_cfg.get("cov_kwds")
    results, reg_tables = {}, {}
    for spec in models:
        if T <= len(pcols) + spec.k:
            raise ValueError(
                f"{spec.name}: not enough observations (T={T}) for "
                f"N={len(pcols)} assets and K={spec.k} factors")
        res = run_regressions(Y, data[spec.factors], spec,
                              cov_type=cov_type, cov_kwds=cov_kwds)
        results[spec.name] = res
        reg_tables[spec.name] = _regression_frame(res)
        write_regression_table(res, tables_dir)
        sig = int((res.t_alpha.abs() > 2).sum())
        log.info("%s: %d/%d significant alphas, mean adj. R^2 = %.3f",
                 spec.name, sig, len(pcols), res.r2adj.mean())

    # ---- 6. GRS tests ----
    grs_rows = []
    if tests_cfg.get("grs", True):
        for spec in models:
            res = results[spec.name]
            F, p = grs_test(res.alpha, res.resid, data[spec.factors])
            grs_rows.append({"model": spec.name, "N": len(pcols),
                             "K": spec.k, "T": T, "GRS_F": F, "p_value": p})
    grs = pd.DataFrame(grs_rows)
    write_summary_tables(stats, grs_rows, tables_dir)
    if not grs.empty:
        log.info("\n%s", grs.set_index("model").to_string())

    # ---- 7. figures ----
    figs_wanted = out_cfg.get("figures", ["all"])
    if figs_wanted:
        rep = cfg.get("report", {})
        make_figures(
            data, [c for c in fcols_all if c != rf], Y, results, figs_dir,
            hml_col=rep.get("hml_col", "HML"),
            base_date_label=rep.get("base_date_label", ""),
            study_title=rep.get("study_title", ""),
            test_assets_label=rep.get("test_assets_label",
                                      "test-asset portfolios"),
            region_label=rep.get("region_label", ""),
        )

    # ---- 8. tearsheet ----
    if out_cfg.get("tearsheet", True) and not grs.empty:
        ts_name = out_cfg.get("tearsheet_name", "tearsheet.md")
        write_tearsheet(cfg.get("study", "Factor study"), sample_label,
                        stats, grs.set_index("model"), reg_tables,
                        out_dir / ts_name,
                        notes=cfg.get("report", {}).get("notes", ""))

    log.info("tables -> %s", tables_dir)
    log.info("figures -> %s", figs_dir)
    return {"config": cfg, "factor_stats": stats, "grs": grs,
            "reg_tables": reg_tables, "results": results}


def _regression_frame(res) -> pd.DataFrame:
    return pd.DataFrame({
        "alpha_ann_pct": res.alpha * 12,
        "t_alpha": res.t_alpha,
        **{f"b_{c}": res.beta[c] for c in res.spec.factors},
        **{f"t_{c}": res.t_beta[c] for c in res.spec.factors},
        "adj_R2": res.r2adj,
    })
