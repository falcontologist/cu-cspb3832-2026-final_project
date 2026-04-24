"""Build the ASC Classifier presentation as a native PDF.

All 16 slides are drawn from scratch using ReportLab primitives.
Design system mirrors the HTML deck: Source Serif 4 (display/titles/italic
examples) + Source Sans 3 (body/UI), four type sizes, Tufte cream content
slides, charcoal dark slides for Title / Conclusion / Future Work.
"""

import math
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import HexColor

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")
OUT_PATH = os.path.join(HERE, "Final Project Presentation Slides.pdf")

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
_FONTS = {
    "Serif":      "SourceSerif4-Regular.ttf",
    "Serif-Bold": "SourceSerif4-Bold.ttf",
    "Serif-It":   "SourceSerif4-It.ttf",
    "Sans-Light": "SourceSans3-Light.ttf",
    "Sans":       "SourceSans3-Regular.ttf",
    "Sans-Bold":  "SourceSans3-Semibold.ttf",
    "Sans-It":    "SourceSans3-It.ttf",
}
for name, fn in _FONTS.items():
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
BODY        = HexColor("#2D3436")
HEADING     = HexColor("#36454F")
ACCENT      = HexColor("#B85042")
GREEN       = HexColor("#2e7d4f")
GOLD        = HexColor("#C5952B")
CAPTION     = HexColor("#888888")
BG          = HexColor("#FAFAF2")
ROW_ALT     = HexColor("#F2F0E8")
GRAY_LIGHT  = HexColor("#F5F5F5")
GRAY_BAR    = HexColor("#D5D5D5")
DARK_BG     = HexColor("#36454F")
DARK_TEXT   = HexColor("#FFFFFF")
DARK_SECOND = HexColor("#C8CED3")
DARK_TERT   = HexColor("#8E9AA5")
DARK_ACCENT = HexColor("#E8856F")
WHITE       = HexColor("#FFFFFF")
CITE_BORDER = HexColor("#E8E4D8")

# ---------------------------------------------------------------------------
# Sizes & layout
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = 1920, 1080

S_DISPLAY = 84
S_TITLE   = 56
S_BODY    = 28
S_CAPTION = 22

LINE_HEIGHT = 1.5

TITLE_Y_TOP = 90       # y-from-top for title baseline top
CONTENT_W = int(PAGE_W * 0.68)
CONTENT_X = (PAGE_W - CONTENT_W) // 2       # 307
CONTENT_RIGHT = CONTENT_X + CONTENT_W

# Translate top-down y into ReportLab's bottom-up y.
def ytop(y_from_top: float) -> float:
    return PAGE_H - y_from_top

def ascent(font: str, size: float) -> float:
    return pdfmetrics.getAscent(font) / 1000.0 * size

def descent(font: str, size: float) -> float:
    return abs(pdfmetrics.getDescent(font)) / 1000.0 * size

def text_height(font: str, size: float) -> float:
    return ascent(font, size) + descent(font, size)

def line_h(size: float) -> float:
    return size * LINE_HEIGHT

# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------
def draw_text(c, x: float, y_top: float, text: str, font: str, size: float, color,
              align: str = "left") -> float:
    """Draw a single line, top aligned to y_top. Returns y_top + size*line_height."""
    c.setFont(font, size)
    c.setFillColor(color)
    baseline = ytop(y_top + ascent(font, size))
    if align == "left":
        c.drawString(x, baseline, text)
    elif align == "center":
        c.drawCentredString(x, baseline, text)
    elif align == "right":
        c.drawRightString(x, baseline, text)
    return y_top + line_h(size)

def wrap_text(text: str, font: str, size: float, max_width: float):
    """Manually wrap text into lines that fit max_width."""
    words = text.split()
    lines, current = [], []
    for w in words:
        trial = " ".join(current + [w])
        if stringWidth(trial, font, size) <= max_width:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
                current = [w]
            else:
                lines.append(w)
                current = []
    if current:
        lines.append(" ".join(current))
    return lines

def draw_paragraph(c, x: float, y_top: float, text: str, font: str, size: float,
                   color, max_width: float, align: str = "left") -> float:
    """Word-wrap and draw; return final y_top (bottom of paragraph)."""
    lines = wrap_text(text, font, size, max_width)
    for line in lines:
        cx = x if align == "left" else (x + max_width / 2 if align == "center" else x + max_width)
        y_top = draw_text(c, cx, y_top, line, font, size, color, align=align)
    return y_top

def draw_multiline(c, x: float, y_top: float, lines, font: str, size: float, color,
                   align: str = "left", max_width: float = None) -> float:
    """Draw explicit lines (already split). Returns bottom y_top."""
    for line in lines:
        cx = x if align == "left" else (x + (max_width or 0) / 2 if align == "center" else x + (max_width or 0))
        y_top = draw_text(c, cx, y_top, line, font, size, color, align=align)
    return y_top

# ---------------------------------------------------------------------------
# Shape helpers
# ---------------------------------------------------------------------------
def fill_rect(c, x, y_top, w, h, color):
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.rect(x, ytop(y_top + h), w, h, stroke=0, fill=1)

def stroke_rect(c, x, y_top, w, h, color, lw=1.0):
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(lw)
    c.rect(x, ytop(y_top + h), w, h, stroke=1, fill=0)

def fill_circle(c, cx, cy_top, r, color):
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.circle(cx, ytop(cy_top), r, stroke=0, fill=1)

def bg(c, dark: bool = False):
    c.setFillColor(DARK_BG if dark else BG)
    c.setStrokeColor(DARK_BG if dark else BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)

# ---------------------------------------------------------------------------
# Standardized arrow — "→" and "↓" drawn as vector strokes for crispness
# ---------------------------------------------------------------------------
# Arrow visual scale set to roughly match 2.2em size (arrow size × 2.2 in HTML).
ARROW_SCALE = 2.2
ARROW_SIZE  = S_BODY * ARROW_SCALE   # ~61

