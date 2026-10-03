# -*- coding: utf-8 -*-
"""In-place resume tailor: keeps the original PDF's format/structure/fonts exactly,
only (1) rewrites bullet text per target role, (2) adds the HK phone to the contact line.
Every output is exactly 1 page (the original is 1 page and line counts are preserved)."""
import fitz, os, json

SRC = r"C:\Users\HUAWEI\Desktop\Xu_Jingxiang_Resume Book.pdf"
OUT_DIR = r"D:\zcode\hk-dashboard\cv"
TEXT_FONT_SIZE = 10.1
BULLET_X = 48.9
RIGHT_EDGE = 578.5
BLACK = (0, 0, 0)

doc0 = fitz.open(SRC)
page0 = doc0[0]

# ---------- collect spans (with origins), grouped by LINE bbox y ----------
spans = []
lines_by_y = {}
d = page0.get_text("dict")
for b in d["blocks"]:
    if b.get("type") != 0:
        continue
    for l in b["lines"]:
        y = round(l["bbox"][1], 1)
        bucket = lines_by_y.setdefault(y, [])
        for s in l["spans"]:
            spans.append({
                "text": s["text"], "bbox": s["bbox"], "origin": s["origin"],
                "size": s["size"], "font": s["font"],
            })
            bucket.append(s)
page_fonts = page0.get_fonts()
tnr_xref = None
for f in page_fonts:
    if "TimesNewRomanPSMT" in f[3]:
        tnr_xref = f[0]
