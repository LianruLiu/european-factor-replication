# Glossary of Asset-Pricing Terminology · 资产定语术语表

Each entry: **English term** — English definition — 中文解释.

---

**Alpha (α)** — The intercept of a factor regression; the average return left
unexplained by the model's factors ("abnormal return"). A significant alpha is
a pricing error. —— 因子回归的截距；模型解释不了的那部分平均收益（"超额收益"/定价误差）。显著的 alpha 说明模型漏掉了东西。

**Beta / factor loading (β)** — The slope on a factor; measures an asset's
exposure to that factor's risk. —— 因子上的斜率；衡量资产对该因子风险的暴露程度。

**Mkt-RF** — Market excess return: the value-weighted market return minus the
risk-free rate. The "market factor" of the CAPM. —— 市场超额收益：市值加权市场收益减无风险利率，CAPM 的市场因子。

**SMB (Small Minus Big)** — Return of small-cap minus large-cap stocks; the
*size factor*. —— 小市值减大市值股票收益；规模因子。

**HML (High Minus Low)** — Return of high book-to-market (value) minus low
book-to-market (growth) stocks; the *value factor*. —— 高账面市值比减低账面市值比；价值因子。

**RMW (Robust Minus Weak)** — Return of highly profitable minus weakly
profitable firms; the *profitability factor* (Fama-French 2015). —— 高盈利减低盈利；盈利因子。

**CMA (Conservative Minus Aggressive)** — Return of low-investment
(conservative) minus high-investment (aggressive) firms; the *investment
factor*. —— 低投资减高投资；投资因子。

**Risk-free rate (Rf)** — Return on a (nearly) default-free short-term asset,
here the one-month U.S. Treasury bill rate. —— 无风险利率；这里用的是一个月美国国债利率。

**Excess return** — Asset return minus the risk-free rate (R − Rf). The object
factor models try to explain. —— 超额收益；因子模型要解释的对象。

**Book-to-market (B/M)** — Book equity divided by market equity. High B/M =
"value" stock. —— 账面市值比；高 = 价值股。

**Market capitalization (Size)** — Price × shares outstanding. —— 市值；规模因子的排序依据。

**Value-weighted portfolio** — Portfolio weighting each stock by market cap
(mimics the actual market). —— 市值加权组合，模拟真实市场结构。

**Sorting / double sort** — Ranking stocks by one (or two) characteristics and
grouping them into portfolios, e.g. 5×5 Size–B/M sorts. —— 按特征排序分组，如 5×5 规模–价值分组。

**Time-series regression** — Regressing one asset's returns over time on
contemporaneous factor returns; yields alpha and betas. —— 对单个资产做时间序列回归，得到 alpha 和 beta。

**t-statistic** — Estimate divided by its standard error; |t| > 2 ≈
significant at 5%. —— 估计值除以标准误；|t|>2 约等于 5% 显著。

**p-value** — Probability of seeing a result this extreme if the null were
true; small p ⇒ reject the null. —— p 值；很小时拒绝原假设。

**R² / adjusted R²** — Share of return variance explained by the model
(adjusted penalizes extra regressors). —— 模型解释的收益方差比例（调整后 R² 惩罚多加变量）。

**Sharpe ratio** — Mean excess return per unit of volatility (annualized here).
—— 单位波动换来的超额收益（年化）。

**GRS test** — Gibbons–Ross–Shanken (1989) F-test of the joint hypothesis that
*all* alphas are zero; the formal scoreboard for a factor model. —— 检验所有 alpha 联合为零的 F 检验；因子模型的正式记分牌。

**Anomaly** — A return pattern the benchmark model cannot explain (e.g., the
value premium under the CAPM). —— 基准模型解释不了的收益模式。

**Risk premium** — Extra expected return for bearing a risk. —— 承担风险应得的额外期望收益。

**Distress risk** — Bankruptcy/financial-distress risk; the risk-based story
for why value stocks earn more. —— 财务困境风险；价值溢价的风险解释。

**Mispricing / behavioral story** — The rival story: premia come from
investor biases corrected slowly (limits of arbitrage). —— 错误定价/行为解释：溢价来自投资者偏差的缓慢修正。

**Out-of-sample test** — Testing on data not used to design the model; the
antidote to data mining. —— 在没参与模型设计的数据上检验；对付数据挖掘的解药。

**Data mining** — Finding spurious patterns by searching many specifications
on one dataset. —— 在同一数据上试很多设定试出来的假规律。

**Factor zoo** — The hundreds of proposed factors, most of which do not
survive scrutiny (Cochrane, 2011). —— 几百个被提出过的因子，大多经不起检验。

**Joint-hypothesis problem** — Any efficiency test is simultaneously a test
of the pricing model used (Fama, 1970). —— 任何市场有效性检验都同时是对所用定价模型的检验。

**Dividend-discount / valuation equation** — The Miller–Modigliani identity
linking expected returns to book-to-market, profitability, and investment;
the theoretical motivation for RMW and CMA. —— 联系期望收益与账面市值比、盈利、投资的恒等式；RMW/CMA 的理论动机。

**Newey–West standard errors** — Standard errors robust to autocorrelation and
heteroskedasticity; a standard robustness check omitted here. —— 对自相关和异方差稳健的标准误；本报告没做，可作稳健性扩展。
