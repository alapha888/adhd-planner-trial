#!/usr/bin/env python3
"""Generate the ADHD Planner free trial PDF (10 pages, 768x1024 pt).

Original layout and copy, written for this trial. Method only (reportlab
generation + pypdf link check) follows the publicly documented approach of
generating a hyperlinked planner PDF with reportlab and validating every
internal link with pypdf. No existing planner's layout, copy, or page
structure was copied.

Usage: python3 build_pdf.py [output.pdf]
Default output: adhd-planner-trial-10pages.pdf (same directory as script).
Requires: reportlab (BSD licence).
"""

import os
import sys

from reportlab.lib.pagesizes import landscape  # noqa: F401  (kept for clarity)
from reportlab.pdfgen import canvas

W, H = 768, 1024  # GoodNotes import size, points

# Palette: neutral paper + one accent. No illustrations, structure wins.
PAPER = (0.984, 0.980, 0.969)   # #FBFAF7
INK = (0.149, 0.149, 0.149)     # #262626
MUTED = (0.420, 0.420, 0.420)   # #6B6B6B
ACCENT = (0.180, 0.431, 0.408)  # #2E6E68 teal
ACCENT_TINT = (0.890, 0.937, 0.925)  # #E3EFEC
LINE = (0.847, 0.835, 0.808)    # #D8D5CE
WHITE = (1.0, 1.0, 1.0)
BOX = (1.0, 1.0, 1.0)

MARGIN = 48
CONTENT_W = W - 2 * MARGIN


def _color(c, rgb):
    c.setFillColorRGB(*rgb)
    c.setStrokeColorRGB(*rgb)


def _hline(c, x1, x2, y, rgb=LINE, width=0.75):
    c.setStrokeColorRGB(*rgb)
    c.setLineWidth(width)
    c.line(x1, y, x2, y)


def _box(c, x, y_top, w, h, fill=BOX, stroke=LINE, width=0.75, radius=6):
    c.setFillColorRGB(*fill)
    c.setStrokeColorRGB(*stroke)
    c.setLineWidth(width)
    c.roundRect(x, y_top - h, w, h, radius, stroke=1, fill=1)


def _checkbox(c, x, y, size=14):
    c.setStrokeColorRGB(*INK)
    c.setLineWidth(1)
    c.setFillColorRGB(*WHITE)
    c.rect(x, y, size, size, stroke=1, fill=1)


def _ruled_lines(c, x, y_top, x_end, count, gap=30):
    y = y_top
    for _ in range(count):
        _hline(c, x, x_end, y)
        y -= gap
    return y


def _title_block(c, title, subtitle):
    """Page header: small eyebrow, title, subtitle, accent rule."""
    y = H - 56
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "ADHD PLANNER  ·  FREE TRIAL")
    y -= 34
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(MARGIN, y, title)
    y -= 26
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 13)
    c.drawString(MARGIN, y, subtitle)
    y -= 18
    _hline(c, MARGIN, W - MARGIN, y, rgb=ACCENT, width=2)
    return y - 28  # content top


def _footer(c, page_no, total=10):
    y = 36
    _hline(c, MARGIN, W - MARGIN, y + 14)
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN, y, "ADHD Planner — Free 10-page trial")
    c.drawRightString(W - MARGIN, y, f"Page {page_no} of {total}")


def _nav(c, prev_dest, next_dest, next_label="Next"):
    """Top-right nav strip on content pages: Index link + Next link."""
    y = H - 34
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "‹  Index")
    c.linkRect("", "index", (MARGIN, y - 4, MARGIN + 70, y + 14), relative=0)
    c.drawRightString(W - MARGIN, y, f"{next_label}  ›")
    c.linkRect("", next_dest, (W - MARGIN - 70, y - 4, W - MARGIN, y + 14), relative=0)


# ---------------------------------------------------------------- pages

