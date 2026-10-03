# -*- coding: utf-8 -*-
"""Flow Traders HK Trading Intern cover letter - tailored to JD 8102618."""
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
"Dear Flow Traders APAC Recruitment Team,\n\n"
"I am applying for the Trading Intern position on the Hong Kong APAC trading floor (June" + "\u2013" + "July 2027 intake). I am a "
"Master of Engineering student in Financial Engineering at Cornell (graduating December 2027) with a First Class Honours BSc in "
"Mathematics from the University of Hong Kong " + "\u2014" + " an APAC degree, as your posting specifies " + "\u2014" + " and I hold an IANG visa "
"with unrestricted right to work in Hong Kong, so no sponsorship is needed.\n\n"
"The posting asks for competitive, innovative people with strong mental arithmetic who can spot opportunities and act on them. "
"That describes how I already operate. With HKU's quant trading team I ran a live Polymarket book: scanning order books, ranking "
"opportunities by expected value, enforcing position limits, and tracking realized P&amp;L against systematic mispricings above three "
"percentage points " + "\u2014" + " trading decisions made quickly, under real money pressure. At Dymon Asia Capital in Hong Kong I predicted Hang "
"Seng index constituent changes before official announcements (an 82.6% action-level hit rate across three live rebalances) by building "
"quantitative models over FactSet, ERD and HKEX filings in Python. Poker and F1 racing " + "\u2014" + " on my resume because they are true " + "\u2014" + " keep my "
"probability intuition and competitive edge sharp.\n\n"
"Flow Traders attracts me specifically: a leading global market maker where interns build trading strategies through quantitative "
"modelling, tackle real problems alongside traders and researchers, and join a One Team culture that trains rather than screens. "
"I am available for the full six weeks from June 2027, can start immediately after my spring semester ends in May, and would be "
"delighted to bring an APAC-educated, market-microstructure-minded profile to your floor.\n\n"
"Sincerely,\nJing Xiang Xu\njx466@cornell.edu \u00b7 +852 6810 9521 (HK) / +1 607-882-5108"
)

out = r"D:\zcode\hk-dashboard\cover-letters\Xu_Jingxiang_Flow_Traders_Cover_Letter.pdf"
doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=16*mm, bottomMargin=14*mm,
                        title="Cover Letter - Flow Traders Trading Intern HK 2027", author="Jing Xiang Xu")
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
