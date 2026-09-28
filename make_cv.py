# -*- coding: utf-8 -*-
"""Generate one differentiated CV per company. Templates vary: headline/role,
skills emphasis, experience order, and project order per employer type."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

try:
    pdfmetrics.registerFont(TTFont("Sans", r"C:\Windows\Fonts\arial.ttf"))
    FONT = "Sans"
except Exception:
    FONT = "Helvetica"

NAVY = "#12233c"; MUTED = "#4d5c72"; AQUA = "#0d8f82"
ss = {
    "name": ParagraphStyle("name", fontName=FONT, fontSize=19, leading=22, textColor=NAVY, spaceAfter=2),
    "contact": ParagraphStyle("contact", fontName=FONT, fontSize=8.6, leading=11, textColor=MUTED, alignment=TA_CENTER),
    "headline": ParagraphStyle("headline", fontName=FONT, fontSize=8.8, leading=11, textColor=AQUA, alignment=TA_CENTER),
    "h2": ParagraphStyle("h2", fontName=FONT, fontSize=10.2, leading=12, textColor=NAVY, spaceBefore=7, spaceAfter=1.5),
    "job": ParagraphStyle("job", fontName=FONT, fontSize=9.1, leading=11, textColor=NAVY, spaceBefore=3.5),
    "bullet": ParagraphStyle("bullet", fontName=FONT, fontSize=8.5, leading=10.6, leftIndent=10, bulletIndent=2, spaceBefore=0.8),
    "small": ParagraphStyle("small", fontName=FONT, fontSize=8.3, leading=10.4),
}

def h2(text):
    return [Paragraph(f"<font color='#0d8f82'><b>{text.upper()}</b></font>", ss["h2"]),
            HRFlowable(width="100%", thickness=0.7, color="#c9d4e0", spaceAfter=2.5)]

EDU = [
    "<b>Cornell University</b>, College of Engineering, Ithaca, NY \u2014 <i>Master of Engineering, Financial Engineering</i> (Expected Dec 2027)",
    "<b>The University of Hong Kong</b> \u2014 <i>BSc Mathematics, Minor in Computer Science</i>, First Class Honours, GPA 3.74/4.0 (Jun 2026)",
    "<b>University of Oxford</b> \u2014 Visiting Student in Mathematics, ROA scholarship (Jul 2025)",
]

DYMON = ("<b>Quantitative Researcher</b> \u2014 Dymon Asia Capital (HK) Ltd, <i>Hong Kong</i>", "May \u2013 Aug 2026",
    ["Researched <b>Hang Seng Composite &amp; Tech Index</b> rebalancing rules to predict constituent additions/deletions before official announcements; translated published methodologies into point-in-time eligibility, liquidity, market-cap and buffer-selection logic.",
     "Built an auditable ranked-waterfall Python pipeline integrating FactSet, ERD and HKEX filings, with DeepSeek-assisted Theme/Innovation gates and a filing-based free-float engine mapping shareholder evidence to the ten HSIL categories.",
     "Achieved an <b>82.6% action-level hit rate</b> (185/224 additions and deletions) across the latest three HSCI rebalances in leakage-controlled, point-in-time evaluation."])
RIVERMAP = ("<b>Quantitative Researcher Intern</b> \u2014 Rivermap Company Ltd, <i>Hong Kong</i>", "Feb \u2013 Apr 2026",
    ["Automated thematic stock selection by translating unstructured investment themes into supply-chain dimensions mapped to proprietary sector taxonomy.",
     "Built a Python/pandas pipeline integrating sector, revenue-segment and company-description data with auditable intermediate outputs and relevance diagnostics.",
     "Designed a two-stage semantic retrieval pipeline (BGE embeddings + cosine similarity, then DeepSeek-based refinement) for ambiguous theme queries."])
NINE = ("<b>Quantitative Strategy Analyst Intern</b> \u2014 Nine Martingale Investment Management, <i>Shanghai</i>", "Jul \u2013 Sep 2025",
    ["Identified a 60-day dividend-event data lag and corrected factor alignment, raising information coefficient by 0.02.",
     "Built a factor-backtesting framework improving annualized return by 6% and Sharpe ratio by 0.3 over five years.",
     "Analyzed daily exposures to 10 Barra style factors to characterize signals and style tilts."])
NORTHEAST = ("<b>Quantitative Strategy Analyst Intern</b> \u2014 Northeast Securities Co., Ltd, <i>Shanghai</i>", "Jul \u2013 Sep 2024",
    ["Developed mean\u2013variance and risk-parity models within a 15-year daily-rebalanced backtesting framework.",
     "Implemented a Monte Carlo approach approximating equal-risk-contribution weights by minimizing asset risk-contribution differences."])
HKU_QT = ("<b>Researcher</b> \u2014 HKU Quant Trading Team, <i>Hong Kong</i>", "Feb \u2013 Aug 2026",
    ["Analyzed historical Polymarket data for systematic price-vs-outcome gaps; grouped contracts by topic, structure and time to resolution; flagged Yes/No shares with pricing gaps above 3 percentage points.",
     "Built a Python pipeline scanning live markets, ranking opportunities, enforcing position limits, simulating/submitting orders via the Polymarket order book, and tracking realized P&amp;L."])
OXFORD = ("<b>Independent Researcher</b> \u2014 University of Oxford, <i>Oxford, UK</i>", "Jan \u2013 Jun 2025",
    ["Modeled Lightning Network channel management as a discounted MDP; derived optimal routing, liquidity-reset and channel-capacity policies under stochastic payment flows.",
     "Implemented value iteration for discrete and exponential payment distributions, showing bidirectional flows naturally rebalance liquidity."])

SK = {
 "quant": "<b>Quantitative:</b> systematic alpha research, index rebalancing prediction (Hang Seng family), point-in-time backtesting, factor models (Barra), performance attribution &nbsp;|&nbsp; <b>Technical:</b> Python (pandas, numpy), C++, R, SQL, Linux, Git &nbsp;|&nbsp; <b>AI/ML:</b> embedding-based retrieval (BGE), LLM pipelines (DeepSeek), fine-tuning workflows &nbsp;|&nbsp; <b>Languages:</b> Mandarin (native), English (fluent)",
 "trading": "<b>Markets &amp; Execution:</b> order-book microstructure, position limits, live opportunity scanning, realized P&amp;L tracking &nbsp;|&nbsp; <b>Quantitative:</b> probability &amp; expected-value reasoning, systematic strategy backtesting, factor models &nbsp;|&nbsp; <b>Technical:</b> Python (pandas, numpy), C++, R, SQL, Linux, Git &nbsp;|&nbsp; <b>Languages:</b> Mandarin (native), English (fluent)",
 "bank": "<b>Pricing &amp; Risk:</b> Monte Carlo simulation, mean\u2013variance &amp; risk-parity optimization, Barra factor risk decomposition, backtesting frameworks &nbsp;|&nbsp; <b>Technical:</b> Python (pandas, numpy), C++, R, SQL, Linux, Git &nbsp;|&nbsp; <b>Coursework:</b> Convex Optimization, Machine Learning, Data Structures &amp; Algorithms &nbsp;|&nbsp; <b>Languages:</b> Mandarin (native), English (fluent)",
 "am": "<b>Investment Research:</b> systematic stock selection, thematic &amp; supply-chain analysis, index methodology, factor models &nbsp;|&nbsp; <b>Technical:</b> Python (pandas, numpy), C++, R, SQL, Linux, Git &nbsp;|&nbsp; <b>AI/ML:</b> embedding-based retrieval, LLM pipelines &nbsp;|&nbsp; <b>Languages:</b> Mandarin (native), English (fluent)",
}

ORDERS = {
 "quant":  {"exp": [DYMON, RIVERMAP, NINE, NORTHEAST], "proj": [HKU_QT, OXFORD]},
 "trading":{"exp": [DYMON, NINE, NORTHEAST, RIVERMAP], "proj": [HKU_QT, OXFORD]},
 "bank":   {"exp": [DYMON, NINE, NORTHEAST, RIVERMAP], "proj": [OXFORD, HKU_QT]},
 "am":     {"exp": [RIVERMAP, DYMON, NINE, NORTHEAST], "proj": [HKU_QT, OXFORD]},
}

# per-company config: (file-slug, template, role-for-headline)
CONFIG = [
 ("Millennium_MLP",            "quant",   "2027 Quantitative Researcher Intern, Hong Kong"),
 ("Jane_Street",                "trading", "Trading & Research Intern (Hong Kong), Summer 2027"),
 ("Citadel_Securities",         "trading", "Quantitative Research / Trading Intern, Summer 2027"),
 ("Point72",                    "quant",   "Academy Investment Analyst Summer Internship 2027, Hong Kong"),
 ("Two_Sigma",                  "quant",   "Quantitative Research Intern, Summer 2027"),
 ("Optiver",                    "trading", "Quantitative Intern, Summer 2027"),
 ("SIG_Susquehanna",            "trading", "Quantitative Systematic Trading Intern, Summer 2027"),
 ("IMC_QR",                     "quant",   "Quantitative Research Intern 2027, Hong Kong"),
 ("DE_Shaw",                    "quant",   "Quantitative Analyst Intern, Summer 2027, Hong Kong"),
 ("DRW",                        "trading", "Quantitative / Technology Internship, Summer 2027"),
 ("Flow_Traders",               "trading", "Trading / Quant Internship, Hong Kong"),
 ("Mako",                       "trading", "Quant / SWE Internship, Hong Kong"),
 ("Squarepoint",                "quant",   "Quantitative Research / Developer Internship 2027"),
 ("WorldQuant",                 "quant",   "Quantitative Researcher Intern / Research Consultant"),
 ("Ubiquant",                   "quant",   "Quantitative Research Intern (Hong Kong office), \u91dc\u676d/\u9999\u6e2f"),
 ("High_Flyer",                 "quant",   "Quantitative Research Intern (\u91cf\u5316\u7814\u7a76\u5b9e\u4e60\u751f)"),
 ("Minghong",                   "quant",   "Quantitative Research Intern, Hong Kong / Shanghai"),
 ("Dymon_Asia",                 "quant",   "Summer 2027 Quantitative Research (return), Hong Kong"),
 ("Wincent",                    "trading", "Quantitative Research / Trading Intern, Summer 2027, Hong Kong"),
 ("Jain_Global",                "bank",    "Risk Quant Modeller Intern, Hong Kong"),
 ("Lingjun",                    "quant",   "Quantitative Researcher Intern \u2014 Hong Kong office (\u7075\u5747\u6295\u8d44)"),
 ("Wizard_Quant",               "quant",   "Quantitative Researcher Intern (\u5bbd\u5fb7, internship-to-partner track)"),
 ("AQR",                        "quant",   "Quantitative Research Summer Internship 2027"),
 ("Bank_of_America_GQS",        "bank",    "Global Quantitative Strategies Summer Associate 2027, Hong Kong"),
 ("Bank_of_America_Markets",    "trading", "Global Markets Sales & Trading Rotational Summer Analyst 2027, Hong Kong"),
 ("Barclays_QA",                "bank",    "Quantitative Analytics Associate Off-Cycle Internship 2027, Hong Kong"),
 ("Barclays_ET",                "bank",    "Electronic Trading Associate Summer Internship 2027, Hong Kong"),
 ("UBS_Quants",                 "bank",    "Investment Bank Quants Off-Cycle Internship, Hong Kong"),
 ("Goldman_Sachs_Strats",       "bank",    "2027 Summer Analyst \u2014 Strats, Hong Kong / APAC"),
 ("JPMorgan_MarketsQR",         "trading", "Markets Quantitative Trading & Research Analyst Program \u2014 Off-Cycle Internship 2027, Hong Kong"),
 ("JPMorgan_Markets",           "trading", "CIB Markets Summer Analyst Program 2027, Hong Kong (Sales & Trading)"),
 ("Morgan_Stanley",             "bank",    "2027 IED Quantitative Finance Summer Analyst/Associate, Hong Kong"),
 ("Citi",                       "bank",    "Investment Banking / Markets Summer Analyst 2027, Hong Kong"),
 ("Deutsche_Bank",              "bank",    "2027 Summer Internship \u2014 Markets & Quant, Hong Kong"),
 ("HSBC",                       "bank",    "Global Banking & Markets Summer Internship 2027, Hong Kong"),
 ("Nomura",                     "bank",    "Summer Analyst 2027 \u2014 Markets / Quant, Hong Kong"),
 ("Wells_Fargo",                "bank",    "2027 APAC Banking Summer Analyst, Hong Kong"),
 ("Jefferies_Macquarie",        "bank",    "Summer Internship 2027 \u2014 Markets / Quant, Hong Kong"),
 ("BlackRock",                  "am",      "2027 Summer Internship Program, APAC"),
 ("Fidelity_International",     "am",      "Summer Internship 2027 (Investment Directing), Hong Kong"),
 ("PIMCO",                      "am",      "APAC Summer Internship 2027, Hong Kong"),
 ("Schroders",                  "am",      "Summer Internship 2027 (Investment / Quant), Hong Kong"),
 ("Ares",                       "am",      "Summer 2027 Internship Program, APAC"),
]

def job(title, dates, items):
    return [Paragraph(f"{title} &nbsp;<font color='#68758a' size='7.6'>{dates}</font>", ss["job"])] + \
           [Paragraph(t, ss["bullet"], bulletText="\u2022") for t in items]

def build(path, role, template):
    order = ORDERS[template]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=14*mm, rightMargin=14*mm, topMargin=11*mm, bottomMargin=10*mm,
                            title=f"Jing Xiang Xu - {role}", author="Jing Xiang Xu")
    story = [
        Paragraph("<b>JING XIANG XU</b>", ss["name"]),
        Paragraph("Hong Kong &nbsp;\u00b7&nbsp; jx466@cornell.edu &nbsp;\u00b7&nbsp; +852 6810 9521 (HK) / +1 607-882-5108 &nbsp;\u00b7&nbsp; Available June \u2013 August 2027", ss["contact"]),
        Paragraph(f"Applying: <b>{role}</b> &nbsp;\u00b7&nbsp; Penultimate-year Master\u2019s student graduating Dec 2027", ss["headline"]),
        Spacer(1, 2),
    ]
    story += h2("Education")
    for line in EDU:
        story.append(Paragraph(line, ss["small"]))
    story += h2("Skills")
    story.append(Paragraph(SK[template], ss["small"]))
    story += h2("Experience")
    for j in order["exp"]:
        story += job(*j)
    story += h2("Projects &amp; Research")
    for j in order["proj"]:
        story += job(*j)
    story += h2("Activities")
    story.append(Paragraph("HKU Young Scientist Scheme &nbsp;\u00b7&nbsp; F1 racing &nbsp;\u00b7&nbsp; Poker (applied probability) &nbsp;\u00b7&nbsp; Running", ss["small"]))
    doc.build(story)

os.makedirs(r"D:\zcode\hk-dashboard\cv", exist_ok=True)
os.chdir(r"D:\zcode\hk-dashboard\cv")
for slug, template, role in CONFIG:
    fn = f"Xu_Jingxiang_{slug}_CV.pdf"
    build(fn, role, template)
print(f"generated {len(CONFIG)} CVs")