def page_cover(c):
    c.bookmarkPage("cover")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    # Accent band
    c.setFillColorRGB(*ACCENT)
    c.rect(0, H - 150, W, 150, stroke=0, fill=1)
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, H - 66, "ADHD PLANNER")
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, H - 88, "Built for brains that work differently.")
    # Main title
    y = H - 260
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 44)
    c.drawString(MARGIN, y, "The Calm Start")
    y -= 56
    c.drawString(MARGIN, y, "Planner")
    y -= 44
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 15)
    c.drawString(MARGIN, y, "A low-pressure daily, weekly, and monthly system")
    y -= 26
    c.drawString(MARGIN, y, "for adults with ADHD and executive-function")
    y -= 26
    c.drawString(MARGIN, y, "challenges. Small steps. No guilt trips.")
    # What is inside
    y -= 70
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "Inside this free trial (10 pages):")
    y -= 30
    c.setFont("Helvetica", 13)
    c.setFillColorRGB(*MUTED)
    for line in [
        "Daily plan  ·  Weekly plan  ·  Brain dump",
        "Task breakdown  ·  Dopamine menu",
        "Low-pressure tracker  ·  Month overview",
    ]:
        c.drawString(MARGIN + 16, y, "—  " + line)
        y -= 26
    # Start button
    y -= 40
    bx, by, bw, bh = MARGIN, y - 16, 220, 52
    c.setFillColorRGB(*ACCENT)
    c.roundRect(bx, by, bw, bh, 8, stroke=0, fill=1)
    c.setFillColorRGB(*WHITE)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(bx + bw / 2, by + 19, "Start  →")
    c.linkRect("", "index", (bx, by, bx + bw, by + bh), relative=0)
    # Footer note
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, 60, "Free trial — 10 pages. Full planner coming after trial validation.")
    c.drawString(MARGIN, 42, "Import into GoodNotes or Notability. Tap the links to jump between pages.")


def page_index(c):
    c.bookmarkPage("index")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    y = _title_block(c, "Index", "Tap a section to jump straight to it.")
    items = [
        ("Daily Plan", "Your top 3, time blocks, and one win.", "daily", "3"),
        ("Weekly Plan", "One focus per day, and what can wait.", "weekly", "4"),
        ("Brain Dump", "Catch every thought, sort it later.", "dump", "5"),
        ("Task Breakdown", "Turn one big task into tiny steps.", "breakdown", "6"),
        ("Dopamine Menu", "Quick rewards, ready before you need them.", "dopamine", "7"),
        ("Low-Pressure Tracker", "Track without streaks that punish you.", "tracker", "8"),
        ("Month Overview", "The whole month on one calm page.", "month", "9"),
        ("How to Use", "Import, links, and the three rules.", "howto", "10"),
    ]
    row_h = 78
    for title, desc, dest, num in items:
        _box(c, MARGIN, y, CONTENT_W, row_h - 12)
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(MARGIN + 20, y - 42, num)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(MARGIN + 58, y - 34, title)
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 12)
        c.drawString(MARGIN + 58, y - 56, desc)
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 14)
        c.drawRightString(W - MARGIN - 18, y - 42, "›")
        c.linkRect("", dest, (MARGIN, y - (row_h - 12), MARGIN + CONTENT_W, y), relative=0)
        y -= row_h
    _footer(c, 2)


def page_daily(c):
    c.bookmarkPage("daily")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "index", "weekly")
    y = _title_block(c, "Daily Plan", "Three things only. Everything else can wait.")
    # Date line
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Date:")
    _hline(c, MARGIN + 48, MARGIN + 260, y - 2)
    c.drawString(MARGIN + 300, y, "Today's one word:")
    _hline(c, MARGIN + 448, W - MARGIN, y - 2)
    y -= 34
    # Top 3
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "Top 3 today")
    y -= 12
    for i in range(1, 4):
        _box(c, MARGIN, y, CONTENT_W, 52)
        _checkbox(c, MARGIN + 16, y - 34)
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 12)
        c.drawString(MARGIN + 44, y - 30, f"{i}.")
        y -= 64
    y -= 6
    # Time blocks
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "Time blocks")
    y -= 12
    for hour in ["7:00", "9:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00"]:
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 12)
        c.drawString(MARGIN, y - 16, hour)
        _hline(c, MARGIN + 56, W - MARGIN, y - 16)
        y -= 30
    y -= 8
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "One thing I can finish in 10 minutes")
    y -= 12
    _box(c, MARGIN, y, CONTENT_W, 44)
    y -= 64
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "End of the day — one win")
    y -= 12
    _box(c, MARGIN, y, CONTENT_W, 44)
    _footer(c, 3)


