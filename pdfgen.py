import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Frame, Spacer
from datetime import datetime
from typing import Dict, List, Tuple
from db import get_random_questions
import random

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

def _shuffle_options(qdict: dict) -> Tuple[dict, str]:
    opts = [('A', qdict['a']), ('B', qdict['b']), ('C', qdict['c']), ('D', qdict['d'])]
    random.shuffle(opts)
    mapping = {chr(65+i): opts[i][1] for i in range(4)}
    correct_text = qdict['a'] if qdict['correct'] == 'A' else qdict['b'] if qdict['correct']=='B' else qdict['c'] if qdict['correct']=='C' else qdict['d']
    new_correct = None
    for label, text in mapping.items():
        if text == correct_text:
            new_correct = label
            break
    new_q = {'question': qdict['question'], 'a': mapping['A'], 'b': mapping['B'], 'c': mapping['C'], 'd': mapping['D'], 'correct': new_correct}
    return new_q, new_correct

def generate_block_pdf(output_path: str, subjects_map: Dict[str,int], shuffle_options: bool = True):
    sections = []
    for subj, cnt in subjects_map.items():
        qlist = get_random_questions(subj, cnt)
        if shuffle_options:
            new_qlist = []
            for q in qlist:
                nq, _ = _shuffle_options(q)
                new_qlist.append(nq)
            qlist = new_qlist
        sections.append((subj, qlist))

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    margin = 18 * mm
    usable_width = width - 2*margin
    y_start = height - margin

    normal_style = ParagraphStyle('normal', fontName='Helvetica', fontSize=11, leading=14)
    heading_style = ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=13, leading=16)

    def draw_header_footer():
        if os.path.exists(LOGO_PATH):
            try:
                c.drawImage(LOGO_PATH, margin, height - margin - 20*mm, width=30*mm, preserveAspectRatio=True, mask='auto')
            except Exception:
                pass
        c.setFont("Helvetica", 9)
        c.drawRightString(width - margin, height - margin + 4*mm, f"Sana: {datetime.now().strftime('%Y-%m-%d')}")
        c.setFont("Helvetica", 8)
        c.drawString(margin, margin/2, "Blok test — tayyorlangan dastur tomonidan chiqarildi.")

    def new_page():
        c.showPage()
        draw_header_footer()

    draw_header_footer()
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y_start - 10*mm, "BLOK TEST")
    c.setFont("Helvetica", 11)
    c.drawCentredString(width/2, y_start - 18*mm, "Abituriyentlar uchun — avtomatik generatsiya")
    c.setFont("Helvetica", 10)
    c.drawString(margin, y_start - 28*mm, "Ko'rsatma: Har bir savolga mos A/B/C/D belgilang.")
    new_page()

    qnum = 1
    answer_key = []

    for section_title, qlist in sections:
        story = []
        story.append(Paragraph(f"<b>{section_title}</b>", heading_style))
        story.append(Spacer(1, 4*mm))
        for q in qlist:
            story.append(Paragraph(f"<b>{qnum})</b> {q['question']}", normal_style))
            story.append(Paragraph(f"A) {q['a']}", normal_style))
            story.append(Paragraph(f"B) {q['b']}", normal_style))
            story.append(Paragraph(f"C) {q['c']}", normal_style))
            story.append(Paragraph(f"D) {q['d']}", normal_style))
            story.append(Spacer(1, 3*mm))
            answer_key.append((qnum, q['correct']))
            qnum += 1
        frame = Frame(margin, margin, usable_width, height - 2*margin, showBoundary=0)
        frame.addFromList(story, c)
        new_page()

    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y_start - 10*mm, "Javoblar varaqasi")
    c.setFont("Helvetica", 11)
    x = margin
    y = y_start - 20*mm
    per_row = 6
    col_w = usable_width / per_row
    cnt = 0
    for num, ans in answer_key:
        row = cnt // per_row
        col = cnt % per_row
        tx = margin + col*col_w
        ty = y - row * 8*mm
        c.drawString(tx, ty, f"{num}) {ans}")
        cnt += 1
        if ty < margin + 20*mm:
            new_page()
            y = y_start - 20*mm
            cnt = 0

    c.save()
