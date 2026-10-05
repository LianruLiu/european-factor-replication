# Replicating the Fama-French Factor Models on European Equities (1990–2026)

**Author:** Lianru Liu · **Date:** October 2026 · **Status:** Independent replication

---

## Part I — The academic questions behind the design

Every empirical asset-pricing model is an answer to a prior puzzle. This section
organizes the questions that motivated the Fama-French factor design, and the
knowledge needed to understand the answers.

### Q1. Why do average returns differ across stocks?

The foundational question of asset pricing: in a market where investors are
risk-averse, expected returns should compensate for risk. The Capital Asset
Pricing Model (Sharpe, 1964; Lintner, 1965) gives the sharpest version of this
idea — a single number, the market beta, should explain all cross-sectional
differences in expected returns:

> E[Rᵢ] − Rf = βᵢ · (E[Rm] − Rf)

If the CAPM held exactly, sorting stocks by anything other than beta — size,
valuation ratios, past returns — would reveal no return differences. The entire
factor literature exists because it does not.

**Related knowledge:** *expected vs. realized returns* (we only ever observe
realized returns; a factor "premium" is the historical average of realized
returns, an estimate of the ex-ante risk premium, not a guarantee); the
*joint-hypothesis problem* (any test of market efficiency is simultaneously a
test of the asset-pricing model used — Fama, 1970).

### Q2. Is the CAPM enough? The size and value anomalies

Two empirical regularities broke the CAPM's monopoly:

- **Size (Banz, 1981):** small-capitalization stocks earned higher average
  returns than their market betas predicted.
- **Value (Fama & French, 1992):** stocks with high book-to-market ratios
  (value stocks) earned higher average returns than low book-to-market
  (growth) stocks, even after controlling for beta and size. In fact, once size
  and book-to-market were accounted for, market beta had almost no explanatory
  power left.

Fama and French (1993) turned these anomalies into *factors*: tradable
long–short portfolios — SMB (small minus big) and HML (high minus low
book-to-market) — and showed that a three-factor model absorbed most of the
CAPM's pricing errors.

**Related knowledge:** *anomaly* (a return pattern unexplained by the benchmark
model); *sorting* (forming portfolios by ranking stocks on a characteristic);
*long–short factor construction* (e.g., 2×3 independent sorts on size and
book-to-market).

### Q3. Risk or mispricing? Competing explanations of the premia

Why should value stocks earn more? Two rival stories:

- **Risk-based:** value firms tend to be distressed; their high returns
  compensate investors for bearing distress/bankruptcy risk that the market
  beta misses (Fama & French, 1996).
- **Behavioral:** investors over-extrapolate past growth, overpaying for
  glamour stocks and underpaying for value stocks; the premium is the slow
  correction of mispricing (Lakonishok, Shleifer & Vishny, 1994).

This debate is unresolved and mostly irrelevant to the replication itself — but
it is the reason the literature keeps score with *alphas*: any return the
factors cannot explain is either missing risk or mispricing, and the GRS test
(Part IV) is the formal scoreboard.

**Related knowledge:** *alpha* (abnormal return vs. the model); *limits of
arbitrage* (why mispricing can persist).

### Q4. Do U.S. results travel? Why Europe is the right out-of-sample test

A pattern found on U.S. data may be *data mining* — the accidental discovery
produced by searching many specifications on one dataset. The scientific
response is out-of-sample testing: the same sorts, the same regressions, on
data the original authors did not use to design the model. Europe is the
natural laboratory: deep, liquid markets, long histories, and economic
structures different enough from the U.S. that survival there is informative.
Fama and French (2012) themselves extended the tests internationally.

### Q5. From three factors to five: the valuation-equation logic

The five-factor model was not assembled by data mining. It follows from the
Miller–Modigliani dividend-discount identity: holding everything else fixed,
a stock's expected return is higher when its book-to-market ratio is higher,
expected profitability is higher, and expected investment is lower. Profitability
(Novy-Marx, 2013) and investment (Aharoni, Grundy & Zeng, 2013) patterns in
returns therefore *had* to be related to expected returns — the only question
was whether the market already priced them. Fama and French (2015) added RMW
(robust minus weak profitability) and CMA (conservative minus aggressive
investment) and showed the five-factor model absorbed the anomalies — notably
the low average returns of small, unprofitable, high-investment firms — that
embarrassed the three-factor model.

