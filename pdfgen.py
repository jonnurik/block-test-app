from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def _center_text(c, text, y, fontname='Times-Roman', fontsize=16):
    width = c._pagesize[0]
    c.setFont(fontname, fontsize)
    text_width = c.stringWidth(text, fontname, fontsize)
    c.drawString((width - text_width)/2.0, y, text)

def generate_block_pdf(output_path: str, structure, shuffle_options=False, logo_path='assets/logo.png', book_number=None):
    """
    Create cover-like PDF similar to sample.

    - output_path: full path to save PDF
    - structure: ordered list of tuples [(subject, count), ...]  e.g.
                 [("Ona tili",10), ("O'zbekiston tarixi",10), ("Matematika",10), ("Biologiya",30), ("Kimyo",30)]
                 (first 3 usually mandatory)
    - shuffle_options: unused here but kept for compatibility
    - logo_path: path to logo image (optional)
    - book_number: string (if None we generate timestamp-based)
    """

    if book_number is None:
        book_number = datetime.now().strftime("%Y%m%d%H%M")

    # Page setup
    PAGE_WIDTH, PAGE_HEIGHT = A4
    margin = 20 * mm

    c = canvas.Canvas(output_path, pagesize=A4)

    # --- Logo (top center) ---
    y = PAGE_HEIGHT - margin - 40*mm
    if logo_path and os.path.exists(logo_path):
        # draw image centered, scale to max width
        max_logo_w = 60*mm
        max_logo_h = 40*mm
        try:
            from PIL import Image
            img = Image.open(logo_path)
            iw, ih = img.size
            scale = min(max_logo_w/iw, max_logo_h/ih, 1.0)
            iw_scaled = iw * scale
            ih_scaled = ih * scale
            c.drawImage(logo_path, (PAGE_WIDTH - iw_scaled)/2.0, y, width=iw_scaled, height=ih_scaled, mask='auto')
        except Exception:
            # fallback: draw image without scaling logic
            c.drawImage(logo_path, (PAGE_WIDTH - max_logo_w)/2.0, y, width=max_logo_w, height=max_logo_h, mask='auto')
    y -= 50*mm

    # --- Book number box (thin rectangle across) ---
    box_h = 12*mm
    box_w = PAGE_WIDTH - 2*margin
    box_x = margin
    box_y = PAGE_HEIGHT - margin - (20*mm)
    c.setLineWidth(1)
    c.rect(box_x, box_y, box_w, box_h, stroke=1, fill=0)
    # left small cell blank and centered "KITOB RAQAMI: <num> TIP: 001001"
    text = f"KITOB RAQAMI: {book_number}    TIP: 001001"
    c.setFont("Times-Bold", 12)
    c.drawCentredString(box_x + box_w/2.0, box_y + box_h/2.0 - 4, text)

    # --- Main title centered ---
    y_title = box_y - 50*mm
    c.setFont("Times-Bold", 26)
    _center_text(c, "TEST TOPSHIRIQ LARI", y_title, fontname="Times-Bold", fontsize=28)
    _center_text(c, "KITOBI", y_title - 18, fontname="Times-Bold", fontsize=28)

    # --- Blocks list: show ranges and subject (left aligned slightly centered) ---
    # compute ranges
    start = 1
    lines = []
    for subj, cnt in structure:
        end = start + cnt - 1
        range_text = f"{start}-{end} topshiriqlar"
        lines.append((range_text, subj))
        start = end + 1

    # place the lines centered horizontally but with two columns: left range, right subject aligned right-of-range
    list_y_start = y_title - 70
    line_gap = 14
    c.setFont("Times-Roman", 12)
    # place lines in center column block
    col_x = PAGE_WIDTH/2.0 - 60*mm
    for i, (rtext, subj) in enumerate(lines):
        y_line = list_y_start - i * line_gap
        # left (range)
        c.drawString(col_x, y_line, rtext)
        # right (subject) with parentheses and numeric code if you want
        subj_display = subj
        c.drawString(col_x + 80*mm, y_line, subj_display)

    # --- Note box (bottom-left) ---
    note_box_w = 80*mm
    note_box_h = 50*mm
    note_x = margin
    note_y = margin + 40*mm
    c.rect(note_x, note_y, note_box_w, note_box_h, stroke=1, fill=0)
    c.setFont("Times-Bold", 10)
    c.drawString(note_x + 6, note_y + note_box_h - 12, "ABITURIYENT DIQQATIGA!")
    # list inside
    c.setFont("Times-Roman", 9)
    notes = [
        "1. Ushbu kitob va javoblar varaqasi",
        "   raqamlarni mosligini tekshiring.",
        "2. Har bir majburiy fandan 10 tadan,",
        "   mutaxassislik fanlardan 30 tadan test",
        "   topshiriqlari mavjudligini tekshiring.",
        "3. Nuqsonlar aniqlanganda, darhol guruh",
        "   nazoratchisiga ma'lum qiling.",
        "4. Kitob muqovasiga o'zingiz haqingizdagi",
        "   ma'lumotlarni yozing va imzo qo'ying."
    ]
    ty = note_y + note_box_h - 26
    for n in notes:
        c.drawString(note_x + 6, ty, n)
        ty -= 10

    # --- signature line (right side) ---
    sig_x = PAGE_WIDTH - margin - 60*mm
    sig_y = note_y + 8
    c.setFont("Times-Roman", 11)
    c.drawString(sig_x, sig_y + 20, "." * 30)
    c.drawString(sig_x + 10, sig_y - 2, "imzo")

    # finish
    c.showPage()
    c.save()
    return output_path
