"""PDF export for rendered copyright pages using reportlab."""

from __future__ import annotations

from io import BytesIO

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

MARGIN = 72
LINE_HEIGHT = 16
HEADER_LINE_HEIGHT = 22


def _strip_markup(text: str) -> str:
    """Very light markdown flattening for PDF drawing."""
    for marker in ("### ", "## ", "# "):
        if text.startswith(marker):
            return text[len(marker):]
    return text


def export_pdf(markdown_text: str, output) -> None:
    """Write a simple, print-ready PDF copyright page to a file path or file object."""
    c = canvas.Canvas(output, pagesize=LETTER)
    width, height = LETTER
    y = height - MARGIN

    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN, y, "Copyright Page")
    y -= HEADER_LINE_HEIGHT

    c.setFont("Helvetica", 11)
    for raw_line in markdown_text.splitlines():
        line = _strip_markup(raw_line).strip()
        if not line:
            y -= LINE_HEIGHT * 0.6
            continue
        if y < MARGIN:
            c.showPage()
            c.setFont("Helvetica", 11)
            y = height - MARGIN
        c.drawString(MARGIN, y, line)
        y -= LINE_HEIGHT

    c.showPage()
    c.save()


def export_pdf_bytes(markdown_text: str) -> bytes:
    """Return the rendered copyright page PDF as bytes."""
    buffer = BytesIO()
    export_pdf(markdown_text, buffer)
    return buffer.getvalue()