def arrow_right(c, cx, cy_top, color=CAPTION, size=ARROW_SIZE, weight=2.0):
    """Draw a centered right-pointing arrow ~size wide."""
    half = size / 2
    y = ytop(cy_top)
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.setLineCap(1)
    c.setLineJoin(1)
    # shaft
    c.line(cx - half, y, cx + half, y)
    # head
    head = size * 0.28
    c.line(cx + half, y, cx + half - head, y + head * 0.8)
    c.line(cx + half, y, cx + half - head, y - head * 0.8)

def arrow_down(c, cx, cy_top, color=CAPTION, size=ARROW_SIZE, weight=2.0):
    half = size / 2
    x = cx
    y_top_abs = ytop(cy_top - half)
    y_bot_abs = ytop(cy_top + half)
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.line(x, y_top_abs, x, y_bot_abs)
    head = size * 0.28
    c.line(x, y_bot_abs, x - head * 0.8, y_bot_abs + head)
    c.line(x, y_bot_abs, x + head * 0.8, y_bot_abs + head)

def arrow_up(c, cx, cy_top, color=CAPTION, size=ARROW_SIZE, weight=2.0):
    half = size / 2
    x = cx
    y_top_abs = ytop(cy_top - half)
    y_bot_abs = ytop(cy_top + half)
    c.setStrokeColor(color)
    c.setLineWidth(weight)
    c.setLineCap(1)
    c.setLineJoin(1)
    c.line(x, y_bot_abs, x, y_top_abs)
    head = size * 0.28
    c.line(x, y_top_abs, x - head * 0.8, y_top_abs - head)
    c.line(x, y_top_abs, x + head * 0.8, y_top_abs - head)

# ---------------------------------------------------------------------------
# Slide header
# ---------------------------------------------------------------------------
def draw_h2(c, text: str) -> float:
    """Slide title; returns y_top below the title (for subsequent content)."""
    c.setFont("Serif-Bold", S_TITLE)
    c.setFillColor(HEADING)
    baseline = ytop(TITLE_Y_TOP + ascent("Serif-Bold", S_TITLE))
    c.drawString(CONTENT_X, baseline, text)
    return TITLE_Y_TOP + line_h(S_TITLE) + 30   # margin below title

# ---------------------------------------------------------------------------
# =========================== SLIDES ========================================
# ---------------------------------------------------------------------------
def slide_1_title(c):
    bg(c, dark=True)
    # Center everything vertically and horizontally
    # Title
    title_lines = [
        "Fine-Tuning a Bidirectional Cross-Encoder",
        "for Verbal Clause Construction Classification",
    ]
    # Compute stacked height
    t_size = S_TITLE
    t_line = t_size * 1.2
    total_title_h = t_line * len(title_lines)
    block_y_top = (PAGE_H - total_title_h) / 2 - 100
    for i, line in enumerate(title_lines):
        c.setFont("Serif-Bold", t_size)
        c.setFillColor(DARK_TEXT)
        y = ytop(block_y_top + i * t_line + ascent("Serif-Bold", t_size))
        c.drawCentredString(PAGE_W / 2, y, line)

    # Gap then author
    author_y_top = block_y_top + total_title_h + 180
    draw_text(c, PAGE_W / 2, author_y_top, "Josh Falconer", "Sans", S_BODY, DARK_TEXT, align="center")
    # Course info
    course_y_top = author_y_top + S_BODY * 1.6
    draw_text(c, PAGE_W / 2, course_y_top,
              "CSPB 3823 NLP \u00B7 Spring 2026 \u00B7 Prof. Curry Guinn",
              "Sans-Light", S_CAPTION, DARK_TERT, align="center")


def slide_2_problem(c):
    bg(c)
    y = draw_h2(c, "The Problem")

    # Two-column examples
    col_gap = 80
    col_w = (CONTENT_W - col_gap) // 2
    left_x = CONTENT_X
    right_x = CONTENT_X + col_w + col_gap

    def draw_example(x, y_top, sentence_pre, highlight, sentence_post, situation, gloss):
        # Wrap the full sentence with an inline highlight. Build word list with
        # styling spans.
        # Simplification: render as wrapped lines by splitting the full plain
        # sentence into words, track which words overlap the highlight.
        full = f'\u201C{sentence_pre}{highlight}{sentence_post}\u201D'
        # Break into tokens where we keep the highlight as one token
        pre = f'\u201C{sentence_pre}'
        post = f'{sentence_post}\u201D'
        # Manual wrap: try to fit the whole thing; wrap on spaces.
        # We'll wrap by alternating styled runs.
        runs = [
            (pre, "Serif-It", BODY),
            (highlight, "Sans-Bold", GREEN),
            (post, "Serif-It", BODY),
        ]
        lines = _wrap_runs(runs, S_BODY, col_w)
        cy = y_top
        for line in lines:
            _draw_runs_line(c, x, cy, line, S_BODY)
            cy += line_h(S_BODY)
        # Arrow
        cy += 24
        arrow_down(c, x + col_w / 2, cy + ARROW_SIZE / 2 - 6, color=CAPTION)
        cy += ARROW_SIZE + 18
        # Situation
        cy = draw_text(c, x + col_w / 2, cy, situation, "Sans-Bold", S_BODY, GREEN, align="center")
        cy += 6
        draw_text(c, x + col_w / 2, cy, gloss, "Sans-Light", S_CAPTION, CAPTION, align="center")

    draw_example(left_x,  y,
                 "Unilever is ", "looking", " for sustainable palm oil suppliers in Southeast Asia.",
                 "Intention",
                 "intender attends to a future, as yet unrealized outcome")
    draw_example(right_x, y,
                 "Traders are ", "looking", " at unusual options activity ahead of earnings reports.",
                 "Perception (exp. subj.)",
                 "perceiver directs attention to a stimulus")

    # Coda at bottom
    coda = "Same verb, different construction, different participants, different meaning."
    draw_text(c, PAGE_W / 2, PAGE_H - 160, coda, "Serif-It", S_BODY, BODY, align="center")