def page_weekly(c):
    c.bookmarkPage("weekly")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "daily", "dump")
    y = _title_block(c, "Weekly Plan", "One focus per day. The rest is optional.")
    # Week of
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Week of:")
    _hline(c, MARGIN + 72, MARGIN + 300, y - 2)
    c.drawString(MARGIN + 330, y, "This week's focus:")
    _hline(c, MARGIN + 470, W - MARGIN, y - 2)
    y -= 36
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        _box(c, MARGIN, y, CONTENT_W, 74)
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(MARGIN + 16, y - 30, day)
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 11)
        c.drawString(MARGIN + 16, y - 52, "Top 1:")
        _hline(c, MARGIN + 150, MARGIN + 420, y - 52)
        _checkbox(c, MARGIN + 440, y - 56)
        c.drawString(MARGIN + 462, y - 52, "done")
        _checkbox(c, MARGIN + 530, y - 56)
        c.drawString(MARGIN + 552, y - 52, "moved")
        y -= 86
    y -= 4
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "What can wait until next week")
    y -= 12
    _box(c, MARGIN, y, CONTENT_W, 52)
    _ruled_lines(c, MARGIN + 16, y - 22, W - MARGIN - 16, 1, gap=30)
    _footer(c, 4)


def page_dump(c):
    c.bookmarkPage("dump")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "weekly", "breakdown")
    y = _title_block(c, "Brain Dump", "Catch it, don't judge it. Sorting comes later.")
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, y, "Write everything on your mind — tasks, ideas, worries, reminders.")
    y -= 26
    c.drawString(MARGIN, y, "No order needed. No complete sentences needed.")
    y -= 24
    y = _ruled_lines(c, MARGIN, y, W - MARGIN, 12, gap=32)
    y -= 18
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "Sort it — only when you are ready")
    y -= 16
    buckets = [("Do now", "Needs doing today."), ("Schedule", "Give it a day and a time."), ("Drop", "Not mine. Not now. Let it go.")]
    col_w = (CONTENT_W - 2 * 16) / 3
    for i, (name, desc) in enumerate(buckets):
        x = MARGIN + i * (col_w + 16)
        _box(c, x, y, col_w, 96, fill=ACCENT_TINT, stroke=ACCENT)
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 14, y - 30, name)
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 11)
        c.drawString(x + 14, y - 52, desc)
        _ruled_lines(c, x + 14, y - 66, x + col_w - 14, 1, gap=30)
    _footer(c, 5)


def page_breakdown(c):
    c.bookmarkPage("breakdown")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "dump", "dopamine")
    y = _title_block(c, "Task Breakdown", "One big task. Tiny steps. Start with the smallest.")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "The big task")
    y -= 12
    _box(c, MARGIN, y, CONTENT_W, 52)
    y -= 72
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "Break it down — each step under 15 minutes")
    y -= 12
    for i in range(1, 7):
        _box(c, MARGIN, y, CONTENT_W, 56)
        _checkbox(c, MARGIN + 16, y - 36)
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 12)
        c.drawString(MARGIN + 44, y - 32, f"Step {i}")
        c.drawRightString(W - MARGIN - 16, y - 32, "≈ ___ min")
        y -= 68
    y -= 4
    _box(c, MARGIN, y, CONTENT_W, 84, fill=ACCENT_TINT, stroke=ACCENT)
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 16, y - 28, "Stuck? Shrink the step.")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 16, y - 52, "“Open the document” counts. “Find the file” counts.")
    c.drawString(MARGIN + 16, y - 70, "The first step only has to take under 5 minutes.")
    _footer(c, 6)


