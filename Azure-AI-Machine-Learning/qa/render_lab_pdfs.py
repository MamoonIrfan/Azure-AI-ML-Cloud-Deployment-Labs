"""Render every lab README.md into a PDF handout beside it.

Run from anywhere:  uv run --with reportlab python "week 7 and 8 - azure/week 8/labs/qa/render_lab_pdfs.py"
"""

from html import escape
from pathlib import Path
import re
import textwrap

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    HRFlowable, KeepTogether, Paragraph, Preformatted, SimpleDocTemplate, Spacer, Table, TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
MARGIN = 56
WIDTH = A4[0] - 2 * MARGIN
BLUE = colors.HexColor("#2E74B5")
TEXT = colors.HexColor("#1F1F1F")
RULE = colors.HexColor("#D0D7DE")
FOOTER = "Week 8 — Azure AI and Machine Learning Labs"

body = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5, textColor=TEXT, spaceAfter=6)
title = ParagraphStyle("title", parent=body, fontSize=20, leading=25, textColor=BLUE, spaceAfter=10)
heading = ParagraphStyle("heading", parent=body, fontSize=13.5, leading=18, textColor=BLUE,
                         spaceBefore=4, spaceAfter=6, keepWithNext=True)
subheading = ParagraphStyle("subheading", parent=heading, fontSize=11.5, spaceBefore=6)
item = ParagraphStyle("item", parent=body, leftIndent=18, bulletIndent=2, spaceAfter=4)
subitem = ParagraphStyle("subitem", parent=item, leftIndent=34, bulletIndent=22, spaceAfter=2)
note = ParagraphStyle("note", parent=body, leftIndent=10, borderPadding=(6, 8, 6, 8),
                      backColor=colors.HexColor("#EEF5FB"), borderColor=BLUE, borderWidth=0,
                      spaceBefore=4, spaceAfter=10)
cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=12, spaceAfter=0)
header_cell = ParagraphStyle("header_cell", parent=cell, fontName="Helvetica-Bold")
code = ParagraphStyle("code", fontName="Courier", fontSize=8.5, leading=11, textColor=TEXT,
                      backColor=colors.HexColor("#F3F5F7"), borderPadding=6, spaceBefore=4, spaceAfter=10)


def check(text):
    # Base-14 fonts only cover cp1252; fail loudly instead of printing empty boxes.
    bad = {c for c in text if c not in "—–’“”•" and ord(c) > 255}
    assert not bad, f"Characters Helvetica cannot draw: {bad} in: {text}"
    return text


def inline(text):
    text = escape(check(text), quote=False)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                  lambda m: f'<link href="{m[2]}" color="#2E74B5">{m[1]}</link>' if m[2].startswith("http") else m[1],
                  text)
    text = re.sub(r"`([^`]+)`", r'<font name="Courier" size="9">\1</font>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<i>\1</i>", text)
    return text


def table(lines):
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not all(re.fullmatch(r":?-+:?", c) for c in cells):
            rows.append(cells)
    count = len(rows[0])
    assert all(len(r) == count for r in rows), f"Malformed table near: {lines[0]}"
    # Each column fits its longest word; the remaining width goes to the wordier columns.
    plain = [[re.sub(r"[`*]|\]\([^)]*\)", "", c) for c in r] for r in rows]
    minimum = [max(len(w) for r in plain for w in r[i].split() or [""]) * 5.6 + 16 for i in range(count)]
    weights = [max(8, *(len(r[i]) for r in plain)) ** 0.7 for i in range(count)]
    spare = max(WIDTH - sum(minimum), 0)
    widths = [m + spare * w / sum(weights) for m, w in zip(minimum, weights)]
    data = [[Paragraph(inline(c), header_cell if n == 0 else cell) for c in r] for n, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF4")),
        ("GRID", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [t, Spacer(1, 8)]


def blocks(markdown):
    lines = markdown.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped == "---":
            i += 1
        elif line.startswith("```"):
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            wrapped = [part for raw in lines[i + 1:j] for part in (textwrap.wrap(check(raw), 92, subsequent_indent="  ") or [""])]
            out.append(Preformatted("\n".join(wrapped), code))
            i = j + 1
        elif line.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            out += table(lines[i:j])
            i = j
        else:
            if line.startswith("# "):
                out.append(Paragraph(inline(line[2:]), title))
            elif line.startswith("## "):
                out += [Spacer(1, 6), HRFlowable(width="100%", thickness=0.6, color=RULE, spaceAfter=8),
                        Paragraph(inline(line[3:]), heading)]
            elif line.startswith("### "):
                out.append(Paragraph(inline(line[4:]), subheading))
            elif re.match(r"^\s{2,}(-|\d+\.) ", line):
                marker, text = stripped.split(" ", 1)
                out.append(Paragraph(inline(text), subitem, bulletText="–" if marker == "-" else marker))
            elif re.match(r"^(-|\d+\.) ", line):
                marker, text = line.split(" ", 1)
                out.append(Paragraph(inline(text), item, bulletText="•" if marker == "-" else marker))
            elif line.startswith("> "):
                quote = [line[2:]]
                while i + 1 < len(lines) and lines[i + 1].startswith("> "):
                    i += 1
                    quote.append(lines[i][2:])
                out.append(Paragraph(inline(" ".join(quote)), note))
            else:
                para = [stripped]
                while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"^(#|\||```|> |\s*(-|\d+\.) )", lines[i + 1]):
                    i += 1
                    para.append(lines[i].strip())
                out.append(Paragraph(inline(" ".join(para)), body))
            i += 1
    return out


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.line(MARGIN, 40, A4[0] - MARGIN, 40)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6A737D"))
    canvas.drawString(MARGIN, 28, FOOTER)
    canvas.drawRightString(A4[0] - MARGIN, 28, f"Page {doc.page}")
    canvas.restoreState()


def render(readme, output):
    text = readme.read_text(encoding="utf-8")
    doc_title = text.splitlines()[0].lstrip("# ").strip()
    doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=50, bottomMargin=56, title=doc_title, author="NIAI",
                            subject="Week 8 Azure AI and Machine Learning Lab")
    doc.build(blocks(text), onFirstPage=footer, onLaterPages=footer)
    print(output.relative_to(ROOT))


def main():
    render(ROOT / "README.md", ROOT / "README.pdf")
    labs = sorted(ROOT.glob("lab-*/README.md"))
    for readme in labs:
        render(readme, readme.parent / f"{readme.parent.name}.pdf")


if __name__ == "__main__":
    main()
