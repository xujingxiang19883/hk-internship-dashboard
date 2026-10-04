# -*- coding: utf-8 -*-
"""Tier-1 US QR/QT internship tracker - 9 firms, deadlines, application links."""
import sys, os
XLSX_SKILL_DIR = r"C:\Users\HUAWEI\.zcode\cli\plugins\cache\zcode-plugins-official\spreadsheets\0.1.7\skills\xlsx"
for sub in [XLSX_SKILL_DIR, os.path.join(XLSX_SKILL_DIR, "templates")]:
    if sub not in sys.path:
        sys.path.insert(0, sub)

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Data: firm, role, location, deadline, apply URL, CV file
ROWS = [
 ("TransMarket Group", "Quantitative Trader Intern (+ Algorithmic Trader Intern)", "Chicago, IL", "Rolling - apply now",
  "https://job-boards.greenhouse.io/transmarketgroup/jobs/5151569007?gh_jid=5151569007",
  "Xu_Jingxiang_TransMarket_CV.pdf"),
 ("Voloridge Investment Management", "Quantitative Research Intern 2027 (+ QR Fellowship 2027)", "Jupiter, FL", "Rolling - apply now",
  "https://job-boards.greenhouse.io/voloridgeinvestmentmanagement/jobs/4226247009?gh_jid=4226247009",
  "Xu_Jingxiang_Voloridge_CV.pdf"),
 ("BlackEdge Capital", "Quantitative Trader Intern (+ Quantitative Developer Intern)", "Chicago, IL", "Rolling - apply now",
  "https://job-boards.greenhouse.io/blackedgecapital/jobs/4703820005?gh_jid=4703820005",
  "Xu_Jingxiang_BlackEdge_CV.pdf"),
 ("Anthelion Capital", "Quant Developer / Quant Research Intern 2026/2027", "New York, NY", "Rolling - apply now",
  "https://jobs.ashbyhq.com/anthelioncap/5e2ea37b-2369-474e-b717-c24c60976e96",
  "Xu_Jingxiang_Anthelion_CV.pdf"),
 ("Stevens Capital Management", "Quantitative Research Analyst Internship", "Radnor, PA", "Rolling - apply now",
  "https://job-boards.greenhouse.io/scm/jobs/721895",
  "Xu_Jingxiang_Stevens_Capital_CV.pdf"),
 ("All Options International", "Quantitative Intern (+ Graduate QR / Graduate QT)", "Austin, TX", "Rolling - apply now",
  "https://www.alloptions-international.com/vacancies/quantitative-intern/",
  "Xu_Jingxiang_AllOptions_CV.pdf"),
 ("Group One Trading", "Trading Analyst Intern (~$30-35/hr)", "Chicago, IL", "Rolling - apply now",
  "https://group1.applicantpro.com/jobs/4192883",
  "Xu_Jingxiang_GroupOne_CV.pdf"),
 ("Kershner Trading Group", "Austin Trading Desk Internship - Summer 2027", "Austin, TX", "Rolling - apply now",
  "https://kershnertrading.applicantstack.com/x/detail/a24el03ed6qb",
  "Xu_Jingxiang_Kershner_CV.pdf"),
 ("PEAK6 Capital Management", "Trading Bootcamp Micro-Internship - Summer 2027 (1 week)", "Chicago, IL", "Rolling - apply now",
  "https://www.peak6.com/careers/",
  "Xu_Jingxiang_PEAK6_CV.pdf"),
 ("Virtu Financial", "2027 Internship - Quantitative Researcher (Undergrad), 10 weeks Jun 7-Aug 13", "New York, NY", "Open now",
  "https://job-boards.greenhouse.io/virtu/jobs/8142539002",
  "Xu_Jingxiang_Virtu_QR_CV.pdf"),
 ("Virtu Financial", "2027 Internship - Quantitative Trading", "Austin / Chicago / New York", "Open now",
  "https://job-boards.greenhouse.io/virtu/jobs/8624408002?gh_jid=8624408002",
  "Xu_Jingxiang_Virtu_QT_CV.pdf"),
]

NAVY = "1B2A4A"; LIGHT = "D6E4F0"; N100 = "F7F7F5"; N600 = "8C8A84"; N900 = "37352F"
WHITE = "FFFFFF"; ROSE = "C0392B"