def page_dopamine(c):
    c.bookmarkPage("dopamine")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "breakdown", "tracker")
    y = _title_block(c, "Dopamine Menu", "Pick your reward before you need it — not after you crash.")
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN, y, "Fill this in on a good day. On a hard day, just pick one and do it.")
    y -= 28
    cols = [
        ("Quick — under 5 min", "A song, a stretch, fresh air, water."),
        ("Medium — 5 to 15 min", "A walk, a snack, a chapter, a call."),
        ("Longer — 15 to 30 min", "A bath, a game level, a hobby session."),
    ]
    col_w = (CONTENT_W - 2 * 16) / 3
    top = y
    for i, (name, desc) in enumerate(cols):
        x = MARGIN + i * (col_w + 16)
        _box(c, x, top, col_w, 380, fill=BOX)
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(x + 14, top - 30, name)
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 11)
        # wrap desc manually (short strings, split once)
        c.drawString(x + 14, top - 50, desc.split(",")[0] + ",")
        c.drawString(x + 14, top - 66, desc.split(",", 1)[1].strip())
        _ruled_lines(c, x + 14, top - 92, x + col_w - 14, 8, gap=32)
    y = top - 380 - 24
    _box(c, MARGIN, y, CONTENT_W, 96, fill=ACCENT_TINT, stroke=ACCENT)
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 16, y - 28, "How to use it")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 16, y - 52, "1. Pick one small reward BEFORE a hard task.")
    c.drawString(MARGIN + 16, y - 70, "2. Pick one AFTER you finish — that is the deal.")
    c.drawString(MARGIN + 16, y - 88, "3. No earning it by suffering first. The menu is always open.")
    _footer(c, 7)


def page_tracker(c):
    c.bookmarkPage("tracker")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "dopamine", "month")
    y = _title_block(c, "Low-Pressure Tracker", "Miss a day? The streak is not broken. Just do the next one.")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Week of:")
    _hline(c, MARGIN + 72, MARGIN + 300, y - 2)
    y -= 36
    habits = ["Move my body", "Drink water", "Tidy one spot", "One task done",
              "Screen-free hour", "Sleep on time", "Something kind"]
    days = ["M", "T", "W", "T", "F", "S", "S"]
    # Header row
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica-Bold", 12)
    label_w = 300
    cell = (CONTENT_W - label_w) / 7
    for i, d in enumerate(days):
        c.drawCentredString(MARGIN + label_w + cell * i + cell / 2, y, d)
    y -= 14
    _hline(c, MARGIN, W - MARGIN, y, rgb=INK, width=1)
    y -= 26
    for habit in habits:
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 13)
        c.drawString(MARGIN, y, habit)
        for i in range(7):
            _checkbox(c, MARGIN + label_w + cell * i + cell / 2 - 7, y - 4, size=14)
        y -= 44
        _hline(c, MARGIN, W - MARGIN, y + 12)
    y -= 22
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "How did the week feel?  (circle one)")
    y -= 34
    for i in range(1, 6):
        x = MARGIN + (i - 1) * 64
        c.setStrokeColorRGB(*ACCENT)
        c.setLineWidth(1.2)
        c.circle(x + 18, y, 16, stroke=1, fill=0)
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 13)
        c.drawCentredString(x + 18, y - 5, str(i))
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 5 * 64 + 10, y - 5, "1 = rough      5 = steady")
    y -= 60
    _box(c, MARGIN, y, CONTENT_W, 84, fill=ACCENT_TINT, stroke=ACCENT)
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 16, y - 28, "The only rule")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 12)
    c.drawString(MARGIN + 16, y - 52, "A blank box is information, not failure. Look for patterns,")
    c.drawString(MARGIN + 16, y - 70, "not perfection — then change one thing next week.")
    _footer(c, 8)


