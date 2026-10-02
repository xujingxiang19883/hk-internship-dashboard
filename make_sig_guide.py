# -*- coding: utf-8 -*-
"""SIG interview prep guide - A4, Times, navy/aqua palette to match the dashboard."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
                                KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

try:
    pdfmetrics.registerFont(TTFont("Sans", r"C:\Windows\Fonts\arial.ttf"))
    F = "Sans"
except Exception:
    F = "Helvetica"

NAVY = "#12233c"; AQUA = "#0d8f82"; MUTED = "#4d5c72"; ROSE = "#b53f4d"

S = {
 "title": ParagraphStyle("t", fontName=F, fontSize=20, leading=24, textColor=NAVY, alignment=TA_CENTER, spaceAfter=2),
 "sub":   ParagraphStyle("s", fontName=F, fontSize=9.5, leading=12, textColor=MUTED, alignment=TA_CENTER, spaceAfter=8),
 "h1":    ParagraphStyle("h1", fontName=F, fontSize=12.5, leading=15, textColor=NAVY, spaceBefore=10, spaceAfter=2),
 "h2":    ParagraphStyle("h2", fontName=F, fontSize=10.3, leading=13, textColor=NAVY, spaceBefore=6, spaceAfter=1),
 "body":  ParagraphStyle("b", fontName=F, fontSize=9.2, leading=12.4, spaceAfter=3),
 "ans":   ParagraphStyle("a", fontName=F, fontSize=9.0, leading=12.2, leftIndent=10, spaceAfter=3, textColor="#26364f"),
 "q":     ParagraphStyle("q", fontName=F, fontSize=9.4, leading=12.4, spaceBefore=4, spaceAfter=2),
 "tip":   ParagraphStyle("tp", fontName=F, fontSize=9.0, leading=12, leftIndent=8, spaceAfter=2, textColor=MUTED),
}

def hr():
    return HRFlowable(width="100%", thickness=0.8, color="#c9d4e0", spaceAfter=4)

def h1(t):
    return [Paragraph("<font color='#0d8f82'><b>" + t.upper() + "</b></font>", S["h1"]), hr()]

def qa(num, q, a_lines, take=None):
    items = [Paragraph("<b>Q" + str(num) + ".</b> " + q, S["q"])]
    for line in a_lines:
        items.append(Paragraph("<b>Answer:</b> " + line if line is a_lines[0] else line, S["ans"]))
    if take:
        items.append(Paragraph("<i>Takeaway:</i> " + take, S["tip"]))
    return KeepTogether(items)

story = []
story += h1("SIG Quant Interview - Prep Sheet (Jing Xiang Xu)")
story.append(Paragraph("For the October 8 interview (Quantitative Research + Quantitative Systematic Trading). "
    "SIG's style: fast probability and expected value, mental math under time pressure, game theory and market-making scenarios, "
    "and probing whether you can explain your reasoning cleanly. Polish your two stories (Polymarket book; Hang Seng index prediction) "
    "and practice the math below out loud, to a timer.", S["sub"]))

story += h1("1. Core Probability & Expected Value (the bread and butter)")
story += [qa(1, "Two players alternate flipping a fair coin; the first to flip Heads wins. What is the probability the first player wins?",
    ["First player wins on flips 1, 3, 5, ...: P = 1/2 + 1/8 + 1/32 + ... = (1/2)/(1 - 1/4) = <b>2/3</b>.",
     "Fast method: first player wins with probability p where p = 1/2 + (1/4)p, so p = 2/3."],
    "Recognize geometric series or set up a self-referential equation; both take under 30 seconds.")]
story += [qa(2, "You roll a die until a 6 appears. What is the expected number of rolls, and the expected number of rolls that show an even number?",
    ["Geometric with p = 1/6: E[rolls] = <b>6</b>.",
     "Every roll is even with probability 1/2 regardless of length; by Wald's identity E[even rolls] = E[N] x P(even per roll) = 6 x 1/2 = <b>3</b>."],
    "Wald's equation shortcuts many 'expected count' questions - say the word 'Wald' to show structure.")]
story += [qa(3, "I offer you a game: pay 10, roll a die, I pay you the square of the outcome. Do you play?",
    ["E[outcome squared] = (1+4+9+16+25+36)/6 = 91/6 = 15.17 &gt; 10, so <b>yes</b>, EV = +5.17 per roll.",
     "Follow-up they will ask: 'now I pay you the square of (outcome - 3)'. Variance view: E[(X-3)^2] = Var(X) + (E[X]-3)^2 = 35/12 + 0.25 = 3.17. Now you should decline if the price is 10."],
    "Always decompose: E[f(X)] is not f(E[X]). Quote variance where relevant.")]
story += [qa(4, "A jar has 50 red and 50 blue balls. Move balls between two jars to maximize P(red when drawing uniformly from a random jar).",
    ["Put 1 red ball alone in jar A, the remaining 49 red + 50 blue in jar B.",
     "P = (1/2)(1) + (1/2)(49/99) = 1/2 + 49/198 = <b>148/198 = 74/99 = 0.7475</b>."],
    "Extremize at the boundary: make one jar as red as possible.")]
story += [qa(5, "You have a biased coin with P(H) = p but you don't know p. How do you generate a fair coin flip?",
    ["Von Neumann scheme: flip pairs until they differ (HT or TH); call HT = H, TH = T. Each differing pair is fair by symmetry.",
     "Expected pairs needed: 1/(2p(1-p)) &lt;= 2."],
    "Classic 'reduction to symmetry' - works for any unknown bias.")]

story += h1("2. Expected Value with Decisions (the SIG signature)")
story += [qa(6, "You may roll a die up to three times; after each roll take the value or reroll (last roll is forced). What is the fair value of the game and your optimal strategy?",
    ["V1 = 3.5. With two rolls left: stop if roll &gt; 3.5, so V2 = (4+5+6)/6 x avg(4,5,6) + (3/6) x 3.5 = (15/6)(5)/... compute directly: V2 = (1/6)(4+5+6) + (1/2)(3.5) = 2.5 + 1.75 = 4.25.",
     "With three: V3 = (1/6)(5+6) + (2/3) x V2... precisely: stop if roll &gt; V2 = 4.25, i.e. on 5 or 6: V3 = (1/6)(5 + 6) + (4/6)(4.25) = 11/6 + 17/6 = <b>4.667</b>.",
     "Strategy: keep 5 or 6 on roll one, keep 4+ on roll two."],
    "Solve backwards (dynamic programming). State the cutoff at each stage before computing.")]
story += [qa(7, "Five ants sit on a 1-meter plank facing left or right at random, walk at 1 m/s, and reverse direction when they collide. How long until all are off?",
    ["Equivalent (relabeling) to ants passing through each other: max time = 1 m / 1 m/s = <b>1 second</b>."],
    "Symmetry/relabeling tricks turn collisions into non-events - look for them constantly.")]
story += [qa(8, "You flip 100 fair coins. Those showing H pay you $1; then you may reflip all T coins once (all T together). Fair value?",
    ["Let k = number of heads. After the single reflip of the rest, total = 100/2 + E[Bin(100 - k, 1/2) | k]... unconditional: each coin ends H with probability 1/2 + (1/2)(1/2) = 3/4, so EV = <b>75</b>."],
    "Linearity of expectation over independent coins beats conditioning on k.")]
story += [qa(9, "St. Petersburg game: flip until H, paid 2^n. What is the fair price? What would you actually pay?",
    ["E = sum (1/2^n)(2^n) = infinity, but utility/log-wealth or bankroll constraints give realistic values: with log utility the certainty equivalent is a small finite number (per-coin toss analysis gives ~$2-10 range depending on assumptions).",
     "SIG wants: state the math, then say 'in practice my counterparty's credit and my bankroll cap it near a few dollars'."],
    "Never just say 'infinite' - discuss practical constraints; they test judgment, not recall.")]
story += [qa(10, "Deal 5 cards. What is the probability of exactly one pair?",
    ["C(13,1) x C(4,2) x C(12,3) x 4^3 / C(52,5) = (13 x 6 x 220 x 64) / 2,598,960 = 1,098,240/2,598,960 = <b>42.26%</b>.",
     "Structure: rank for the pair, 3 distinct other ranks, suits."],
    "Know C(52,5) = 2,598,960 by heart; count patterns methodically.")]

story += h1("3. Mental Math & Speed (warm up daily, timed)")
story += [qa(11, "Drill list (target: 10-15 seconds each, out loud).",
    ["17 x 23; 24 x 25; 7.5% of 240; 61 squared; 1/17 to 4 decimals; 2^15; C(10,3).",
     "Answers: 391; 600; 18; 3721; 0.0588; 32,768; 120.",
     "Tricks: 17x23 = (20-3)(20+3) = 400-9; x25 = x100/4; a% of b = b% of a; squares via (a+b)^2."],
    "SIG interviews include rapid-fire arithmetic; accuracy at speed beats slow perfection.")]
story += [qa(12, "Estimation (Fermi) example: How many tennis balls fit in this room?",
    ["Volume ratio with packing factor ~64%: room 4x5x3 m = 60 m^3; ball d = 6.7cm, V = 1.57e-4 m^3; count = 60 x 0.64 / 1.57e-4 = ~245,000.",
     "State assumptions before arithmetic; round aggressively; sanity-check the order of magnitude."],
    "They grade your estimation process and confidence, not the last digit.")]

story += h1("4. Games, Market-Making & Behavioral Scenarios")
story += [qa(13, "Market-making: 'Make me a market on the number of windows in this building.'",
    ["Give a two-way quote with width: '35 - 55'. If pressed tighter: '42 - 48'. If they trade, update your belief: they buy at 55 only if they know something - shade up to '55 - 75'.",
     "Never quote a point value; always show the bid-ask and explain the information update after a trade."],
    "This tests Bayesian updating under adverse selection. Practice saying quotes out loud with conviction.")]
story += [qa(14, "Guess 2/3 of the average of all guesses (0-100). What do you submit?",
    ["Iterated dominance: 0 is the Nash equilibrium, but real humans play ~20-35. Against a mixed group submit <b>~18-22</b>; against quant-savvy competitors submit lower (10-15).",
     "Say: 'equilibrium is 0, but I'm playing against people, so I expect one or two levels of reasoning, not infinite.'"],
    "SIG loves p-beauty-contest questions; calibrating to the population IS the skill.")]
story += [qa(15, "Poker (they know you play): you hold a flush draw on the flop, pot 100, villain bets 50. Call?",
    ["9 outs twice: ~36% equity by the river (rule of 4). Need 50/(100+50+50) = 25% breakeven with implied odds - <b>clear call</b>.",
     "Connect it to your Polymarket edge: 'pricing gaps above 3 points' is the same idea - EV per unit risked vs price."],
    "Expect one poker/probability-in-games question since it's on your resume; have numbers, not vibes.")]
story += [qa(16, "You and a rival simultaneously choose a number 1-5; higher number wins $10 from the other unless the difference is 1, in which case the lower number wins. What do you play?",
    ["Mixed-strategy game; pure strategies lose to counters (2 beats 1 and 5 is beaten by 4...). Equilibrium mixes over several numbers with no dominant pure play.",
     "If pressed for a heuristic: 2 and 3 carry most weight (they beat the aggressive high numbers on the difference-1 rule)."],
    "Acknowledge it's a mixed-strategy equilibrium; walk through why pure play fails.")]
story += [qa(17, "Trade on it: I'll pay you the number of H in 10 flips at $5 per H... wait, I mean I sell you each H at $5. Deal?",
    ["E[H] = 5, so zero EV at $5 - fair but with no edge and variance, decline as a risk-neutral trader with transaction costs.",
     "If price were $4.80 you buy; quantify edge = 0.2 per flip-set and relate to your Polymarket threshold of 3 percentage points."],
    "Trick phrasing happens; slow down one second, restate the payoff to confirm, then answer.")]

story += h1("5. Your Stories (90 seconds each, rehearsed)")
story += [Paragraph("<b>A. Polymarket systematic book (HKU team).</b> Found &gt;3pp price-vs-outcome gaps by topic and time-to-resolution; built the scan-rank-limit-execute pipeline; tracked realized P&amp;L. Frame as: edge discovery, execution discipline, P&amp;L accountability - exactly a systematic trading loop.", S["body"])]
story += [Paragraph("<b>B. Hang Seng rebalancing prediction (Dymon Asia).</b> Rulebook to point-in-time signals, 82.6% action-level hit rate on 224 events, auditable pipeline, LLM-assisted screening. Frame as: alternative data, backtesting rigor, leakage control - exactly quant research craft.", S["body"])]
story += [Paragraph("<b>C. Lightning Network MDP (Oxford).</b> Stochastic control, value iteration - your answer to 'hardest math you've done for fun'.", S["body"])]
story += [Paragraph("Behavioral prep: why SIG (entrepreneurial desks, education program, HK placement goal); a time you were wrong (have one with numbers); how you handle losing streaks (risk limits from your Polymarket book).", S["body"])]

story += h1("6. Strategy for the Day")
for t in [
 "<b>Before:</b> sleep, warm up 20 minutes of mental math the morning of (not hours), re-read this sheet once.",
 "<b>During:</b> think aloud in structured steps (assumptions, method, arithmetic, sanity check). If stuck, restate the problem - half the time the restate reveals the trick.",
 "<b>Speed vs accuracy:</b> they interrupt to add twists; expect the question to change mid-answer - that is a feature, not an attack.",
 "<b>Hong Kong placement:</b> say explicitly: 'My goal is the Hong Kong office - it is where I studied and interned, and I hold an IANG visa with unrestricted work rights.' (JD lists HK placement + sponsorship as standard.)",
 "<b>Ask them:</b> 'How do junior researchers get their first live strategy?' or 'How is the education program structured for the HK cohort?'",
 "<b>After:</b> log every question you were asked into your tracker the same day - SIG recycles patterns across rounds.",
]:
    story.append(Paragraph(t, S["body"]))

doc = SimpleDocTemplate(r"D:\zcode\hk-dashboard\SIG_Interview_Prep_2026.pdf", pagesize=A4,
                        leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=14*mm,
                        title="SIG Interview Prep - Jing Xiang Xu", author="Jing Xiang Xu")
def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont(F, 7.5)
    canvas.setFillColor("#68758a")
    canvas.drawString(18*mm, 9*mm, "SIG Interview Prep - Jing Xiang Xu - private study sheet")
    canvas.drawRightString(A4[0]-18*mm, 9*mm, "Page %d" % doc_.page)
    canvas.restoreState()
doc.build(story, onFirstPage=footer, onLaterPages=footer)

import pypdf
r = pypdf.PdfReader(r"D:\zcode\hk-dashboard\SIG_Interview_Prep_2026.pdf")
print("pages:", len(r.pages))
