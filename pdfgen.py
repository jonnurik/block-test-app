from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(questions, filename="test.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    y = 800
    num = 1

    for q in questions:
        c.drawString(40, y, f"{num}. {q['question']}")
        y -= 20
        for opt in q["options"]:
            c.drawString(60, y, f"- {opt}")
            y -= 15
        y -= 10
        if y < 100:
            c.showPage()
            y = 800
        num += 1

    c.save()
