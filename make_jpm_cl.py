# -*- coding: utf-8 -*-
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
"Dear J.P. Morgan Recruiting Team,\n\n"
"I am writing to apply for the 2027 Commercial & Investment Bank Markets Summer Analyst Program in Hong Kong. I am a Master of Engineering student in Financial Engineering at Cornell (graduating December 2027) with a First Class Honours BSc in Mathematics and a Computer Science minor from the University of Hong Kong \u2014 this is my penultimate summer, and Hong Kong is my home base on an IANG visa with unrestricted work rights.\n\n"
"Markets are where my record is most concrete. At Dymon Asia Capital in Hong Kong I predicted Hang Seng Composite and Tech Index constituent changes before official announcements, achieving an 82.6% action-level hit rate (185/224 additions and deletions) across three live rebalances with an auditable, point-in-time Python pipeline over FactSet, ERD and HKEX filings. At Rivermap I automated thematic stock selection with a two-stage semantic retrieval system. With the HKU Quant Trading Team I ran a live Polymarket book \u2014 scanning order books, enforcing position limits, submitting orders and tracking realized P&L. Earlier roles at Nine Martingale and Northeast Securities added factor backtesting (IC +0.02 after fixing a dividend-event data lag; +6% annualized return, +0.3 Sharpe) and Monte Carlo risk-parity modeling.\n\n"
"I fit the program profile directly: strong quantitative and probability skills, native Mandarin for the desks covering Chinese markets, and fluency in English. I would welcome the chance to contribute to the Hong Kong Markets desk and am available for interviews in North America this fall or virtually at any time.\n\n"
"Sincerely,\nJing Xiang Xu\njx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108"
)

out = r"D:\zcode\hk-dashboard\cover-letters\Xu_Jingxiang_JPMorgan_Markets_Cover_Letter.pdf"
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=16*mm, bottomMargin=14*mm,
                        title="Cover Letter - JPM Markets Summer Analyst 2027", author="Jing Xiang Xu")
story = [
    Paragraph("<b>JING XIANG XU</b>", st["head"]),
    Paragraph("Hong Kong \u00b7 jx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108", st["meta"]),
    Paragraph(datetime.date(2026, 9, 26).strftime("%B %d, %Y"), st["meta"]),
    Spacer(1, 6),
]
for p in text.split("\n\n"):
    story.append(Paragraph(p.replace("\n", "<br/>"), st["body"]))
doc.build(story)

import pypdf
print("written:", out, "pages:", len(pypdf.PdfReader(out).pages))