wb = Workbook()
ws = wb.active
ws.title = "Tier-1 US QR-QT Internships"

# Title row
ws.merge_cells("A1:F1")
c = ws["A1"]
c.value = "US Summer 2027 QR / QT Internships - Tier-1+2 New Targets (11 firms) (Jing Xiang Xu) - compiled 2026-10-03"
c.font = Font(bold=True, size=13, color=NAVY)
c.alignment = Alignment(horizontal="left", vertical="center")
ws.row_dimensions[1].height = 24

# Header row
headers = ["#", "Company", "Role", "Location", "Deadline", "Application Link", "CV to Attach", "Status"]
HR = 3
for col, h in enumerate(headers, 1):
    cell = ws.cell(row=HR, column=col, value=h)
    cell.font = Font(bold=True, size=10, color=WHITE)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.alignment = Alignment(horizontal="left", vertical="center")

thin = Side(style="thin", color="D6E4F0")
for idx, (comp, role, loc, dl, url, cv) in enumerate(ROWS, 1):
    r = HR + idx
    fill = PatternFill("solid", fgColor=N100) if idx % 2 == 1 else None
    vals = [idx, comp, role, loc, dl, url, cv, "Not started"]
    for col, v in enumerate(vals, 1):
        cell = ws.cell(row=r, column=col, value=v)
        cell.font = Font(size=9.5, color=N900)
        cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=(col in (2, 3)))
        if fill: cell.fill = fill
    link_cell = ws.cell(row=r, column=6)
    link_cell.hyperlink = url
    link_cell.font = Font(size=9.5, color="0B6D8A", underline="single")
    # CV path note as comment-style text (file lives in D:\zcode\hk-dashboard\cv\)
    ws.cell(row=r, column=7).value = "D:\\zcode\\hk-dashboard\\cv\\" + cv
    ws.cell(row=r, column=7).font = Font(size=8.5, color=N600)
    st = ws.cell(row=r, column=8)
    st.font = Font(size=9.5, bold=True, color=ROSE)
    ws.row_dimensions[r].height = 30

# Column widths
widths = [4, 26, 42, 14, 18, 60, 44, 12]
for i, w in enumerate(widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = w

# Notes
note_r = HR + len(ROWS) + 2
notes = [
 "Notes:",
 "1. All 9 postings verified live on 2026-10-03 via quantroles.com hidden-gems audit (cross-checked against the 56-firm applied list - none duplicated).",
 "2. Deadlines are rolling - seats fill without notice (Deutsche Bank closed 3 weeks early). Apply in list order: QR-fit firms first (Voloridge, Anthelion, Stevens), then QT (TransMarket, BlackEdge, All Options, Group One, Kershner), then PEAK6 bootcamp.",
 "3. CVs are the in-place-tailored one-page PDFs in D:\\zcode\\hk-dashboard\\cv\\ (trading template for QT roles, quant-research template for QR roles).",
 "4. Jump / Tower / HRT excluded from this sheet - already self-applying (tracked in the main dashboard).",
"5. Tier-2 audit results: Virtu CONFIRMED (rows 10-11). Trexquant QR intern on LinkedIn (actively hiring, no public apply link - search Trexquant on LinkedIn). Balyasny/Headlands: QR internships exist but 2027 cycle unconfirmed or PhD-only. GSA: QR intern is London-only (NY is full-time). Teza: no intern role on Ashby board (QR All Streams is full-time). Wolverine: no intern postings live on wolve.com. Vatic/Selini: no intern roles. Wintermute: grad algo trader London only. Old Mission: QT 2027 Graduate full-time only. PDT/Voleon/Radix/CTC/Pinely/Qube-US: no public intern postings (Qube has QR&T intern in SINGAPORE).",
]
for i, n in enumerate(notes):
    cell = ws.cell(row=note_r + i, column=1, value=n)
    cell.font = Font(size=9, color=N600 if i else N900, bold=(i == 0))
    ws.merge_cells(start_row=note_r + i, start_column=1, end_row=note_r + i, end_column=8)

ws.freeze_panes = "A4"
wb.properties.creator = "Z.ai"
out = r"D:\zcode\hk-dashboard\Tier1_US_QR_QT_Internships.xlsx"
wb.save(out)
print("saved:", out)
