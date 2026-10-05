# factorlab — a YAML-configured factor research framework

**Plug in your data. Pick your models. Get a full asset-pricing study.**

`factorlab` turns a factor-research idea into a reproducible study — data
loading, factor premia statistics, time-series regressions, Gibbons-Ross-Shanken
(1989) joint-alpha tests, tables, figures, and an auto-generated tearsheet —
from a single YAML config file.

Its flagship example replicates the Fama-French 3-factor (1993) and 5-factor
(2015) models on European equities, July 1990 – August 2026.

## Installation

```bash
pip install -r requirements.txt        # runtime deps
# or install as a package (gives you the `factorlab` command):
pip install .
pip install -r requirements-dev.txt   # pytest, for development
```

## Quickstart

```bash
python -m factorlab run examples/europe_ff3_ff5/config.yaml
# or, after pip install .:  factorlab run examples/europe_ff3_ff5/config.yaml
```

That's it. Everything below is regenerated under `results/`:

- `results/tables/` — factor summary stats, per-model regressions, GRS tests (CSV)
- `results/figures/` — cumulative factors, alphas, HML dynamics, excess returns (PNG)
- `results/tearsheet.md` — auto-generated headline summary

## Your own study in 5 minutes

1. Copy `examples/europe_ff3_ff5/` to `examples/my_study/`.
2. Point `data.factors` / `data.portfolios` at your files
   (French-library format, or any CSV with a date column — set
   `data.format: csv`).
3. Edit `models:` — use a preset or define your own:
   ```yaml
   models:
     FF5: ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
     FF5+MOM: ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "MOM"]
   ```
4. Run: `python -m factorlab run examples/my_study/config.yaml`

Python API works too:

```python
from factorlab.pipeline import run
run("examples/europe_ff3_ff5/config.yaml")

from factorlab.models.specs import custom_model
from factorlab.tests import run_regressions, grs_test
```

### Config reference

| Section | Key | Meaning |
|---|---|---|
| `data` | `format` | `french_library` or `csv` |
| `data` | `factors` / `portfolios` | input files (relative to the config) |
| `data` | `start` / `end` | sample window, e.g. `1990-07` |
| `universe` | `factors` | all factor columns (incl. risk-free) |
| `universe` | `risk_free` | risk-free column for excess returns |
| `universe` | `test_assets` | `all` or a list of portfolio columns |
| `models` | `<name>: [...]` | model name → factor columns |
| `tests` | `grs` | run the GRS joint-alpha test (default true) |
| `tests` | `cov_type` | `nonrobust` (default) or `HAC` for Newey-West |
| `output` | `dir` / `tearsheet` | where results go |

## Framework layout

```
factorlab/
├── data/        # loaders: French Data Library, generic CSVs, downloader
├── factors/     # premia stats (ann. mean/vol/t-stat/Sharpe), rolling stats
├── models/      # ModelSpec + presets (FF3, FF5, Carhart4, CAPM, custom)
├── tests/       # time-series OLS (+ optional Newey-West), GRS F-test
├── report/      # CSV tables, PNG figures, auto tearsheet
├── config.py    # YAML loading / validation
├── pipeline.py  # run(config) — the whole study end to end
└── cli.py       # python -m factorlab run|download
examples/
└── europe_ff3_ff5/   # flagship study: config + notes
tests/                # pytest suite (17 tests: unit + integration)
```

## Testing

```bash
pytest -q
```

The suite includes regression tests pinned to the flagship study's committed
outputs (factor premia, alphas, GRS statistics), so any change that alters
published numbers fails loudly. CI runs on Python 3.10–3.12
(`.github/workflows/ci.yml`).

---

## Flagship example: Fama-French on European equities

**Research question.** Do the size, value, profitability, and investment premia
documented on U.S. data also price the cross-section of European equity returns —
and does the five-factor model explain the test assets its predecessor could not?

**Data.** Kenneth R. French Data Library (August 2026 Bloomberg vintage):
monthly European factors `Mkt-RF, SMB, HML, RMW, CMA, RF` and 25 value-weighted
Size–B/M portfolios, July 1990 – August 2026 (**T = 434**). Raw files vendored
under `data/raw/`; see `data/README.md`.

**Method.** For each test asset, time-series OLS of excess returns on the
factors; models compared via adjusted R², count of significant alphas, and the
GRS F-test of joint α = 0.

### Key findings

| Factor | Ann. mean | Ann. vol | t(mean) | Sharpe |
|--------|-----------|----------|---------|--------|
| Mkt-RF | 6.36% | 17.01% | 2.25 | 0.37 |
| SMB    | 0.15% | 7.23%  | 0.12 | 0.02 |
| HML    | 4.24% | 9.01%  | 2.83 | 0.47 |
| RMW    | 3.60% | 5.56%  | 3.89 | 0.65 |
| CMA    | 1.71% | 6.21%  | 1.66 | 0.28 |

- **The size premium is essentially zero in Europe** (0.15%/yr, t = 0.12).
- **Value (HML) and profitability (RMW) premia are significant**; RMW has the
  highest Sharpe (0.65).
- **The small-growth problem replicates:** FF3 alpha of **−5.17%/yr
  (t = −4.94)** shrinks to −2.43%/yr (t = −2.39) under FF5 — the textbook
  motivation for the five-factor model.
- **Neither model fully passes:** GRS rejects joint α = 0 for both
  (FF3: F = 3.05, p < 0.001; FF5: F = 2.71, p < 0.001), but FF5 cuts significant
  alphas from 8 to 6 of 25 and lifts mean adjusted R² from 0.942 to 0.946.

Full tables: [`results/tables/`](results/tables/) · Figures:
[`results/figures/`](results/figures/) · Tearsheet:
[`results/tearsheet.md`](results/tearsheet.md)

---

## Commercial use & data licensing

`factorlab` itself is MIT-licensed — use it commercially freely. Note the
**data** is a separate matter: the Kenneth R. French Data Library is free for
research use; if you deploy factorlab commercially, check the library's terms
and consider computing factors from licensed price data instead. The example
CSVs under `data/raw/` are vendored for reproducibility of the flagship study.

## Disclaimer

Research framework. Nothing here is investment advice. Factor premia are
historical averages; they do not predict future returns.
