# -*- coding: utf-8 -*-
"""Differentiated cover letters for the companies that request/recommend one."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os, datetime

try:
    pdfmetrics.registerFont(TTFont("Sans", r"C:\Windows\Fonts\arial.ttf"))
    FONT = "Sans"
except Exception:
    FONT = "Helvetica"

NAVY = "#12233c"; MUTED = "#4d5c72"
st = {
 "head": ParagraphStyle("head", fontName=FONT, fontSize=10, leading=13, textColor=NAVY),
 "meta": ParagraphStyle("meta", fontName=FONT, fontSize=8.8, leading=12, textColor=MUTED, spaceAfter=2),
 "body": ParagraphStyle("body", fontName=FONT, fontSize=9.4, leading=13.2, spaceAfter=7),
 "sign": ParagraphStyle("sign", fontName=FONT, fontSize=9.4, leading=13),
}

OPEN = ("Dear {salutation} Recruiting Team,\n\n"
        "I am writing to apply for the {role} in Hong Kong. I am a Master of Engineering student in "
        "Financial Engineering at Cornell University (graduating December 2027) and hold a First Class Honours BSc in "
        "Mathematics with a Computer Science minor from the University of Hong Kong, making this my penultimate summer and "
        "Hong Kong my home base.")

CLOSE = ("I would welcome the opportunity to discuss how my background can contribute to your team, and I am available "
         "for interviews at any time. Thank you for your consideration.\n\nSincerely,\nJing Xiang Xu\n"
         "jx466@cornell.edu · +1 607-882-5108")

# per-company: (slug, salutation, role, [tailored middle paragraphs])
LETTERS = [
 ("Bank_of_America_GQS","Bank of America","Global Quantitative Strategies Summer Associate Program 2027",[
  "At Dymon Asia Capital in Hong Kong I built the quantitative machinery your strategists use daily: I reverse-engineered the "
  "Hang Seng Composite and Tech Index rebalancing methodologies into point-in-time eligibility, liquidity and buffer-selection "
  "logic, and delivered an auditable Python pipeline across FactSet, ERD and HKEX filings that achieved an 82.6% action-level "
  "hit rate on three live rebalances. Earlier roles at Nine Martingale and Northeast Securities added factor backtesting, Barra "
  "exposure analysis, and Monte Carlo risk-parity optimization \u2014 the modeling toolkit BofA GQS applies to derivatives, "
  "electronic markets and risk analytics.",
  "I fit the program\u2019s stated profile directly: object-oriented programming in Python and C++; hands-on AI/ML experience "
  "(embedding-based retrieval and LLM-assisted research pipelines in production internships); a Mathematics degree with CS minor "
  "from HKU now deepened by Cornell financial engineering; and native Mandarin on top of fluent English \u2014 the additional "
  "Asian language the posting flags as advantageous, and daily currency for covering APAC markets from Hong Kong.",
  "What draws me to GQS specifically is the chance to work at the intersection of quantitative research and client-facing "
  "solutions in APAC markets I already know deeply, within a bank whose Hong Kong franchise sits at the center of regional "
  "capital flows."]),
 ("Barclays_QA","Barclays","Quantitative Analytics Associate Off-Cycle Internship 2027",[
  "My training maps directly onto Quantitative Analytics work: at Nine Martingale I built a five-year factor-backtesting "
  "framework (improving annualized return by 6% and Sharpe by 0.3) and decomposed daily exposures across ten Barra style "
  "factors; at Northeast Securities I implemented Monte Carlo engines and mean\u2013variance/risk-parity optimizers inside a "
  "15-year daily-rebalanced backtest. At Dymon Asia I added production-grade data hygiene \u2014 point-in-time reconstruction "
  "of index methodology from HKEX filings \u2014 which is exactly the rigor model validation demands.",
  "The six-month Hong Kong structure suits my Cornell program, and Barclays\u2019 quant culture of publishing and debating "
  "research internally matches how I work best."]),
 ("Barclays_ET","Barclays","Electronic Trading Associate Summer Internship 2027",[
  "Electronic markets are where my experience is most concrete: at Dymon Asia I modeled index-rebalancing flows that drive "
  "predictable trading volume, and with the HKU Quant Trading Team I built a full pipeline that scans live order books, ranks "
  "opportunities, enforces position limits, submits orders and tracks realized P&L on Polymarket \u2014 effectively a small "
  "systematic trading desk in code.",
  "I am applying to the Hong Kong program to work on APAC electronic execution where my Mandarin and English let me liaise "
  "with regional exchanges, brokers and internal stakeholders without friction."]),
 ("Deutsche_Bank","Deutsche Bank","2027 Summer Internship Programme \u2014 Markets & Quant, Hong Kong",[
  "Across three prior internships I have owned research end-to-end: at Dymon Asia (HK) I predicted Hang Seng index "
  "reconstitutions with an 82.6% action-level hit rate; at Nine Martingale I repaired a dividend-event data lag that lifted "
  "information coefficient by 0.02; at Northeast Securities I built mean\u2013variance and Monte Carlo risk-parity engines over "
  "15 years of daily data.",
  "Deutsche Bank\u2019s Markets franchise in Hong Kong, and its investment in electrification of flow and quant analytics in "
  "APAC, is exactly where I want to convert these skills from a fund-side seat to a sell-side one."]),
 ("HSBC","HSBC","Global Banking & Markets Summer Internship 2027",[
  "As a Hong Kong-based mathematics graduate of HKU who has already worked in two Hong Kong financial firms (Dymon Asia, "
  "Rivermap), I bring both the quantitative craft \u2014 index rebalancing prediction with an 82.6% hit rate, factor "
  "backtesting, Monte Carlo risk models \u2014 and the local market fluency your APAC franchise is built on.",
  "HSBC\u2019s pan-Asian footprint and its pivot toward technology-driven markets businesses make this the place where a "
  "bilingual quant with mainland and Hong market experience adds the most value."]),
 ("Nomura","Nomura","Summer Analyst 2027 \u2014 Markets / Quant, Hong Kong",[
  "Japan\u2019s and Asia\u2019s index landscapes share the rebalancing mechanics I researched at Dymon Asia: point-in-time "
  "eligibility screens, liquidity buffers and free-float categorization, where I achieved an 82.6% action-level prediction "
  "hit rate on Hang Seng reconstitutions using only public filings.",
  "Nomura\u2019s strength in APAC derivatives and structured markets is where my Oxford-trained stochastic modeling and "
  "Cornell financial engineering coursework compound most naturally, and Hong Kong is where I intend to build my career."]),
 ("Wells_Fargo","Wells Fargo","2027 APAC Banking Summer Analyst, Hong Kong",[
  "My internship record pairs quantitative research with disciplined execution: quant research at Dymon Asia and Rivermap in "
  "Hong Kong, factor and risk modeling at Nine Martingale and Northeast Securities in Shanghai \u2014 each role ending in "
  "measurable improvements (82.6% prediction hit rate; +6% annualized backtest return; +0.3 Sharpe).",
  "Wells Fargo\u2019s growing APAC platform offers the chance to apply that rigor to regional markets with a team that "
  "values analytical, build-it-yourself analysts."]),
 ("Point72","Point72","Academy Investment Analyst Summer Internship Program 2027",[
  "The Academy\u2019s mission \u2014 turning rigorous, non-traditional talent into discretionary analysts through structured "
  "training \u2014 fits me precisely. My edge is building data-driven research where none exists: at Dymon Asia I predicted "
  "Hang Seng constituent changes with an 82.6% action-level hit rate before official announcements; at Rivermap I automated "
  "thematic stock selection by translating unstructured themes into supply-chain dimensions with embedding-based retrieval; "
  "with HKU\u2019s quant trading team I ran a live Polymarket book and tracked realized P&L.",
  "I read markets probabilistically (poker, prediction markets) and build my own tooling (Python, LLM-assisted research "
  "pipelines). I want to sharpen that raw material into fundamental investing judgment under the Academy\u2019s mentors, in "
  "Hong Kong, where I already live and work."]),
 ("BlackRock","BlackRock","2027 Summer Internship Program, APAC",[
  "BlackRock\u2019s technology-first identity matches how I already work: I build auditable research pipelines rather than "
  "spreadsheets. At Dymon Asia my pipeline reconstructed Hang Seng index methodology point-in-time and hit 82.6% on "
  "constituent-change prediction; at Rivermap I automated thematic screening with a two-stage semantic retrieval system; "
  "these are the same inputs Aladdin and systematic strategies are built on.",
  "An APAC internship would let me apply index methodology, factor analytics and AI-augmented research to the region\u2019s "
  "markets from Hong Kong, where I completed my undergraduate degree and both of my Hong Kong internships."]),
 ("Fidelity_International","Fidelity International","Summer Internship 2027 (Investment Directing), Hong Kong",[
  "Investment directing demands people who can connect investment content with implementation \u2014 my exact profile. At "
  "Rivermap I translated unstructured investment themes into auditable portfolio-relevant dimensions; at Dymon Asia I turned "
  "index rulebooks into actionable rebalancing forecasts (82.6% hit rate); at Nine Martingale I aligned factors, data and "
  "backtests tightly enough to add 0.02 IC.",
  "Fidelity\u2019s long-horizon, research-deep culture in Hong Kong is where I want to develop as an investor who both "
  "models and decides."]),
 ("PIMCO","PIMCO","APAC Summer Internship 2027, Hong Kong",[
  "PIMCO\u2019s analytical, debate-driven culture suits how I work: I build evidence, then defend it. My Oxford research "
  "optimized liquidity policy under stochastic flows; my Dymon Asia work forecast index-driven flows with an 82.6% hit rate "
  "\u2014 flows that matter directly to bond index implementation and passive tracking in APAC credit and rates.",
  "I am completing Cornell\u2019s financial engineering program precisely to add fixed-income and macro depth to an "
  "equities-heavy internship record, and Hong Kong is my home base for APAC coverage."]),
 ("Schroders","Schroders","Summer Internship 2027 (Investment / Quant), Hong Kong",[
  "At Schroders the quant and fundamental traditions meet \u2014 and so do I. My Dymon Asia research (82.6% hit rate "
  "predicting Hang Seng rebalances) served discretionary portfolio decisions; my Rivermap work automated thematic screening "
  "for fundamental analysts; my HKU quant team ran a live systematic book.",
  "As an HKU graduate based in Hong Kong with active Mandarin and English, I can support both the local franchise and "
  "mainland-oriented mandates from day one."]),
 ("Ares","Ares Management","Summer 2027 Internship Program, APAC",[
  "Alternative managers live on information advantage in less-efficient markets \u2014 the environment where my research "
  "style wins. My Polymarket research at HKU found systematic mispricings above 3 percentage points and monetized them "
  "through a live order-book pipeline; my Dymon Asia work extracted a tradable edge (82.6% hit rate) from public index "
  "methodology alone.",
  "Ares\u2019 APAC growth and credit heritage make Hong Kong the place I want to apply that edge-hunting instinct to "
  "private and alternative credit markets."]),
]

os.makedirs(r"D:\zcode\hk-dashboard\cover-letters", exist_ok=True)
os.chdir(r"D:\zcode\hk-dashboard\cover-letters")
for slug, salut, role, mids in LETTERS:
    text = OPEN.format(salutation=salut, role=role) + "\n\n" + "\n\n".join(mids) + "\n\n" + CLOSE
    doc = SimpleDocTemplate(f"Xu_Jingxiang_{slug}_Cover_Letter.pdf", pagesize=A4,
                            leftMargin=20*mm, rightMargin=20*mm, topMargin=16*mm, bottomMargin=14*mm,
                            title=f"Cover Letter - {role}", author="Jing Xiang Xu")
    story = [
        Paragraph("<b>JING XIANG XU</b>", st["head"]),
        Paragraph("Hong Kong · jx466@cornell.edu · +1 607-882-5108", st["meta"]),
        Paragraph(f"{datetime.date(2026,9,26).strftime('%B %d, %Y')}", st["meta"]),
        Spacer(1, 6),
    ]
    for para in text.split("\n\n"):
        story.append(Paragraph(para.replace("\n", "<br/>"), st["body"]))
    doc.build(story)
print(f"generated {len(LETTERS)} cover letters")