### Q6. The factor zoo: why replication discipline matters

Hundreds of "factors" have been proposed (Cochrane, 2011, calls it the
*factor zoo*). Most do not survive transaction costs, out-of-sample tests, or
multiple-testing corrections. This replication practices the discipline the
literature demands: pre-committed test assets (the 25 Size–B/M portfolios),
a fixed sample, and a formal joint test (GRS) rather than cherry-picked
t-statistics.

---

## Part II — Literature (concise tour)

| Study | Contribution |
|---|---|
| Sharpe (1964); Lintner (1965) | CAPM: market beta as the single priced risk |
| Banz (1981) | Size effect: small stocks earn more than beta predicts |
| Fama & French (1992) | Book-to-market and size drive the cross-section; beta fades |
| Fama & French (1993) | Three-factor model: Mkt-RF, SMB, HML |
| Lakonishok, Shleifer & Vishny (1994) | Behavioral account of the value premium |
| Fama & French (1996) | Risk-based multifactor explanation of anomalies |
| Carhart (1997) | Momentum (WML) as a fourth factor |
| Novy-Marx (2013) | Gross profitability premium → motivates RMW |
| Aharoni, Grundy & Zeng (2013) | Investment effect → motivates CMA |
| Fama & French (2012) | Size, value, momentum in international (incl. European) returns |
| Fama & French (2015) | Five-factor model adds RMW and CMA |
| Gibbons, Ross & Shanken (1989) | GRS F-test of joint alpha = 0 |
| Cochrane (2011) | "Factor zoo" critique; discount-rate view |

Full citations: [REFERENCES.md](../REFERENCES.md).

---

## Part III — Data

- **Source.** Kenneth R. French Data Library, files constructed from the
  August 2026 Bloomberg database (free for research use; vendored in
  `data/raw/`).
- **Region.** Europe (16 developed markets incl. the UK, Germany, France,
  Switzerland).
- **Factors (monthly).** Mkt-RF (market excess return), SMB (size), HML
  (value), RMW (profitability), CMA (investment), RF (one-month T-bill).
  Factors are returns on diversified long–short portfolios from 2×3 sorts.
- **Test assets (monthly).** 25 value-weighted portfolios from independent 5×5
  sorts on market capitalization (Size) and book-to-market — the classic
  Fama-French (1993) test assets. Portfolios are reformed each June.
- **Sample.** July 1990 – August 2026, T = 434 months. Missing values (−99.99)
  treated as NaN; the common sample is used throughout.

---

## Part IV — Methodology

For each test portfolio *i*, estimate by OLS:

> Rᵢ,ₜ − Rfₜ = αᵢ + bᵢ·MKTₜ + sᵢ·SMBₜ + hᵢ·HMLₜ (+ rᵢ·RMWₜ + cᵢ·CMAₜ) + εᵢ,ₜ

Reported per portfolio: annualized alpha, t(alpha), factor loadings with
t-statistics, adjusted R². Model comparison uses:

1. the **count of significant alphas** (|t| > 2) out of 25;
2. mean adjusted R²;
3. the **Gibbons–Ross–Shanken F-test** of H₀: α₁ = … = α₂₅ = 0,

> F = (T/N)·[(T−N−K)/(T−K−1)] · (α̂′Σ̂⁻¹α̂) / (1 + μ̂f′Ω̂⁻¹μ̂f) ∼ F(N, T−N−K),

where N = 25 test assets, K factors, Σ̂ the residual covariance matrix, and
μ̂f, Ω̂ the factor mean vector and covariance matrix. Rejection means the
model's factors cannot jointly price the test assets.

*Note on standard errors:* t-statistics use OLS standard errors. Returns show
mild autocorrelation/heteroskedasticity; Newey–West corrections would be a
natural robustness extension (see §VI).

