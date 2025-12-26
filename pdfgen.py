from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(path, blocks):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 50
    num = 1

    for title, qs in blocks:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, title)
        y -= 30

        c.setFont("Helvetica", 11)
        for q in qs:
            if y < 100:
                c.showPage()
                y = h - 50
            c.drawString(50, y, f"{num}. {q[0]}")
            y -= 15
            for opt in q[1:]:
                c.drawString(70, y, opt)
                y -= 12
            y -= 10
            num += 1

    c.save()
