# pdfgen.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Paragraph
from reportlab.lib.fonts import addMapping
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import random
import datetime


PAGE_W, PAGE_H = A4
LEFT = 20 * mm
TOP = PAGE_H - 20 * mm
LINE = 7 * mm


def _draw_header(c, title):
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(PAGE_W / 2, TOP, title)
    c.setLineWidth(1)
    c.line(LEFT, TOP - 5, PAGE_W - LEFT, TOP - 5)


def _new_page(c, title):
    c.showPage()
    _draw_header(c, title)
    return TOP - 15


def generate_pdf(
    output_path: str,
    logo_path: str,
    blocks: list
):
    """
    blocks = [
      ("Ona tili (majburiy)", [q1, q2, ...]),
      ("Matematika (majburiy)", [...]),
      ("Tarix (majburiy)", [...]),
      ("Biologiya", [...]),
      ("Kimyo", [...])
    ]

    Har bir q:
    (id, savol, A, B, C, D, togri, qiyinlik)
    """

    c = canvas.Canvas(output_path, pagesize=A4)

    # =========================
    # MUQOVA
    # =========================
    if os.path.exists(logo_path):
        c.drawImage(
            logo_path,
            PAGE_W / 2 - 20 * mm,
            PAGE_H - 45 * mm,
            width=40 * mm,
            height=40 * mm,
            preserveAspectRatio=True
        )

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(
        PAGE_W / 2,
        PAGE_H - 65 * mm,
        "TEST TOPSHIRIQLARI KITOBI"
    )

    c.setFont("Helvetica", 11)
    y = PAGE_H - 85 * mm

    index = 1
    ranges = []
    for title, qs in blocks:
        start = index
        index += len(qs)
        end = index - 1
        ranges.append((start, end, title))

    for start, end, title in ranges:
        c.drawCentredString(
            PAGE_W / 2,
            y,
            f"{start}-{end} topshiriqlar — {title}"
        )
        y -= 7 * mm

    c.setFont("Helvetica", 9)
    c.rect(LEFT, 40 * mm, PAGE_W - 2 * LEFT, 40 * mm)
    c.drawString(LEFT + 5 * mm, 70 * mm, "ABITURIYENT DIQQATIGA!")
    c.drawString(LEFT + 5 * mm, 62 * mm, "1. Har bir savol uchun faqat bitta javob belgilanadi.")
    c.drawString(LEFT + 5 * mm, 55 * mm, "2. Javoblar varaqasiga aniq va to‘g‘ri belgilang.")
    c.drawString(LEFT + 5 * mm, 48 * mm, "3. Savollar sonini tekshirib oling.")

    c.showPage()

    # =========================
    # SAVOLLAR
    # =========================
    page_title = "Test topshiriqlari"
    _draw_header(c, page_title)
    y = TOP - 20

    qnum = 1

    for block_title, questions in blocks:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(LEFT, y, block_title)
        y -= 10

        for q in questions:
            if y < 40 * mm:
                y = _new_page(c, page_title)

            _, text, a, b, c1, d, correct, diff = q

            c.setFont("Helvetica-Bold", 10)
            c.drawString(LEFT, y, f"{qnum}. {text}")
            y -= 7

            c.setFont("Helvetica", 10)
            c.drawString(LEFT + 5 * mm, y, f"A) {a}")
            y -= 6
            c.drawString(LEFT + 5 * mm, y, f"B) {b}")
            y -= 6
            c.drawString(LEFT + 5 * mm, y, f"C) {c1}")
            y -= 6
            c.drawString(LEFT + 5 * mm, y, f"D) {d}")
            y -= 8

            qnum += 1

        y -= 5

    c.save()