# Styled-run helpers (for Slide 2 highlighted sentences)
def _wrap_runs(runs, size, max_width):
    """Wrap a list of (text, font, color) runs into a list of lines,
    each line is a list of (text, font, color) chunks."""
    # Tokenize into styled words preserving spaces between words in same run.
    words = []
    for text, font, color in runs:
        parts = text.split(" ")
        for i, p in enumerate(parts):
            prefix = "" if i == 0 else " "
            if p == "" and prefix == "":
                continue
            words.append((prefix + p, font, color))

    lines, current, cw = [], [], 0
    space_w = lambda font: stringWidth(" ", font, size)
    for w, font, color in words:
        ww = stringWidth(w, font, size)
        if cw + ww <= max_width or not current:
            current.append((w, font, color))
            cw += ww
        else:
            # trim leading space from the first token for display
            lines.append(current)
            stripped = w.lstrip()
            ww2 = stringWidth(stripped, font, size)
            current = [(stripped, font, color)]
            cw = ww2
    if current:
        lines.append(current)
    # Strip leading space from first element of each line
    for ln in lines:
        if ln and ln[0][0].startswith(" "):
            txt, f, col = ln[0]
            ln[0] = (txt.lstrip(), f, col)
    return lines


def _draw_runs_line(c, x, y_top, chunks, size):
    cur_x = x
    for text, font, color in chunks:
        c.setFont(font, size)
        c.setFillColor(color)
        baseline = ytop(y_top + ascent(font, size))
        c.drawString(cur_x, baseline, text)
        cur_x += stringWidth(text, font, size)


def slide_3_motivation(c):
    bg(c)
    y = draw_h2(c, "Why This Matters")

    # Three-column icon row
    # Compute column centers
    # Columns at roughly 25%, 50%, 75%
    cx1, cx2, cx3 = PAGE_W * 0.28, PAGE_W * 0.5, PAGE_W * 0.72
    icon_center_y = 430

    # Icon 1: document
    doc_w, doc_h = 120, 148
    doc_x = cx1 - doc_w / 2
    doc_y = icon_center_y - doc_h / 2
    stroke_rect(c, doc_x, doc_y, doc_w, doc_h, HEADING, lw=2)
    # interior lines
    line_widths = [1.0, 0.78, 1.0, 0.62, 0.90, 0.48]
    for i, lw in enumerate(line_widths):
        lx = doc_x + 16
        lw_px = (doc_w - 32) * lw
        ly = doc_y + 22 + i * 18
        c.setFillColor(HexColor("#D8D8D8"))
        c.setStrokeColor(HexColor("#D8D8D8"))
        c.rect(lx, ytop(ly + 5), lw_px, 5, stroke=0, fill=1)

    # Icon 2: two solid gray gears
    def gear(cx, cy_top, outer_r, teeth, tooth_len, tooth_w, hole_r):
        cy = ytop(cy_top)
        # body disc
        c.setFillColor(CAPTION)
        c.setStrokeColor(CAPTION)
        c.circle(cx, cy, outer_r, stroke=0, fill=1)
        # teeth as rotated rectangles around center
        for k in range(teeth):
            angle = (2 * math.pi * k) / teeth
            # tooth "root" at outer_r, extends outward by tooth_len
            # draw as rectangle centered along that radial
            c.saveState()
            c.translate(cx, cy)
            c.rotate(math.degrees(angle))
            # rect: x=-w/2, y=outer_r - 1, w=tooth_w, h=tooth_len + 1
            c.rect(-tooth_w / 2, outer_r - 1, tooth_w, tooth_len + 1, stroke=0, fill=1)
            c.restoreState()
        # hole in center — overdraw with page bg
        c.setFillColor(BG)
        c.setStrokeColor(BG)
        c.circle(cx, cy, hole_r, stroke=0, fill=1)

    # Big gear on upper-left of icon 2 area; small gear lower-right.
    gear_center_x = cx2
    gear(gear_center_x - 32, icon_center_y - 22, outer_r=44, teeth=8,
         tooth_len=14, tooth_w=16, hole_r=14)
    gear(gear_center_x + 38, icon_center_y + 30, outer_r=28, teeth=6,
         tooth_len=10, tooth_w=12, hole_r=9)

    # Icon 3: knowledge graph
    # Nodes roughly at corners + center
    nodes = [
        (cx3 - 78, icon_center_y - 50, 12, HEADING),
        (cx3,      icon_center_y,       14, ACCENT),
        (cx3 + 78, icon_center_y - 50, 12, HEADING),
        (cx3 - 50, icon_center_y + 56, 12, HEADING),
        (cx3 + 60, icon_center_y + 48, 12, HEADING),
    ]
    # Edges — center connects to everyone
    center = nodes[1]
    c.setStrokeColor(CAPTION)
    c.setLineWidth(2)
    for i, n in enumerate(nodes):
        if i == 1:
            continue
        c.line(center[0], ytop(center[1]), n[0], ytop(n[1]))
    # Nodes
    for nx, ny, r, col in nodes:
        c.setFillColor(col)
        c.setStrokeColor(col)
        c.circle(nx, ytop(ny), r, stroke=0, fill=1)

    # Labels below icons
    label_y = icon_center_y + 120
    draw_text(c, cx1, label_y, "Unstructured text", "Sans-Bold", S_BODY, HEADING, align="center")
    draw_text(c, cx2, label_y, "ASC Parser",        "Sans-Bold", S_BODY, HEADING, align="center")
    draw_text(c, cx3, label_y, "Knowledge graph",   "Sans-Bold", S_BODY, HEADING, align="center")

    # Arrows between columns
    ay = icon_center_y
    arrow_right(c, (cx1 + cx2) / 2, ay)
    arrow_right(c, (cx2 + cx3) / 2, ay)

    # Question paragraph — centered, at bottom
    lines = [
        "Can a fine-tuned encoder reliably disambiguate",
        "between closely related verbal clause constructions,",
        "as a first step toward automated parsing of argument structure for knowledge graph construction?",
    ]
    # Draw centered, starting well below icons
    p_y = 750
    for ln in lines:
        p_y = draw_text(c, PAGE_W / 2, p_y, ln, "Sans", S_BODY, BODY, align="center")


