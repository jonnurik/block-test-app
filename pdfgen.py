from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(path, blocks):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    y = height - 40
    qnum = 1

    for title, questions in blocks:
        c.setFont("Times-Bold", 14)
        c.drawString(40, y, title)
        y -= 25

        c.setFont("Times-Roman", 11)

        for q in questions:
            if y < 80:
                c.showPage()
                y = height - 40

            c.drawString(40, y, f"{qnum}. {q['q']}")
            y -= 18

            for opt in ["A", "B", "C", "D"]:
                c.drawString(60, y, f"{opt}) {q[opt]}")
                y -= 15

            y -= 10
            qnum += 1

        c.showPage()
        y = height - 40

    c.save()
