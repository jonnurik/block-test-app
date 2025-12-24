from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(path, blocks):
    c = canvas.Canvas(path, pagesize=A4)
    w, h = A4
    y = h - 40
    num = 1

    for title, qs in blocks:
        c.setFont("Times-Bold", 14)
        c.drawString(40, y, title)
        y -= 25
        c.setFont("Times-Roman", 11)

        for q in qs:
            if y < 80:
                c.showPage()
                y = h - 40

            c.drawString(40, y, f"{num}. {q['q']}")
            y -= 18
            for o in ["A", "B", "C", "D"]:
                c.drawString(60, y, f"{o}) {q[o]}")
                y -= 15
            y -= 10
            num += 1

        c.showPage()
        y = h - 40

    c.save()