def slide_4a_dataset_flow(c):
    bg(c)
    y = draw_h2(c, "Gold Dataset")

    # Three columns: sources (w≈30%) -> arrow -> counts (w≈25%) -> arrow -> table (w≈30%)
    top_y = y + 50
    # column 1 x
    col1_x = CONTENT_X
    col1_w = 360
    col2_x = col1_x + col1_w + 80
    col2_w = 320
    col3_x = col2_x + col2_w + 80
    col3_w = 420

    # Column 1: Manual Curation
    cy = top_y
    cy = draw_text(c, col1_x, cy, "Manual Curation", "Sans-Bold", S_BODY, HEADING)
    cy += 14
    sources = ["OntoNotes 5.0", "VerbNet", "FrameNet", "Croft et al. (2021)", "Kalm (2022)"]
    for src in sources:
        # gold dot
        dot_r = 4
        dot_cx = col1_x + dot_r
        dot_cy = cy + ascent("Sans", S_BODY) / 2
        c.setFillColor(GOLD)
        c.setStrokeColor(GOLD)
        c.circle(dot_cx, ytop(dot_cy), dot_r, stroke=0, fill=1)
        draw_text(c, col1_x + dot_r * 2 + 14, cy, src, "Sans", S_BODY, BODY)
        cy += line_h(S_BODY)

    # Column 2: two count lines (bold number + label)
    col_center_x = col2_x + col2_w / 2
    count_y = top_y + 60
    def count_line(y, num, label):
        # Draw centered; compute total width
        f_num, f_lbl = "Serif-Bold", "Sans"
        s = S_BODY
        w_num = stringWidth(num, f_num, s)
        w_space = stringWidth("  ", f_lbl, s)
        w_lbl = stringWidth(label, f_lbl, s)
        total = w_num + w_space + w_lbl
        start_x = col_center_x - total / 2
        c.setFont(f_num, s)
        c.setFillColor(HEADING)
        baseline = ytop(y + ascent(f_num, s))
        c.drawString(start_x, baseline, num)
        c.setFont(f_lbl, s)
        c.setFillColor(BODY)
        c.drawString(start_x + w_num + w_space, baseline, label)
    count_line(count_y, "11,672", "curated seed examples")
    count_line(count_y + line_h(S_BODY) + 12, "1,514", "synthetic examples")

    # Column 3: table
    table_y = top_y + 40
    labels = ["Situations", "Total examples", "Verb lemmas"]
    values = ["62", "13,186", "4,189"]
    row_h = line_h(S_BODY) + 6
    for i, (lab, val) in enumerate(zip(labels, values)):
        ry = table_y + i * row_h
        if i % 2 == 1:
            fill_rect(c, col3_x, ry, col3_w, row_h, ROW_ALT)
        # text
        draw_text(c, col3_x + 16, ry + 6, lab, "Sans", S_BODY, BODY)
        draw_text(c, col3_x + col3_w - 16, ry + 6, val, "Sans-Bold", S_BODY, BODY, align="right")

    # Arrows between columns — centered on the visual middle of the content
    arrow_y = top_y + 130
    arrow_right(c, col1_x + col1_w + 40, arrow_y)
    arrow_right(c, col2_x + col2_w + 40, arrow_y)


def slide_4b_dataset_pairs(c):
    bg(c)
    y = draw_h2(c, "Gold Dataset")

    # Two compact boxes side by side
    gap = 40
    pair_w = (CONTENT_W - gap) / 2
    left_x = CONTENT_X
    right_x = CONTENT_X + pair_w + gap
    top_y = y + 30

    def pair(x, label_text, label_color, sentence, definition):
        box_padding_x = 28
        box_padding_y = 24
        inner_w = pair_w - 2 * box_padding_x

        # Compute content height
        lines_label = [label_text]
        lines_sent  = wrap_text(sentence, "Serif-It", S_BODY, inner_w)
        lines_def   = wrap_text(definition, "Sans", S_CAPTION, inner_w)
        content_h = (
            line_h(S_CAPTION) * len(lines_label) + 14
            + line_h(S_BODY) * len(lines_sent) + 10
            + line_h(S_CAPTION) * len(lines_def)
        )
        box_h = content_h + 2 * box_padding_y
        fill_rect(c, x, top_y, pair_w, box_h, ROW_ALT)

        cy = top_y + box_padding_y
        # Label — uppercase small caps feel
        c.setFont("Sans-Bold", S_CAPTION)
        c.setFillColor(label_color)
        baseline = ytop(cy + ascent("Sans-Bold", S_CAPTION))
        c.drawString(x + box_padding_x, baseline, label_text.upper())
        cy += line_h(S_CAPTION) + 14
        # Sentence
        for ln in lines_sent:
            cy = draw_text(c, x + box_padding_x, cy, ln, "Serif-It", S_BODY, BODY)
        cy += 10
        # Definition
        for ln in lines_def:
            cy = draw_text(c, x + box_padding_x, cy, ln, "Sans", S_CAPTION, CAPTION)
        return top_y + box_h

    box_bottom_a = pair(left_x,
                        "\u2713 Positive pair (Constrain)",
                        GREEN,
                        "\u201CFort Knox holds the United States' official gold reserves.\u201D",
                        "An entity physically constrains the motion of a theme by being spatially co-located with it; the constraining entity can be inanimate or animate.")
    box_bottom_b = pair(right_x,
                        "\u2717 Negative pair (Capacity)",
                        ACCENT,
                        "\u201CFort Knox holds the United States' official gold reserves.\u201D",
                        "Capacity refers to the fit verbs, where oblique arguments are locations, describing the capacity of the location with respect to the action named by the verb (e.g. sleeps, seats, fits, serves).")
    cap_y = max(box_bottom_a, box_bottom_b) + 40
    draw_text(c, CONTENT_X, cap_y,
              "Same sentence, different construction. The Capacity construction requires a specified quantity.",
              "Sans-Light", S_CAPTION, CAPTION)