font = None
if tnr_xref:
    name, ext, _, buf = doc0.extract_font(tnr_xref)
    if buf:
        try:
            cand = fitz.Font(fontbuffer=buf)
            if all(cand.has_glyph(ord(ch)) for ch in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,;:%()/+-&' "):
                font = cand
        except Exception:
            pass
if font is None:
    font = fitz.Font("tiro")
print("font in use:", font.name)

def tlen(s):
    return font.text_length(s, fontsize=TEXT_FONT_SIZE)

# ---------- locate bullet blocks ----------
BULLET_FIRST_YS = [295.1, 331.4, 355.6, 394.0, 418.5, 442.7, 479.0, 491.5, 504.2, 528.4, 541.1, 596.3, 632.6, 671.0, 695.2]
ALL_YS = sorted(lines_by_y.keys())

def text_span(y):
    # the Times text span of a bullet body line (x ~= 48.9), not the Symbol glyph
    cands = [s for s in lines_by_y[y] if s["bbox"][0] >= 46.5]
    cands.sort(key=lambda s: s["bbox"][0])
    return cands[0] if cands else None

def block_lines(first_y):
    out = [first_y]
    y = first_y
    while True:
        # next line = nearest following y within 9..15pt
        nxt = None
        for yy in ALL_YS:
            if 9.0 < yy - y < 15.0:
                nxt = yy
                break
            if yy - y >= 15.0:
                break
        if nxt is None:
            break
        spans_here = lines_by_y[nxt]
        has_symbol = any("Symbol" in s["font"] for s in spans_here)
        s0 = sorted(spans_here, key=lambda s: s["bbox"][0])[0]
        # continuation: no bullet glyph, starts at text x (~48.9), Times font
        if has_symbol or s0["bbox"][0] < 46.5 or "Times" not in s0["font"]:
            break
        out.append(nxt)
        y = nxt
    return out

BLOCKS = {}  # key -> list of line ys
keys = ["dymon1","dymon2","dymon3","river1","river2","river3","nine1","nine2","nine3","ne1","ne2","hku1","hku2","oxf1","oxf2"]
for k, fy in zip(keys, BULLET_FIRST_YS):
    BLOCKS[k] = block_lines(fy)
print(json.dumps({k: v for k, v in BLOCKS.items()}))

# ---------- contact line phone span ----------
phone_span = next(s for s in spans if "cell:" in s["text"])

# ---------- bullet text variants ----------
# each string must fit (len(lines) <= block lines, width <= RIGHT_EDGE-BULLET_X)
V = {
# ---- QUANT RESEARCH (funds) ----
"quant": {
 "dymon1": "Researched Hang Seng Composite and Tech Index rebalancing rules to predict constituent inclusions and exclusions ahead of official announcements, converting published methodologies into point-in-time eligibility, liquidity and buffer-selection logic built only on public data.",
 "dymon2": "Designed an auditable, fully reproducible Python research pipeline integrating FactSet, ERD and HKEX filings, including LLM-assisted screening gates and a filing-driven free-float engine, so every signal input can be traced to its source.",
 "dymon3": "Achieved an 82.6% action-level hit rate (185 of 224 additions and deletions) across the latest three HSCI rebalances in leakage-controlled, point-in-time evaluation, with no licensed index feed.",
 "river1": "Automated thematic stock selection by mapping unstructured investment themes onto supply-chain dimensions and a proprietary sector taxonomy, turning qualitative theses into testable, auditable universes.",
 "river2": "Built a Python/Pandas pipeline integrating sector, revenue-segment and company-description data, generating auditable intermediate outputs and segment-level relevance diagnostics for every screen.",
 "river3": "Designed a two-stage semantic retrieval pipeline (BGE embeddings with cosine similarity, then LLM-based refinement) for candidate generation and ambiguous theme resolution.",
 "nine1":  "Identified a 60-day dividend-event data lag and corrected factor alignment, raising information coefficient by 0.02.",
 "nine2":  "Built a factor-backtesting framework; improved annualized return by 6% and Sharpe ratio by 0.3 over five years.",
 "nine3":  "Analyzed daily exposures to 10 Barra style factors to characterize signal crowding, decay and style tilts.",
 "ne1":    "Developed mean-variance and risk-parity models within a 15-year daily-rebalanced backtesting framework.",
 "ne2":    "Implemented a Monte Carlo method approximating ERC weights by minimizing asset risk-contribution gaps.",
 "hku1":   "Analyzed historical Polymarket data for systematic price-versus-outcome gaps, grouping contracts by topic, market structure and time to resolution, and flagging Yes/No shares with pricing gaps above 3 percentage points.",
 "hku2":   "Built a Python pipeline that scanned live markets, ranked opportunities by expected value, enforced position limits, submitted orders through the order book, and tracked realized P&L.",
 "oxf1":   "Modeled Lightning Network channel management as a discounted MDP, deriving optimal routing, liquidity-reset and channel-capacity policies under stochastic payment flows.",
 "oxf2":   "Implemented value iteration for discrete and exponential payment distributions, proving bidirectional flows can naturally rebalance liquidity and remove costly resets.",
},
# ---- TRADING / PROP ----
"trading": {
 "dymon1": "Researched Hang Seng Composite and Tech Index rebalancing rules to anticipate constituent additions and exclusions before official announcements, modeling the predictable index-driven flows they create via point-in-time eligibility and buffer rules.",
 "dymon2": "Designed an auditable Python pipeline integrating FactSet, ERD and HKEX filings with LLM-assisted screening gates, hard-coding selection rules into repeatable, deadline-critical production logic.",
 "dymon3": "Achieved an 82.6% action-level hit rate (185 of 224 additions and deletions) across three live rebalances in leakage-controlled evaluation, monetizable ahead of reconstitution dates.",
 "river1": "Automated thematic stock selection by translating unstructured investment themes into supply-chain dimensions mapped to a proprietary taxonomy, expanding the tradeable universe per theme.",
 "river2": "Built a Python/Pandas pipeline integrating sector, revenue-segment and company-description data with relevance diagnostics for rapid idea iteration.",
 "river3": "Designed a two-stage semantic retrieval pipeline (BGE embeddings plus LLM refinement) for fast, ambiguous-theme candidate generation.",
 "nine1":  "Identified a 60-day dividend-event data lag and corrected factor timing, raising information coefficient by 0.02.",
 "nine2":  "Built a factor-backtesting framework; improved annualized return by 6% and Sharpe ratio by 0.3 over five years.",
 "nine3":  "Analyzed daily exposures to 10 Barra style factors to manage signal crowding and unwanted style risk.",
 "ne1":    "Developed mean-variance and risk-parity models within a 15-year daily-rebalanced backtesting framework.",
 "ne2":    "Implemented a Monte Carlo method approximating ERC weights by minimizing asset risk-contribution gaps.",
 "hku1":   "Analyzed historical Polymarket data for systematic mispricings between market prices and realized outcomes, grouping contracts by topic, structure and time to resolution; flagged Yes/No shares with edges above 3 percentage points and refreshed estimates monthly.",
 "hku2":   "Built a Python pipeline that scanned live order books, ranked opportunities by expected value, enforced position limits, simulated or submitted orders, and tracked realized P&L.",
 "oxf1":   "Modeled Lightning Network channel management as a discounted MDP, deriving optimal routing, liquidity-reset and capacity policies under stochastic payment flows.",
 "oxf2":   "Implemented value iteration for discrete and exponential payment distributions, showing bidirectional flows naturally rebalance liquidity and remove costly resets.",
},
# ---- BANK STRATS / PRICING & RISK ----
"bank": {
 "dymon1": "Researched Hang Seng Composite and Tech Index rebalancing rules to predict constituent inclusions and exclusions before official announcements, translating published methodologies into point-in-time eligibility, liquidity and buffer-selection logic validated against outcomes.",
 "dymon2": "Designed an auditable, object-oriented Python pipeline (pandas/NumPy) integrating FactSet, ERD and HKEX filings, with LLM-assisted gates and a filing-based free-float engine mapping shareholder evidence to the ten HSIL categories.",
 "dymon3": "Achieved an 82.6% action-level hit rate (185 of 224 additions and deletions) across three rebalances in leakage-controlled, point-in-time evaluation, demonstrating rigorous model validation practice.",
 "river1": "Automated thematic stock selection by translating unstructured investment themes into supply-chain dimensions and a proprietary sector taxonomy with full auditability.",
 "river2": "Built a Python/Pandas pipeline integrating sector, revenue-segment and company-description data with auditable intermediate outputs and diagnostics.",
 "river3": "Designed a two-stage semantic retrieval pipeline (BGE embeddings, then LLM refinement) applying machine learning to classification and reranking problems.",
 "nine1":  "Identified a 60-day dividend-event data lag and corrected factor alignment, raising information coefficient by 0.02.",
 "nine2":  "Built a factor-backtesting framework; improved annualized return by 6% and Sharpe ratio by 0.3 over five years.",
 "nine3":  "Analyzed daily exposures to 10 Barra style factors to quantify risk and style tilts.",
 "ne1":    "Developed mean-variance and risk-parity models within a 15-year daily-rebalanced backtesting framework.",
 "ne2":    "Implemented a Monte Carlo method approximating ERC weights by minimizing risk-contribution gaps.",
 "hku1":   "Analyzed historical Polymarket data for systematic price-versus-outcome gaps, grouping contracts by topic, market structure and time to resolution; identified Yes/No shares with pricing gaps above 3 percentage points.",
 "hku2":   "Built a Python pipeline that scanned live markets, ranked opportunities, enforced position limits, submitted orders via the exchange order book, and tracked realized P&L.",
 "oxf1":   "Modeled Lightning Network channel management as a discounted MDP, deriving optimal routing, liquidity-reset and channel-capacity policies under stochastic flows.",
 "oxf2":   "Implemented value iteration for discrete and exponential payment distributions, demonstrating how bidirectional flows naturally rebalance liquidity and eliminate costly resets.",
},
# ---- ASSET MANAGEMENT / INVESTMENT RESEARCH ----
"am": {
 "dymon1": "Researched Hang Seng Composite and Tech Index rebalancing rules to predict constituent inclusions and exclusions before official announcements, converting index methodologies into point-in-time eligibility, liquidity and buffer-selection logic.",
 "dymon2": "Designed an auditable Python pipeline integrating FactSet, ERD and HKEX filings, including LLM-assisted screening gates and a filing-based free-float engine, ensuring every output is explainable to portfolio managers.",
 "dymon3": "Achieved an 82.6% action-level hit rate (185 of 224 additions and deletions) across the latest three HSCI rebalances in leakage-controlled, point-in-time evaluation.",
 "river1": "Automated thematic stock selection by translating unstructured investment themes into supply-chain dimensions mapped to a proprietary sector taxonomy for research coverage.",
 "river2": "Built a Python/Pandas pipeline integrating sector, revenue-segment and company-description data with segment-level relevance diagnostics.",
 "river3": "Designed a two-stage semantic retrieval pipeline (BGE embeddings plus cosine similarity, then LLM refinement) for theme classification and ambiguous queries.",
 "nine1":  "Identified a 60-day dividend-event data lag and corrected factor alignment, raising information coefficient by 0.02.",
 "nine2":  "Built a factor-backtesting framework; improved annualized return by 6% and Sharpe ratio by 0.3 over five years.",
 "nine3":  "Analyzed daily exposures to 10 Barra style factors to identify signal characteristics and style tilts for portfolio construction.",
 "ne1":    "Developed mean-variance and risk-parity models within a 15-year daily-rebalanced backtesting framework.",
 "ne2":    "Implemented a Monte Carlo method approximating ERC weights by minimizing asset risk-contribution gaps.",
 "hku1":   "Analyzed historical Polymarket data for systematic price-versus-outcome differences, grouping contracts by topic, market structure and time to resolution; flagged Yes/No shares with pricing gaps above 3 percentage points.",
 "hku2":   "Built a Python pipeline that scanned live markets, ranked opportunities, enforced position limits, and tracked resolved trades and realized P&L.",
 "oxf1":   "Modeled Lightning Network channel management as a discounted MDP, deriving optimal on-chain/off-chain routing, liquidity-reset and channel-capacity policies under stochastic payment flows.",
 "oxf2":   "Implemented value iteration for discrete and exponential payment distributions, demonstrating that bidirectional flows can naturally rebalance liquidity.",
},
}

# per-company overrides keyed (block) for targeted JD alignment
SPECIALS = {
 "Bank_of_America_GQS": {"dymon2": "Designed an auditable, object-oriented Python pipeline (pandas/NumPy) integrating FactSet, ERD and HKEX filings, with AI/LLM-assisted screening gates and a filing-based free-float engine mapping shareholder evidence to the ten HSIL categories."},
 "JPMorgan_MarketsQR": {"oxf1": "Modeled Lightning Network channel management as a discounted MDP under stochastic payment flows, applying probability theory, dynamic programming and numerical methods to derive optimal routing and liquidity policies."},
 "Point72":       {"dymon1": "Researched Hang Seng Composite and Tech Index rebalancing rules to predict constituent inclusions and exclusions before official announcements \u2014 a repeatable, thesis-driven edge built from public filings and rulebook analysis."},
}

CONFIG = [    ("Flow_Traders","trading"), ("Squarepoint","quant"),
 ("WorldQuant","quant"), ("Ubiquant","quant"), ("High_Flyer","quant"), ("Minghong","quant"),
 ("Lingjun","quant"), ("Wizard_Quant","quant"), ("Dymon_Asia","quant"),
 ("Jump_Trading","trading"), ("Tower_Research","trading"), ("HRT","trading"),
 ("Bank_of_America_GQS","bank"), ("Bank_of_America_Markets","trading"),  ("Goldman_Sachs_Strats","bank"),
 ("JPMorgan_MarketsQR","trading"), 
 ("Citi","bank"), ("Jefferies_Macquarie","bank"),  ("Point72","quant"),
    
]

PHONE_TEXT = "+852 6810 9521 / 607-882-5108"

def wrap(text, maxw, maxlines):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if tlen(trial) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if len(lines) > maxlines:  # word-safe fallback: drop trailing words, never cut mid-word
        while len(lines) > maxlines:
            lines.pop()
        while lines and tlen(lines[-1] + " x") > maxw and " " in lines[-1]:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] = lines[-1].rstrip(" ,;:") + "."
        print("  [warn] shortened to fit:", lines[-1][-50:])
    return lines