def page_month(c):
    c.bookmarkPage("month")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "tracker", "howto")
    y = _title_block(c, "Month Overview", "The whole month on one page. Big picture only.")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Month:")
    _hline(c, MARGIN + 56, MARGIN + 260, y - 2)
    c.drawString(MARGIN + 300, y, "One theme for this month:")
    _hline(c, MARGIN + 500, W - MARGIN, y - 2)
    y -= 32
    # Calendar grid 5 rows x 7 cols
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    col_w = CONTENT_W / 7
    row_h = 78
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica-Bold", 11)
    for i, d in enumerate(days):
        c.drawCentredString(MARGIN + col_w * i + col_w / 2, y, d)
    y -= 12
    for r in range(5):
        for i in range(7):
            x = MARGIN + col_w * i
            _box(c, x, y, col_w - 4, row_h - 6, radius=4)
        y -= row_h
    y -= 10
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "3 things I want to finish this month")
    y -= 12
    for i in range(1, 4):
        _box(c, MARGIN, y, CONTENT_W, 44)
        _checkbox(c, MARGIN + 16, y - 30)
        c.setFillColorRGB(*MUTED)
        c.setFont("Helvetica", 12)
        c.drawString(MARGIN + 44, y - 26, f"{i}.")
        y -= 56
    y -= 2
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, y, "What I will NOT do this month")
    y -= 12
    _box(c, MARGIN, y, CONTENT_W, 44)
    _footer(c, 9)


def page_howto(c):
    c.bookmarkPage("howto")
    c.setFillColorRGB(*PAPER)
    c.rect(0, 0, W, H, stroke=0, fill=1)
    _nav(c, "month", "index", next_label="Back to Index")
    y = _title_block(c, "How to Use", "Three minutes to set up. Thirty seconds a day to keep.")
    steps = [
        ("1. Import it",
         "In GoodNotes or Notability, choose Import and select this PDF.",
         "It opens as a notebook — every link below already works."),
        ("2. Tap to move around",
         "Tap “Index” at the top of any page to come back here.",
         "Tap “Next” to move forward one page at a time."),
        ("3. Write on it",
         "Use your stylus or the text tool. Duplicate a page whenever",
         "you need a fresh copy — daily and weekly pages are reusable."),
        ("4. Start small",
         "Fill in only the Top 3 each morning. Skip everything else",
         "until the Top 3 feels easy. That is the whole system."),
    ]
    for title, l1, l2 in steps:
        c.setFillColorRGB(*ACCENT)
        c.setFont("Helvetica-Bold", 15)
        c.drawString(MARGIN, y, title)
        y -= 24
        c.setFillColorRGB(*INK)
        c.setFont("Helvetica", 13)
        c.drawString(MARGIN + 16, y, l1)
        y -= 22
        c.drawString(MARGIN + 16, y, l2)
        y -= 34
    _box(c, MARGIN, y, CONTENT_W, 110, fill=ACCENT_TINT, stroke=ACCENT)
    c.setFillColorRGB(*ACCENT)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(MARGIN + 16, y - 28, "The three rules")
    c.setFillColorRGB(*INK)
    c.setFont("Helvetica", 13)
    c.drawString(MARGIN + 16, y - 52, "1.  Small is a win. A 5-minute step still counts.")
    c.drawString(MARGIN + 16, y - 70, "2.  Missed days are data, not failure. Restart, don't catch up.")
    c.drawString(MARGIN + 16, y - 88, "3.  If a page feels heavy, use fewer boxes — never more.")
    y -= 150
    c.setFillColorRGB(*MUTED)
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "This is a free 10-page trial. The full planner will be released after")
    y -= 18
    c.drawString(MARGIN, y, "trial validation. Questions or feedback: see the project README.")
    _footer(c, 10)


PAGES = [
    page_cover,
    page_index,
    page_daily,
    page_weekly,
    page_dump,
    page_breakdown,
    page_dopamine,
    page_tracker,
    page_month,
    page_howto,
]


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "adhd-planner-trial-10pages.pdf")
    c = canvas.Canvas(out, pagesize=(W, H))
    c.setTitle("ADHD Planner — Free 10-Page Trial")
    c.setAuthor("ADHD Planner (trial)")
    for fn in PAGES:
        fn(c)
        c.showPage()
    c.save()
    print(f"Wrote {out} ({len(PAGES)} pages, {os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