def slide_5_theory(c):
    bg(c)
    y = draw_h2(c, "Theoretical Foundation")

    # Apex
    apex_y = y + 10
    apex_title = "62 Situation ASCs, computationally applied and extended"
    apex_y = draw_text(c, PAGE_W / 2, apex_y, apex_title, "Serif-Bold", S_BODY, HEADING, align="center")
    apex_y += 24

    lines = [
        "Each Situation is a constructional pattern pairing",
        "a syntactic form with a force-dynamic event structure,",
        "grounded in decades of cross-linguistic typological analysis.",
    ]
    for ln in lines:
        apex_y = draw_text(c, PAGE_W / 2, apex_y, ln, "Sans", S_BODY, BODY, align="center")

    # Up arrow
    apex_y += 20
    arrow_up(c, PAGE_W / 2, apex_y + ARROW_SIZE / 2 - 6, color=CAPTION)
    apex_y += ARROW_SIZE + 16

    # Citation box
    citations = [
        ("Kalm (2022)",         "Social Verbs: A Force-Dynamic Analysis"),
        ("Croft (2022)",        "Morphosyntax: Constructions of the World's Languages"),
        ("Croft et al. (2021)", "Developing Language-Independent Event Representations"),
        ("Croft (2012)",        "Verbs: Aspect and Causal Structure"),
        ("Goldberg (1995)",     "Constructions: A Construction Grammar Approach to Argument Structure"),
        ("Levin (1993)",        "English Verb Classes and Alternations"),
    ]
    box_x = CONTENT_X
    box_w = CONTENT_W
    box_pad_x = 40
    box_pad_y = 28
    row_spacing = line_h(S_BODY) + 6
    box_h = box_pad_y * 2 + row_spacing * len(citations)
    # Fill white bg + subtle border
    fill_rect(c, box_x, apex_y, box_w, box_h, WHITE)
    stroke_rect(c, box_x, apex_y, box_w, box_h, CITE_BORDER, lw=1)

    cy = apex_y + box_pad_y
    for cite, title in citations:
        # author/year bold, title italic
        cite_str = cite + "  "
        c.setFont("Sans-Bold", S_BODY)
        c.setFillColor(HEADING)
        base = ytop(cy + ascent("Sans-Bold", S_BODY))
        c.drawString(box_x + box_pad_x, base, cite_str)
        cw = stringWidth(cite_str, "Sans-Bold", S_BODY)
        c.setFont("Serif-It", S_BODY)
        c.setFillColor(BODY)
        c.drawString(box_x + box_pad_x + cw, base, title)
        cy += row_spacing


def slide_6_tiers(c):
    bg(c)
    y = draw_h2(c, "Tiered Training Data")

    tiers = [
        (1.00, "T1 \u00B7 50% \u00B7 Hard",
         "Same semantic cluster. Shared verbs, adjacent event types. The classifier must learn the finest distinctions."),
        (0.78, "T2 \u00B7 30% \u00B7 Medium",
         "Same broad domain, different cluster. Structurally distinct but lexically overlapping."),
        (0.52, "T3 \u00B7 20% \u00B7 Easy",
         "Different domain. Confirms basic differences."),
    ]

    cy = y + 20
    for frac, label, desc in tiers:
        bar_w = CONTENT_W * frac
        pad_x, pad_y = 36, 24
        inner_w = bar_w - 2 * pad_x
        # compute bar height
        desc_lines = wrap_text(desc, "Sans", S_BODY, inner_w)
        bar_h = pad_y * 2 + line_h(S_BODY) + 12 + line_h(S_BODY) * len(desc_lines)
        fill_rect(c, CONTENT_X, cy, bar_w, bar_h, ROW_ALT)
        # label
        iy = cy + pad_y
        iy = draw_text(c, CONTENT_X + pad_x, iy, label, "Serif-Bold", S_BODY, ACCENT)
        iy += 4
        for ln in desc_lines:
            iy = draw_text(c, CONTENT_X + pad_x, iy, ln, "Sans", S_BODY, BODY)
        cy += bar_h + 26

    cy += 14
    draw_text(c, CONTENT_X, cy, "Applied consistently to both positive and negative examples.",
              "Sans", S_BODY, BODY)