def build(slug, variant):
    over = SPECIALS.get(slug, {})
    bullets = dict(V[variant])
    bullets.update(over)
    nd = fitz.open(SRC)
    pg = nd[0]
    # 1) phone: redact original phone span, insert new right-aligned
    r = fitz.Rect(phone_span["bbox"][0] - 1, phone_span["bbox"][1] - 1, phone_span["bbox"][2] + 1, phone_span["bbox"][3] + 1)
    pg.add_redact_annot(r)
    # 2) bullets: redact text portion only (keep the Symbol bullet glyph at x=40.3)
    for k, ys in BLOCKS.items():
        for y in ys:
            sp = text_span(y)
            if sp is None:
                continue
            x1 = max(s["bbox"][2] for s in lines_by_y[y])
            rr = fitz.Rect(BULLET_X - 1, sp["bbox"][1] - 1.5, x1 + 1, sp["bbox"][3] + 1.5)
            pg.add_redact_annot(rr)
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    # 3) insert phone (right-aligned to original right edge, same baseline)
    tw = fitz.TextWriter(pg.rect, color=BLACK)
    px = phone_span["origin"][0]
    px = min(px, RIGHT_EDGE - tlen(PHONE_TEXT))
    tw.append(fitz.Point(px, phone_span["origin"][1]), PHONE_TEXT, font=font, fontsize=TEXT_FONT_SIZE)
    # 4) insert bullets
    for k, ys in BLOCKS.items():
        maxlines = len(ys)
        newlines = wrap(bullets[k], RIGHT_EDGE - BULLET_X - 2, maxlines)
        for i, y in enumerate(ys):
            if i < len(newlines):
                tw.append(fitz.Point(BULLET_X, text_span(y)["origin"][1]), newlines[i], font=font, fontsize=TEXT_FONT_SIZE)
    tw.write_text(pg, color=BLACK)
    out = os.path.join(OUT_DIR, "Xu_Jingxiang_%s_CV.pdf" % slug)
    nd.save(out, garbage=3, deflate=True)
    nd.close()
    return out

os.makedirs(OUT_DIR, exist_ok=True)
for slug, variant in CONFIG:
    out = build(slug, variant)
    check = fitz.open(out)
    assert len(check) == 1, out
    check.close()
print("generated", len(CONFIG), "one-page CVs (in-place edits of the original)")
