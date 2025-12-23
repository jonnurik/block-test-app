from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(path, logo, blocks):
    c = canvas.Canvas(path, pagesize=A4)
    W, H = A4

    if logo:
        c.drawImage(logo, 70*mm, H-40*mm, width=60*mm, preserveAspectRatio=True)

    c.setFont("Times-Bold", 24)
    c.drawCentredString(W/2, H-70*mm, "TEST TOPSHIRIQLARI KITOBI")
    c.showPage()

    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    y_top = H - 30*mm
    y_bottom = 30*mm
    qnum = 1

    for title, items in blocks:
        c.setFont("Times-Bold", 14)
        c.drawString(20*mm, y_top, title)
        y = y_top - 10*mm

        for q in items:
            if y < y_bottom:
                c.showPage()
                c.setFont("Times-Bold", 14)
                c.drawString(20*mm, y_top, title)
                y = y_top - 10*mm

            p = Paragraph(f"{qnum}. {q['q']}", normal)
            w, h = p.wrap(170*mm, y)
            p.drawOn(c, 20*mm, y-h)
            y -= h + 4*mm

            for opt in ["A","B","C","D"]:
                c.drawString(30*mm, y, f"{opt}) {q[opt]}")
                y -= 6*mm

            y -= 4*mm
            qnum += 1

        c.showPage()

    c.save()