---

## Part V — Results

### 5.1 Factor premia in Europe, 1990–2026

| Factor | Ann. mean | Ann. vol | t(mean) | Sharpe |
|--------|-----------|----------|---------|--------|
| Mkt-RF | 6.36% | 17.01% | 2.25 | 0.37 |
| SMB    | 0.15% | 7.23%  | 0.12 | 0.02 |
| HML    | 4.24% | 9.01%  | 2.83 | 0.47 |
| RMW    | 3.60% | 5.56%  | 3.89 | 0.65 |
| CMA    | 1.71% | 6.21%  | 1.66 | 0.28 |

Three facts stand out. First, **the size premium is economically and
statistically zero in Europe** (0.15%/yr, t = 0.12) — consistent with the
documented post-publication decay of the size effect. Second, **value and
profitability premia are alive**: HML earns 4.24%/yr (t = 2.83) and RMW
3.60%/yr (t = 3.89, Sharpe 0.65, the strongest risk-adjusted premium). Third,
the investment premium is positive but marginal (t = 1.66).

### 5.2 Do the models price the 25 Size–B/M portfolios?

- **Factor loadings behave as theory predicts.** Within every size quintile,
  HML loadings rise monotonically with book-to-market (e.g., smallest quintile:
  −0.43, −0.24, −0.10, 0.09, 0.35). Value-weighted portfolios are well
  described: mean adjusted R² is 0.942 (FF3) and 0.946 (FF5).
- **The small-growth problem replicates — and the five-factor model halves
  it.** The small-growth portfolio (small size, low B/M) earns an FF3 alpha of
  **−5.16%/yr (t = −4.94)**, the largest pricing error in the cross-section.
  Under FF5 it shrinks to −2.43%/yr (t = −2.38): negative RMW (−0.48) and CMA
  (−0.26) loadings show these firms are unprofitable high-investors — exactly
  the anomaly the two added factors were designed to absorb. Big-value's FF3
  alpha (−2.34%/yr, t = −2.44) likewise vanishes under FF5 (+0.06%/yr).
- **Scoreboard:** significant alphas (|t| > 2) fall from **8 of 25 (FF3) to
  6 of 25 (FF5)**. The GRS test **rejects** joint α = 0 for both models —
  FF3: F = 3.05 (p < 0.001); FF5: F = 2.71 (p < 0.001) — so neither model fully
  prices European equities, but the five-factor model prices them *better*,
  mirroring the U.S. verdict of Fama and French (2015).

### 5.3 Dynamics

HML's 12-month rolling mean (see `results/figures/hml_rolling.png`) shows the
value premium is highly time-varying: deeply negative during the late-1990s
tech boom and 2020 growth rally (HML lost −30.1% in 2020 alone), violently
positive in recoveries (+29.6% in 2025). The premium is compensation for
*enduring* bad times, not a free lunch — the core intuition of the risk-based
story in §I-Q3.

---

## Part VI — Conclusion and limitations

**What we learn.** (1) The value and profitability premia survive
out-of-sample in Europe; the size premium does not. (2) The five-factor
model's added factors earn their keep precisely where theory said they would —
small, unprofitable, high-investment firms. (3) Formally, both models are
rejected: factor models are useful approximations, not literal truth.

**Limitations.**
1. *Test assets are value-weighted portfolios*, tradable only approximately;
   no transaction costs are modeled.
2. *OLS standard errors* — Newey–West (1987) corrections are a standard
   robustness check, omitted here for clarity.
3. *One region, one sort.* Results are conditional on the 25 Size–B/M design;
   other test assets (e.g., Size–Profitability sorts) could tell a different
   story — the classic joint-hypothesis caveat.
4. *No investment implication.* Historical premia do not predict future
   returns; see the disclaimer in the README.

---

## References

See [REFERENCES.md](../REFERENCES.md) for full citations.

## Glossary

See [GLOSSARY.md](../GLOSSARY.md) for terminology (English + 中文).
