# Replicating the Fama-French Factor Models on European Equities

An independent, fully reproducible replication of the Fama-French 3-factor (1993)
and 5-factor (2015) asset-pricing models on European stock market data,
using the Kenneth R. French Data Library.

**Research question.** Do the size, value, profitability, and investment premia
documented on U.S. data also price the cross-section of European equity returns —
and does the five-factor model explain the test assets its predecessor could not?

## Data

- **Source:** Kenneth R. French Data Library (constructed from the August 2026
  Bloomberg database; free for research use).
- **Factors (monthly):** `Mkt-RF`, `SMB`, `HML`, `RMW`, `CMA`, `RF` — Europe region.
- **Test assets (monthly):** 25 value-weighted portfolios formed on Size and
  Book-to-Market — the classic Fama-French (1993) test assets.
- **Sample:** July 1990 – August 2026, **T = 434 months**.
- Raw files are vendored under `data/raw/`; see `data/README.md` for the source
  and refresh instructions.

## Method

For each of the 25 Size–B/M portfolios, time-series OLS regressions of excess
returns on the factor returns:

- **FF3:** R − Rf = α + b·(Mkt−Rf) + s·SMB + h·HML + ε
- **FF5:** R − Rf = α + b·(Mkt−Rf) + s·SMB + h·HML + r·RMW + c·CMA + ε

Model fit is compared via adjusted R², the count of significant alphas, and the
Gibbons–Ross–Shanken (1989) F-test of the joint hypothesis α₁ = … = α₂₅ = 0.

## Key findings

| Factor | Ann. mean | Ann. vol | t(mean) | Sharpe |
|--------|-----------|----------|---------|--------|
| Mkt-RF | 6.36% | 17.01% | 2.25 | 0.37 |
| SMB    | 0.15% | 7.23%  | 0.12 | 0.02 |
| HML    | 4.24% | 9.01%  | 2.83 | 0.47 |
| RMW    | 3.60% | 5.56%  | 3.89 | 0.65 |
| CMA    | 1.71% | 6.21%  | 1.66 | 0.28 |

- **The size premium is essentially zero in Europe** (0.15%/yr, t = 0.12) —
  consistent with the post-publication decay of the size effect.
- **Value (HML) and profitability (RMW) premia are statistically significant**,
  with RMW the strongest (Sharpe 0.65).
- **The textbook "small-growth problem" replicates:** the small-growth portfolio
  earns an FF3 alpha of **−5.16%/yr (t = −4.94)**; adding RMW and CMA shrinks it
  to −2.43%/yr (t = −2.38) — the exact motivation for the five-factor model.
- **HML loadings rise monotonically with book-to-market** within every size
  quintile, as theory predicts.
- **Neither model fully passes:** the GRS test rejects joint α = 0 for both
  (FF3: F = 3.05, p < 0.001; FF5: F = 2.71, p < 0.001), but FF5 cuts significant
  alphas from 8 to 6 of 25 and raises mean adjusted R² from 0.942 to 0.946.

Full tables: [`results/tables/`](results/tables/) · Figures: [`results/figures/`](results/figures/)

## Repository structure

```
├── README.md                 # this file
├── requirements.txt
├── data/
│   ├── README.md             # data source, license, refresh instructions
│   └── raw/                  # French-library CSVs (vendored for reproducibility)
├── src/
│   ├── download.py           # re-download raw data from the French library
│   └── analyze.py            # parse → summary stats → regressions → GRS → figures
├── results/
│   ├── tables/               # factor stats, regression output, GRS test (CSV)
│   └── figures/              # cumulative factors, alphas, HML dynamics (PNG)
├── report/
│   ├── REPORT.md             # full academic report (questions, literature, method, results)
│   └── REPORT.pdf            # PDF version
├── GLOSSARY.md               # bilingual glossary of asset-pricing terminology
└── REFERENCES.md             # academic references
```

## Reproduce

```bash
pip install -r requirements.txt
python src/download.py      # fetch raw data (or use data/raw as-is)
python src/analyze.py       # regenerates results/tables and results/figures
```

## Docs

- **[Full academic report](report/REPORT.md)** — the academic questions behind the
  factor design, literature, data, methodology, results, and limitations.
- **[Glossary](GLOSSARY.md)** — asset-pricing terminology (English + 中文).
- **[References](REFERENCES.md)** — cited literature.

## Disclaimer

Educational replication project. Nothing here is investment advice. Factor premia
are historical averages; they do not predict future returns.