def slide_7_pipeline(c):
    bg(c)
    y = draw_h2(c, "Pipeline")

    stages = [
        ("Dependency Parse",    ["spaCy", "en_core_web_sm"]),
        ("Verb Lemma",          ["NLTK", "WordNet"]),
        ("Candidate Retrieval", ["curated", "pos files"]),
        ("Cross-Encoder Scoring", ["DeBERTa-v3-base", "HuggingFace", "PyTorch \u00B7 MPS"]),
        ("Situation",           ["Croft et al. (2021)", "Kalm (2022)", "+ my extensions"]),
    ]
    pad = 60
    usable_w = PAGE_W - 2 * pad
    gap = 50
    n = len(stages)
    stage_w = (usable_w - gap * (n - 1)) / n
    stage_h = 240
    top_y = y + 40

    for i, (name, tools) in enumerate(stages):
        sx = pad + i * (stage_w + gap)
        fill_rect(c, sx, top_y, stage_w, stage_h, ROW_ALT)
        # Name: up to two lines
        name_words = name.split()
        if len(name_words) >= 2 and len(name) > 14:
            # split roughly in half
            half = max(1, len(name_words) // 2)
            line1 = " ".join(name_words[:half])
            line2 = " ".join(name_words[half:])
            name_lines = [line1, line2]
        else:
            name_lines = [name]
        ty = top_y + 26
        for ln in name_lines:
            ty = draw_text(c, sx + stage_w / 2, ty, ln, "Serif-Bold", S_BODY, HEADING, align="center")
        # Tools
        ty += 14
        for t in tools:
            ty = draw_text(c, sx + stage_w / 2, ty, t, "Sans-Light", S_CAPTION, CAPTION, align="center")

    # Arrows in gaps, between stages
    arrow_y = top_y + stage_h / 2
    for i in range(n - 1):
        gap_center = pad + (i + 1) * stage_w + (i * gap) + gap / 2
        arrow_right(c, gap_center, arrow_y, size=42)

    # Captions below pipeline
    cap_y = top_y + stage_h + 50
    caps = [
        "Training: 5-fold CV \u00B7 AdamW lr=2e-5 \u00B7 batch 32 \u00B7 early stopping",
        "Training time: ~17 hours (5 folds)",
        "Hardware: Apple M4 Mac Mini, 24 GB unified memory",
    ]
    for line in caps:
        cap_y = draw_text(c, CONTENT_X, cap_y, line, "Sans-Light", S_CAPTION, CAPTION)


def slide_8_experiments(c):
    bg(c)
    y = draw_h2(c, "Experiments & Analysis")

    stages = [
        ("Stage 1", "Automated extraction",  "OntoNotes via VerbNet class mapping", None, "Polysemy contamination",    ACCENT),
        ("Stage 2", "Pivot",                 "Inductive scope maps from curated examples", "All 62 scopes defined before any data changes", "Clean boundary definitions", GOLD),
        ("Stage 3", "Synthetic generation",  "Pattern-based, tiered, scope-map-validated", None, "95.9% audit pass rate", GREEN),
    ]
    gap = 30
    col_w = (CONTENT_W - gap * 2) / 3
    top_y = y + 40

    for i, (num, label, brief, sub, result, color) in enumerate(stages):
        sx = CONTENT_X + i * (col_w + gap)
        # Compute needed height
        brief_lines = wrap_text(brief, "Sans", S_BODY, col_w - 48)
        sub_lines = wrap_text(sub, "Sans-Light", S_CAPTION, col_w - 48) if sub else []
        h = (
            24 + line_h(S_BODY)       # stage num
            + line_h(S_BODY)          # label
            + 10 + line_h(S_BODY) * len(brief_lines)
            + (14 + line_h(S_CAPTION) * len(sub_lines) if sub_lines else 0)
            + 20 + line_h(S_BODY)
            + 24
        )
        fill_rect(c, sx, top_y, col_w, h, ROW_ALT)
        iy = top_y + 24
        iy = draw_text(c, sx + 24, iy, num,   "Serif-Bold", S_BODY, HEADING)
        iy = draw_text(c, sx + 24, iy, label, "Sans-Bold",  S_BODY, HEADING)
        iy += 6
        for ln in brief_lines:
            iy = draw_text(c, sx + 24, iy, ln, "Sans", S_BODY, BODY)
        if sub_lines:
            iy += 8
            for ln in sub_lines:
                iy = draw_text(c, sx + 24, iy, ln, "Sans-Light", S_CAPTION, CAPTION)
        iy += 14
        draw_text(c, sx + 24, iy, result, "Sans-Bold", S_BODY, color)

    # Footer caption
    cap = "Methodology: Claude (prompt design) \u2192 Claude Code (execution) \u2192 human validation \u2192 iterate"
    draw_text(c, CONTENT_X, PAGE_H - 130, cap, "Sans-Light", S_CAPTION, CAPTION)


def slide_9_results(c):
    bg(c)
    y = draw_h2(c, "Results")

    # Three callouts at top
    col_w = CONTENT_W / 3
    top_y = y + 20
    callouts = [
        ("94.4%", "Macro F1"),
        ("96.7%", "Constrained Accuracy"),
        ("+5.9pp", "Lift over Random Baseline"),
    ]
    for i, (num, label) in enumerate(callouts):
        cx = CONTENT_X + col_w * i + col_w / 2
        ny = draw_text(c, cx, top_y, num, "Serif-Bold", S_DISPLAY, GREEN, align="center")
        ny = ny - line_h(S_DISPLAY) + S_DISPLAY * 1.1   # correct line-height override
        ny += 16
        draw_text(c, cx, ny, label, "Sans-Bold", S_BODY, HEADING, align="center")

    # Three tables in grid
    tables_y = top_y + S_DISPLAY * 1.1 + 60 + 24
    gap = 40
    t_w = (CONTENT_W - gap * 2) / 3

    tables = [
        [("Accuracy", "0.953"),
         ("Precision", "0.944"),
         ("Recall", "0.944"),
         ("F1 (macro)", "0.944"),
         ("F1 (weighted)", "0.953")],
        [("T1  hard negatives", "94.4%"),
         ("T2  medium", "97.4%"),
         ("T3  easy", "93.0%")],
        [("Corpus F1", "0.91"),
         ("Synthetic F1", "0.97"),
         ("All 62 Situations", "above 0.70")],
    ]
    row_h = line_h(S_BODY) + 6
    for i, tbl in enumerate(tables):
        tx = CONTENT_X + i * (t_w + gap)
        for j, (lab, val) in enumerate(tbl):
            ry = tables_y + j * row_h
            if j % 2 == 1:
                fill_rect(c, tx, ry, t_w, row_h, ROW_ALT)
            draw_text(c, tx + 14, ry + 6, lab, "Sans", S_BODY, BODY)
            draw_text(c, tx + t_w - 14, ry + 6, val, "Sans-Bold", S_BODY, GREEN, align="right")


def demo_card(c, y_top, sentence, verb, candidates, caption):
    """Render a demo card with score bars. candidates: [(name, prob)]."""
    card_w = 1000
    card_x = (PAGE_W - card_w) / 2
    pad_x, pad_y = 52, 42
    # compute card height
    n = len(candidates)
    header_h = line_h(S_CAPTION) + 28
    input_h = line_h(S_BODY) + 30
    verb_h  = line_h(S_CAPTION) + 20
    bars_h  = n * (28 + 10)
    card_h = pad_y * 2 + header_h + input_h + verb_h + bars_h

    fill_rect(c, card_x, y_top, card_w, card_h, WHITE)
    stroke_rect(c, card_x, y_top, card_w, card_h, HexColor("#E8E8E8"), lw=1)

    iy = y_top + pad_y
    # Header (uppercase)
    header = "ASC Classifier \u00B7 Event Structure Disambiguation"
    draw_text(c, card_x + pad_x, iy, header.upper(), "Sans-Bold", S_CAPTION, HEADING)
    iy += line_h(S_CAPTION) + 28

    # Input with bottom rule
    draw_text(c, card_x + pad_x, iy, sentence, "Sans", S_BODY, BODY)
    iy += line_h(S_BODY) + 6
    # rule below input
    c.setStrokeColor(HEADING); c.setLineWidth(2)
    c.line(card_x + pad_x, ytop(iy), card_x + card_w - pad_x, ytop(iy))
    iy += 22

    # Verb + candidate count
    verb_line = f"verb:  {verb}  \u00B7  {len(candidates)} candidate{'' if len(candidates) == 1 else 's'}"
    # Draw with "verb:" and count in caption gray; verb itself in heading
    c.setFont("Sans-Light", S_CAPTION)
    c.setFillColor(CAPTION)
    base = ytop(iy + ascent("Sans-Light", S_CAPTION))
    pre = "verb:  "
    c.drawString(card_x + pad_x, base, pre)
    x2 = card_x + pad_x + stringWidth(pre, "Sans-Light", S_CAPTION)
    c.setFont("Sans-Bold", S_CAPTION); c.setFillColor(HEADING)
    c.drawString(x2, base, verb)
    x3 = x2 + stringWidth(verb, "Sans-Bold", S_CAPTION)
    suffix = f"  \u00B7  {len(candidates)} candidate{'' if len(candidates) == 1 else 's'}"
    c.setFont("Sans-Light", S_CAPTION); c.setFillColor(CAPTION)
    c.drawString(x3, base, suffix)
    iy += line_h(S_CAPTION) + 20

    # Score bars
    name_w = 300
    track_x = card_x + pad_x + name_w + 18
    track_w = card_w - 2 * pad_x - name_w - 18 - 90
    for name, prob in candidates:
        bar_y = iy
        # Name (right-aligned within the name column, matches demo)
        draw_text(c, card_x + pad_x + name_w, bar_y + 2, name, "Sans", S_BODY, BODY, align="right")
        # Track
        fill_rect(c, track_x, bar_y, track_w, 28, GRAY_LIGHT)
        # Fill (green proportional)
        fill_rect(c, track_x, bar_y, track_w * prob, 28, GREEN)
        # Value on right
        draw_text(c, card_x + card_w - pad_x, bar_y + 4,
                  f"{prob:.3f}", "Sans-Bold", S_CAPTION, HEADING, align="right")
        iy += 28 + 10

    # Caption below card
    cap_y = y_top + card_h + 40
    draw_paragraph(c, CONTENT_X, cap_y, caption, "Sans-Light", S_CAPTION, CAPTION, CONTENT_W)


def slide_10_demo_capacity(c):
    bg(c)
    y = draw_h2(c, "Demo: Capacity")
    demo_card(c, y + 40,
              "The old barn holds about forty head of cattle.",
              "hold",
              [("Capacity", 0.994)],
              "\u201Chold\u201D \u2192 Capacity: the barn has capacity for a given quantity of cattle.")


def slide_11_demo_emotion(c):
    bg(c)
    y = draw_h2(c, "Demo: Emotion (stim. subj.)")
    demo_card(c, y + 40,
              "The news worried the investors.",
              "worry",
              [("Emotion (stim. subj.)", 0.995),
               ("Emotion (exp. subj.)", 0.112)],
              "\u201Cworry\u201D \u2192 stimulus-subject (not experiencer-subject). The news causes the emotion; the investors undergo it.")


def slide_12_demo_intention(c):
    bg(c)
    y = draw_h2(c, "Demo: Intention")
    demo_card(c, y + 40,
              "She looked for her keys everywhere.",
              "look",
              [("Intention", 0.991),
               ("Perception (exp. subj.)", 0.087),
               ("Pursuit", 0.034)],
              "\u201Clook for\u201D \u2192 Intention (not Perception). Directed effort toward an unrealized goal \u2014 same contrast as Slide 2.")


def slide_13_challenges(c):
    bg(c)
    y = draw_h2(c, "Challenges & Lessons")

    items = [
        ("1", "Scale vs. quality", [
            "62 Situations, thousands of examples, limited time.",
            "Hybrid approach: curated seeds \u2192 synthetic generation."]),
        ("2", "Scope discipline", [
            "Constant temptation to expand or refine boundaries.",
            "All scopes must be learned in one phase before proceeding."]),
        ("3", "Methodology coherence", [
            "Same tiered design for positives and negatives, across",
            "extraction, generation, and validation."]),
    ]
    cy = y + 40
    num_col_w = 80
    for num, title, body_lines in items:
        # Number
        c.setFont("Serif-Bold", S_BODY)
        c.setFillColor(ACCENT)
        base = ytop(cy + ascent("Serif-Bold", S_BODY))
        c.drawString(CONTENT_X, base, num)
        # Title
        text_x = CONTENT_X + num_col_w
        ty = draw_text(c, text_x, cy, title, "Sans-Bold", S_BODY, HEADING)
        ty += 6
        for ln in body_lines:
            ty = draw_text(c, text_x, ty, ln, "Sans", S_BODY, BODY)
        cy = ty + 34


def _draw_closing_body(c, start_y, paragraphs, size=S_BODY * 1.3, arrow_para_idx=None):
    """Center closing-style body paragraphs on a dark slide."""
    cy = start_y
    para_spacing = size * 1.0
    for i, para in enumerate(paragraphs):
        # paragraphs is list of lines (each line rendered as-is, centered)
        if isinstance(para, str):
            lines = [para]
        else:
            lines = para
        for ln in lines:
            # Build with possible dark-accent inline arrows indicated by "→"
            if "\u2192" in ln:
                # Split by arrows and draw with dark-accent color on arrows
                parts = ln.split("\u2192")
                # measure total width
                widths = []
                total_w = 0
                for j, p in enumerate(parts):
                    w = stringWidth(p, "Serif", size)
                    widths.append(w)
                    total_w += w
                    if j != len(parts) - 1:
                        total_w += stringWidth(" \u2192 ", "Serif", size)
                xcur = PAGE_W / 2 - total_w / 2
                base = ytop(cy + ascent("Serif", size))
                c.setFont("Serif", size)
                for j, p in enumerate(parts):
                    c.setFillColor(DARK_TEXT)
                    c.drawString(xcur, base, p)
                    xcur += widths[j]
                    if j != len(parts) - 1:
                        c.setFillColor(DARK_ACCENT)
                        c.drawString(xcur, base, " \u2192 ")
                        xcur += stringWidth(" \u2192 ", "Serif", size)
                cy += size * 1.5
            else:
                # centered plain line
                c.setFont("Serif", size)
                c.setFillColor(DARK_TEXT)
                base = ytop(cy + ascent("Serif", size))
                c.drawCentredString(PAGE_W / 2, base, ln)
                cy += size * 1.5
        # Extra spacing between paragraphs (but less after last)
        if i != len(paragraphs) - 1:
            cy += para_spacing
    return cy


def slide_14_conclusion(c):
    bg(c, dark=True)
    # Header
    header_size = S_TITLE
    # Vertically center the whole block
    body_size = int(S_BODY * 1.3)
    lines = [
        "A fine-tuned cross-encoder can learn how to distinguish",
        "among verbal clause constructions,",
        "but only when the training data is built with sufficient",
        "quantity, quality, and balanced difficulty tiers across",
        "the full set of constructions simultaneously.",
    ]
    total_h = line_h(header_size) + 30 + body_size * 1.5 * len(lines)
    start = (PAGE_H - total_h) / 2
    # Header
    c.setFont("Serif-Bold", header_size)
    c.setFillColor(DARK_ACCENT)
    base = ytop(start + ascent("Serif-Bold", header_size))
    c.drawCentredString(PAGE_W / 2, base, "Conclusion")
    start += line_h(header_size) + 30
    for ln in lines:
        c.setFont("Serif", body_size)
        c.setFillColor(DARK_TEXT)
        b = ytop(start + ascent("Serif", body_size))
        c.drawCentredString(PAGE_W / 2, b, ln)
        start += body_size * 1.5


def slide_15_future(c):
    bg(c, dark=True)
    header_size = S_TITLE
    body_size = int(S_BODY * 1.3)
    para1 = [
        "Document understanding broken down",
        "into classification tasks",
        "by divide and conquer approach:",
    ]
    arrow_line = "discourse \u2192 predication \u2192 reference \u2192 modification"
    para3 = [
        "Classify each functional and formal parameter",
        "as fully interpretable features,",
        "one dimension at a time.",
    ]
    block_spacing = body_size * 1.5
    total_h = (line_h(header_size) + 30
               + body_size * 1.5 * len(para1)
               + block_spacing  # gap around arrow line
               + body_size * 1.5
               + block_spacing
               + body_size * 1.5 * len(para3))
    start = (PAGE_H - total_h) / 2

    c.setFont("Serif-Bold", header_size)
    c.setFillColor(DARK_ACCENT)
    base = ytop(start + ascent("Serif-Bold", header_size))
    c.drawCentredString(PAGE_W / 2, base, "Future Work")
    start += line_h(header_size) + 30

    for ln in para1:
        c.setFont("Serif", body_size)
        c.setFillColor(DARK_TEXT)
        b = ytop(start + ascent("Serif", body_size))
        c.drawCentredString(PAGE_W / 2, b, ln)
        start += body_size * 1.5

    start += block_spacing

    # Arrow line — inline arrows in dark-accent color
    parts = arrow_line.split(" \u2192 ")
    # widths
    widths = [stringWidth(p, "Serif", body_size) for p in parts]
    sep = " \u2192 "
    sep_w = stringWidth(sep, "Serif", body_size)
    total_w = sum(widths) + sep_w * (len(parts) - 1)
    xcur = PAGE_W / 2 - total_w / 2
    base = ytop(start + ascent("Serif", body_size))
    for j, p in enumerate(parts):
        c.setFont("Serif", body_size); c.setFillColor(DARK_TEXT)
        c.drawString(xcur, base, p)
        xcur += widths[j]
        if j != len(parts) - 1:
            c.setFillColor(DARK_ACCENT)
            c.drawString(xcur, base, sep)
            xcur += sep_w
    start += body_size * 1.5

    start += block_spacing

    for ln in para3:
        c.setFont("Serif", body_size)
        c.setFillColor(DARK_TEXT)
        b = ytop(start + ascent("Serif", body_size))
        c.drawCentredString(PAGE_W / 2, b, ln)
        start += body_size * 1.5


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
def build():
    c = canvas.Canvas(OUT_PATH, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Fine-Tuning a Bidirectional Cross-Encoder for Verbal Clause Construction Classification")
    c.setAuthor("Josh Falconer")

    slides = [
        slide_1_title, slide_2_problem, slide_3_motivation,
        slide_4a_dataset_flow, slide_4b_dataset_pairs,
        slide_5_theory, slide_6_tiers, slide_7_pipeline,
        slide_8_experiments, slide_9_results,
        slide_10_demo_capacity, slide_11_demo_emotion, slide_12_demo_intention,
        slide_13_challenges, slide_14_conclusion, slide_15_future,
    ]
    for fn in slides:
        fn(c)
        c.showPage()

    c.save()
    print(f"Wrote {OUT_PATH}")

if __name__ == "__main__":
    build()
