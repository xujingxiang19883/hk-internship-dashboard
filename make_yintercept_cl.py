# -*- coding: utf-8 -*-
"""Y-Intercept (HK) QR Intern cover letter - tailored to Greenhouse JD 4000160201."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import datetime

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
}

text = (
"Dear Y-Intercept Recruiting Team,\n\n"
"I am applying for the Quantitative Researcher Intern position at your Central office. I am a Master of Engineering student in "
"Financial Engineering at Cornell (graduating December 2027) and completed my BSc in Mathematics with First Class Honours at the "
"University of Hong Kong this June; I hold an IANG visa with unrestricted right to work in Hong Kong and can commit to the full "
"three-to-six-month internship from summer 2027.\n\n"
"The role\u2019s focus \u2014 designing and testing predictive statistical models, mining unconventional data for new signals, and "
"monitoring strategy performance and risk \u2014 mirrors how I already work. At Dymon Asia Capital in Hong Kong I predicted Hang Seng "
"Composite and Tech Index constituent changes before official announcements: translating published methodologies into point-in-time "
"eligibility, liquidity and buffer logic, building an auditable Python pipeline over FactSet, ERD and HKEX filings, and achieving an "
"82.6% action-level hit rate (185/224) across three live rebalances in leakage-controlled evaluation. At Rivermap I mined "
"company-description and revenue-segment data into tradable themes using a two-stage semantic retrieval pipeline (BGE embeddings, then "
"LLM-based refinement). At Nine Martingale I built a factor-backtesting framework (annualized return +6%, Sharpe +0.3) and corrected a "
"60-day dividend-event data lag, raising information coefficient by 0.02 \u2014 hands-on experience with exactly the data-integrity and "
"performance-analysis work your researchers do daily.\n\n"
"Your requirements align directly: probability and statistics (HKU mathematics, Cornell convex optimization and machine learning "
"coursework), machine learning and pattern recognition (embedding retrieval and LLM pipelines in production internships), and Python and "
"SQL as my primary tools. Just as importantly, Hong Kong is my home market \u2014 I studied and interned here, work natively in Mandarin "
"and English, and want to build my career in the city where Y-Intercept trades. I would welcome the chance to contribute to your team "
"and am available for interviews at any time.\n\n"
"Sincerely,\nJing Xiang Xu\njx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108"
)

out = r"D:\zcode\hk-dashboard\cover-letters\Xu_Jingxiang_YIntercept_Cover_Letter.pdf"
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=16*mm, bottomMargin=14*mm,
                        title="Cover Letter - Y-Intercept QR Intern", author="Jing Xiang Xu")
story = [
    Paragraph("<b>JING XIANG XU</b>", st["head"]),
    Paragraph("Hong Kong \u00b7 jx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108", st["meta"]),
    Paragraph(datetime.date(2026, 10, 3).strftime("%B %d, %Y"), st["meta"]),
    Spacer(1, 6),
]
for p in text.split("\n\n"):
    story.append(Paragraph(p.replace("\n", "<br/>"), st["body"]))
doc.build(story)

import pypdf
print("written:", out, "pages:", len(pypdf.PdfReader(out).pages))
