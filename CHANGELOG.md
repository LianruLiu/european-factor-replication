# Changelog

## 0.1.0 — 2026-10-05

- Initial `factorlab` release: YAML-configured factor research framework.
- Modules: `data` (French-library + CSV loaders, downloader), `factors`
  (premia statistics), `models` (FF3/FF5/Carhart4/CAPM/custom specs),
  `tests` (time-series OLS with optional Newey-West, GRS joint-alpha test),
  `report` (CSV tables, PNG figures, auto-generated tearsheet).
- One-command studies: `python -m factorlab run <config.yaml>`
  (`--outdir` override, `--quiet` flag); `python -m factorlab download`.
- Flagship example: European Fama–French 3- and 5-factor replication
  (1990-07 – 2026-08, T = 434).
- 17-test pytest suite (unit + integration, incl. regression tests against
  committed reference outputs) and GitHub Actions CI (Python 3.10–3.12).
- Installable package (`pip install .`, `factorlab` console script).
