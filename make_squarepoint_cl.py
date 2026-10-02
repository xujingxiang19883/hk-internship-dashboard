# -*- coding: utf-8 -*-
"""Squarepoint cover letter - references the April 2026 exchange, NY preferred + HK secondary."""
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
"Dear Squarepoint Recruiting Team,\n\n"
"I am applying for the Intern Quant Researcher position (Summer 2027), with New York as my preferred office and Hong Kong and "
"Singapore as strong secondary preferences. I am currently a Master of Engineering student in Financial Engineering at Cornell "
"(graduating December 2027), and I completed my BSc in Mathematics with First Class Honours at the University of Hong Kong this June. "
"My connection to Squarepoint is not new: in April 2026 I was invited by Nicole Liew to interview for the Desk Quant Analyst role, "
"and I withdrew only because my Cornell offer arrived on a conflicting timeline \u2014 with the express hope of returning once my "
"Master\u2019s was underway. This internship is exactly that return, at exactly the stage your team suggested.\n\n"
"My research experience maps directly onto the role. At Dymon Asia Capital in Hong Kong I predicted Hang Seng Composite and Tech "
"Index constituent changes before official announcements \u2014 an 82.6% action-level hit rate (185/224) across three live rebalances \u2014 "
"by translating published index methodologies into point-in-time eligibility, liquidity and buffer logic inside an auditable Python "
"pipeline over FactSet, ERD and HKEX filings, with LLM-assisted screening gates. At Rivermap I automated thematic stock selection with "
"a two-stage semantic retrieval system (BGE embeddings, then LLM refinement). With HKU\u2019s quant trading team I ran a live Polymarket "
"book: scanning order books, ranking opportunities by expected value, enforcing position limits, and tracking realized P&L against "
"systematic mispricings above three percentage points.\n\n"
"The role\u2019s core \u2014 researching and implementing trading ideas inside an automated framework, analyzing large datasets, and "
"understanding exchange microstructure \u2014 is a precise description of how I already work, and Squarepoint\u2019s multi-office platform "
"is where I want to build my career. I am available for interviews at any time and can start in June 2027.\n\n"
"Sincerely,\nJing Xiang Xu\njx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108"
)

out = r"D:\zcode\hk-dashboard\cover-letters\Xu_Jingxiang_Squarepoint_Cover_Letter.pdf"
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=16*mm, bottomMargin=14*mm,
                        title="Cover Letter - Squarepoint Intern Quant Researcher 2027", author="Jing Xiang Xu")
story = [
    Paragraph("<b>JING XIANG XU</b>", st["head"]),
    Paragraph("Hong Kong \u00b7 jx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108", st["meta"]),
    Paragraph(datetime.date(2026, 10, 2).strftime("%B %d, %Y"), st["meta"]),
    Spacer(1, 6),
]
for p in text.split("\n\n"):
    story.append(Paragraph(p.replace("\n", "<br/>"), st["body"]))
doc.build(story)

import pypdf
print("written:", out, "pages:", len(pypdf.PdfReader(out).pages))
