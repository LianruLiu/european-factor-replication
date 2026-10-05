# Example: European Fama-French 3- and 5-factor replication

The flagship study built with **factorlab**. It replicates the Fama-French
three-factor (1993) and five-factor (2015) models on European equities,
July 1990 – August 2026 (T = 434 months), using the Kenneth R. French Data
Library.

## Run it

From the repo root:

```bash
pip install -r requirements.txt
python -m factorlab run examples/europe_ff3_ff5/config.yaml
```

This regenerates everything under `results/`:

- `results/tables/` — factor summary stats, per-model regressions, GRS tests
- `results/figures/` — cumulative factors, alphas, HML dynamics, excess returns
- `results/tearsheet.md` — auto-generated headline summary

## Make it yours

Copy this folder, point `data.factors` / `data.portfolios` at your own files,
edit `models:` — e.g. add a momentum factor or a custom model — and run.
See the [main README](../../README.md) for the config reference.
