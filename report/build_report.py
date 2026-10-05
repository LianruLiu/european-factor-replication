#!/usr/bin/env python3
"""Render report/REPORT.md as a professional PDF (ASCII-safe transcription)."""
from fpdf import FPDF
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "results" / "figures"

DARK = (25, 25, 25)
GRAY = (90, 90, 90)
ACCENT = (30, 70, 130)
RULE = (190, 190, 190)


class Report(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.set_margins(20, 18, 20)
        self.set_auto_page_break(True, margin=18)

    def rule(self):
        self.set_draw_color(*RULE); self.set_line_width(0.4)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y)
        self.ln(4)

    def title_block(self, title, meta):
        self.set_font("Helvetica", "B", 20); self.set_text_color(*DARK)
        self.multi_cell(0, 8, title, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        self.set_font("Helvetica", "", 10); self.set_text_color(*GRAY)
        for m in meta:
            self.cell(0, 5, m, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2); self.rule()

    def h2(self, text):
        self.ln(3)
        self.set_font("Helvetica", "B", 13); self.set_text_color(*ACCENT)
        self.multi_cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def h3(self, text):
        self.ln(2)
        self.set_font("Helvetica", "B", 11); self.set_text_color(*DARK)
        self.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def para(self, text, italic=False):
        self.set_font("Helvetica", "I" if italic else "", 10)
        self.set_text_color(*DARK)
        self.multi_cell(0, 5.2, text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)

    def quote(self, text):
        x = self.get_x()
        self.set_x(x + 6)
        self.set_font("Helvetica", "I", 10); self.set_text_color(*GRAY)
        self.multi_cell(self.w - self.l_margin - self.r_margin - 6, 5.2, text,
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(1.5)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10); self.set_text_color(*DARK)
        x0, w = self.get_x(), self.w - self.l_margin - self.r_margin
        self.set_x(x0 + 5)
        self.multi_cell(w - 5, 5.2, "- " + text, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def table(self, headers, rows, col_widths=None, fontsize=9):
        w = self.w - self.l_margin - self.r_margin
        n = len(headers)
        if col_widths is None:
            col_widths = [w / n] * n
        self.set_font("Helvetica", "B", fontsize); self.set_text_color(*DARK)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 6, h, border=0, new_x="END")
        self.ln()
        self.set_draw_color(*RULE); self.set_line_width(0.3)
        y = self.get_y()
        self.line(self.l_margin, y, self.w - self.r_margin, y); self.ln(1.5)
        self.set_font("Helvetica", "", fontsize)
        for r in rows:
            for i, c in enumerate(r):
                self.cell(col_widths[i], 5.5, str(c), new_x="END")
            self.ln()
        self.ln(3)

    def figure(self, path, caption, width=150):
        self.ln(2)
        x = (self.w - width) / 2
        self.image(str(path), x=x, w=width)
        self.ln(1)
        self.set_font("Helvetica", "I", 9); self.set_text_color(*GRAY)
        self.multi_cell(0, 4.5, caption, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)


def build(path):
    r = Report()
    r.add_page()
    r.title_block(
        "Replicating the Fama-French Factor Models\non European Equities (1990-2026)",
        ["Author: Lianru Liu", "Date: October 2026", "Status: Independent replication"],
    )

    # ---------------- Part I ----------------
    r.h2("Part I -- The academic questions behind the design")
    r.para("Every empirical asset-pricing model is an answer to a prior puzzle. "
           "This section organizes the questions that motivated the Fama-French factor "
           "design, and the knowledge needed to understand the answers.")

    r.h3("Q1. Why do average returns differ across stocks?")
    r.para("The foundational question of asset pricing: in a market where investors are "
           "risk-averse, expected returns should compensate for risk. The Capital Asset "
           "Pricing Model (Sharpe, 1964; Lintner, 1965) gives the sharpest version of this "
           "idea -- a single number, the market beta, should explain all cross-sectional "
           "differences in expected returns.")
    r.quote("E[Ri] - Rf = beta_i * (E[Rm] - Rf)")
    r.para("If the CAPM held exactly, sorting stocks by anything other than beta -- size, "
           "valuation ratios, past returns -- would reveal no return differences. The entire "
           "factor literature exists because it does not.")
    r.para("Related knowledge: expected vs. realized returns (we only ever observe realized "
           "returns; a factor 'premium' is the historical average of realized returns, an "
           "estimate of the ex-ante risk premium, not a guarantee); the joint-hypothesis "
           "problem (any test of market efficiency is simultaneously a test of the "
           "asset-pricing model used -- Fama, 1970).", italic=True)

    r.h3("Q2. Is the CAPM enough? The size and value anomalies")
    r.bullet("Size (Banz, 1981): small-capitalization stocks earned higher average returns "
             "than their market betas predicted.")
    r.bullet("Value (Fama & French, 1992): high book-to-market stocks earned higher average "
             "returns than growth stocks, even after controlling for beta and size. Once size "
             "and book-to-market were accounted for, market beta had almost no explanatory "
             "power left.")
    r.para("Fama and French (1993) turned these anomalies into factors: tradable long-short "
           "portfolios -- SMB (small minus big) and HML (high minus low book-to-market) -- "
           "and showed that a three-factor model absorbed most of the CAPM's pricing errors.")
    r.para("Related knowledge: anomaly (a return pattern unexplained by the benchmark model); "
           "sorting (forming portfolios by ranking stocks on a characteristic); long-short "
           "factor construction (e.g., 2x3 independent sorts on size and book-to-market).",
           italic=True)

    r.h3("Q3. Risk or mispricing? Competing explanations of the premia")
    r.bullet("Risk-based: value firms tend to be distressed; their high returns compensate "
             "investors for bearing distress/bankruptcy risk that market beta misses "
             "(Fama & French, 1996).")
    r.bullet("Behavioral: investors over-extrapolate past growth, overpaying for glamour "
             "stocks; the premium is the slow correction of mispricing (Lakonishok, Shleifer "
             "& Vishny, 1994).")
    r.para("This debate is unresolved -- but it is why the literature keeps score with "
           "alphas: any return the factors cannot explain is either missing risk or "
           "mispricing, and the GRS test (Part IV) is the formal scoreboard.")
    r.para("Related knowledge: alpha (abnormal return vs. the model); limits of arbitrage "
           "(why mispricing can persist).", italic=True)

    r.h3("Q4. Do U.S. results travel? Why Europe is the right out-of-sample test")
    r.para("A pattern found on U.S. data may be data mining -- an accidental discovery from "
           "searching many specifications on one dataset. The scientific response is "
           "out-of-sample testing: the same sorts, the same regressions, on data the "
           "original authors did not use to design the model. Europe is the natural "
           "laboratory: deep, liquid markets, long histories, and economic structures "
           "different enough from the U.S. that survival there is informative.")

    r.h3("Q5. From three factors to five: the valuation-equation logic")
    r.para("The five-factor model was not assembled by data mining. It follows from the "
           "Miller-Modigliani dividend-discount identity: holding everything else fixed, a "
           "stock's expected return is higher when its book-to-market ratio is higher, "
           "expected profitability is higher, and expected investment is lower. "
           "Profitability (Novy-Marx, 2013) and investment (Aharoni, Grundy & Zeng, 2013) "
           "patterns in returns therefore had to be related to expected returns -- the only "
           "question was whether the market already priced them. Fama and French (2015) "
           "added RMW and CMA and showed the five-factor model absorbed the anomalies -- "
           "notably the low returns of small, unprofitable, high-investment firms -- that "
           "embarrassed the three-factor model.")

    r.h3("Q6. The factor zoo: why replication discipline matters")
    r.para("Hundreds of 'factors' have been proposed (Cochrane, 2011, calls it the factor "
           "zoo). Most do not survive transaction costs, out-of-sample tests, or "
           "multiple-testing corrections. This replication practices the discipline the "
           "literature demands: pre-committed test assets (the 25 Size-B/M portfolios), a "
           "fixed sample, and a formal joint test (GRS) rather than cherry-picked "
           "t-statistics.")

    # ---------------- Part II ----------------
    r.h2("Part II -- Literature (concise tour)")
    lit = [
        ["Sharpe (1964); Lintner (1965)", "CAPM: market beta as the single priced risk"],
        ["Banz (1981)", "Size effect"],
        ["Fama & French (1992)", "B/M and size drive the cross-section; beta fades"],
        ["Fama & French (1993)", "Three-factor model: Mkt-RF, SMB, HML"],
        ["Lakonishok et al. (1994)", "Behavioral account of the value premium"],
        ["Fama & French (1996)", "Risk-based multifactor explanation of anomalies"],
        ["Carhart (1997)", "Momentum (WML) as a fourth factor"],
        ["Novy-Marx (2013)", "Gross profitability premium -> motivates RMW"],
        ["Aharoni et al. (2013)", "Investment effect -> motivates CMA"],
        ["Fama & French (2012)", "Size, value, momentum in international returns"],
        ["Fama & French (2015)", "Five-factor model adds RMW and CMA"],
        ["Gibbons, Ross & Shanken (1989)", "GRS F-test of joint alpha = 0"],
        ["Cochrane (2011)", "'Factor zoo' critique; discount-rate view"],
    ]
    r.table(["Study", "Contribution"], lit, col_widths=[62, 108], fontsize=8.5)
    r.para("Full citations: REFERENCES.md.", italic=True)

    # ---------------- Part III ----------------
    r.h2("Part III -- Data")
    r.bullet("Source: Kenneth R. French Data Library, files constructed from the August "
             "2026 Bloomberg database (free for research use; vendored in data/raw/).")
    r.bullet("Region: Europe (16 developed markets incl. the UK, Germany, France, Switzerland).")
    r.bullet("Factors (monthly): Mkt-RF, SMB, HML, RMW, CMA, RF. Factors are returns on "
             "diversified long-short portfolios from 2x3 sorts.")
    r.bullet("Test assets (monthly): 25 value-weighted portfolios from independent 5x5 sorts "
             "on market capitalization (Size) and book-to-market -- the classic Fama-French "
             "(1993) test assets, reformed each June.")
    r.bullet("Sample: July 1990 - August 2026, T = 434 months. Missing values (-99.99) "
             "treated as NaN; the common sample is used throughout.")

    # ---------------- Part IV ----------------
    r.h2("Part IV -- Methodology")
    r.para("For each test portfolio i, estimate by OLS:")
    r.quote("R(i,t) - Rf(t) = alpha(i) + b(i)*MKT(t) + s(i)*SMB(t) + h(i)*HML(t) "
            "[+ r(i)*RMW(t) + c(i)*CMA(t)] + e(i,t)")
    r.para("Reported per portfolio: annualized alpha, t(alpha), factor loadings with "
           "t-statistics, adjusted R-squared. Model comparison uses (1) the count of "
           "significant alphas (|t| > 2) out of 25, (2) mean adjusted R-squared, and "
           "(3) the Gibbons-Ross-Shanken F-test of H0: all 25 alphas = 0.")
    r.quote("F = (T/N) * [(T-N-K)/(T-K-1)] * (a' S^-1 a) / (1 + mu_f' Omega^-1 mu_f), "
            "distributed F(N, T-N-K),")
    r.para("where N = 25 test assets, K factors, S the residual covariance matrix, and "
           "mu_f, Omega the factor mean vector and covariance matrix. Rejection means the "
           "model's factors cannot jointly price the test assets.")
    r.para("Note on standard errors: t-statistics use OLS standard errors. Returns show "
           "mild autocorrelation/heteroskedasticity; Newey-West corrections would be a "
           "natural robustness extension (see Part VI).", italic=True)

    # ---------------- Part V ----------------
    r.h2("Part V -- Results")
    r.h3("5.1 Factor premia in Europe, 1990-2026")
    stats_rows = [
        ["Mkt-RF", "6.36%", "17.01%", "2.25", "0.37"],
        ["SMB", "0.15%", "7.23%", "0.12", "0.02"],
        ["HML", "4.24%", "9.01%", "2.83", "0.47"],
        ["RMW", "3.60%", "5.56%", "3.89", "0.65"],
        ["CMA", "1.71%", "6.21%", "1.66", "0.28"],
    ]
    r.table(["Factor", "Ann. mean", "Ann. vol", "t(mean)", "Sharpe"], stats_rows,
            col_widths=[30, 30, 30, 30, 30])
    r.para("Three facts stand out. First, the size premium is economically and "
           "statistically zero in Europe (0.15%/yr, t = 0.12) -- consistent with the "
           "documented post-publication decay of the size effect. Second, value and "
           "profitability premia are alive: HML earns 4.24%/yr (t = 2.83) and RMW 3.60%/yr "
           "(t = 3.89, Sharpe 0.65, the strongest risk-adjusted premium). Third, the "
           "investment premium is positive but marginal (t = 1.66).")
    r.figure(FIG / "factor_cumulative.png",
             "Figure 1. Cumulative returns of the five European Fama-French factors "
             "(July 1990 = 1).")

    r.h3("5.2 Do the models price the 25 Size-B/M portfolios?")
    r.bullet("Factor loadings behave as theory predicts. Within every size quintile, HML "
             "loadings rise monotonically with book-to-market (smallest quintile: -0.43, "
             "-0.24, -0.10, 0.09, 0.35). Mean adjusted R-squared is 0.942 (FF3) and "
             "0.946 (FF5).")
    r.bullet('The small-growth problem replicates -- and the five-factor model halves it. '
             "The small-growth portfolio earns an FF3 alpha of -5.16%/yr (t = -4.94), the "
             "largest pricing error in the cross-section. Under FF5 it shrinks to -2.43%/yr "
             "(t = -2.38): negative RMW (-0.48) and CMA (-0.26) loadings show these firms "
             "are unprofitable high-investors -- exactly the anomaly the two added factors "
             "were designed to absorb. Big-value's FF3 alpha (-2.34%/yr, t = -2.44) likewise "
             "vanishes under FF5 (+0.06%/yr).")
    r.bullet("Scoreboard: significant alphas (|t| > 2) fall from 8 of 25 (FF3) to 6 of 25 "
             "(FF5). The GRS test rejects joint alpha = 0 for both models -- FF3: F = 3.05 "
             "(p < 0.001); FF5: F = 2.71 (p < 0.001) -- so neither model fully prices "
             "European equities, but the five-factor model prices them better, mirroring "
             "the U.S. verdict of Fama and French (2015).")
    r.figure(FIG / "alphas_ff3_ff5.png",
             "Figure 2. Annualized alphas: 25 European Size-B/M portfolios, FF3 vs FF5.")

    r.h3("5.3 Dynamics")
    r.para("HML's 12-month rolling mean shows the value premium is highly time-varying: "
           "deeply negative during the late-1990s tech boom and the 2020 growth rally "
           "(HML lost -30.1% in 2020 alone), violently positive in recoveries (+29.6% in "
           "2025). The premium is compensation for enduring bad times, not a free lunch -- "
           "the core intuition of the risk-based story in Q3.")
    r.figure(FIG / "hml_rolling.png",
             "Figure 3. HML (value premium), 12-month rolling mean, Europe.")

    # ---------------- Part VI ----------------
    r.h2("Part VI -- Conclusion and limitations")
    r.h3("What we learn")
    r.bullet("The value and profitability premia survive out-of-sample in Europe; the size "
             "premium does not.")
    r.bullet("The five-factor model's added factors earn their keep precisely where theory "
             "said they would -- small, unprofitable, high-investment firms.")
    r.bullet("Formally, both models are rejected: factor models are useful approximations, "
             "not literal truth.")
    r.h3("Limitations")
    r.bullet("Test assets are value-weighted portfolios, tradable only approximately; no "
             "transaction costs are modeled.")
    r.bullet("OLS standard errors -- Newey-West (1987) corrections are a standard "
             "robustness check, omitted here for clarity.")
    r.bullet("One region, one sort. Results are conditional on the 25 Size-B/M design; "
             "other test assets could tell a different story -- the classic "
             "joint-hypothesis caveat.")
    r.bullet("No investment implication. Historical premia do not predict future returns; "
             "see the disclaimer in the README.")

    r.h2("References & glossary")
    r.para("Full citations: REFERENCES.md. Terminology (English + Chinese): GLOSSARY.md.",
           italic=True)

    r.output(str(ROOT / "report" / "REPORT.pdf"))
    print("wrote REPORT.pdf | pages:", r.pages_count)


if __name__ == "__main__":
    build(None)
