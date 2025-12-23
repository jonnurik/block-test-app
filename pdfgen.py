from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

PAGE_BOTTOM = 30 * mm
PAGE_TOP = 30 * mm

def generate_pdf(path, logo, blocks):
    c = canvas.Canvas(path, pagesize=A4)
    W, H = A4

    # ================= MUQOVA =================
    if logo:
        try:
            c.drawImage(logo, 70*mm, H-40*mm, width=60*mm, preserveAspectRatio=True)
        except:
            pass

    c.setFont("Times-Bold", 26)
    c.drawCentredString(W/2, H-70*mm, "TEST TOPSHIRIQLARI")
    c.drawCentredString(W/2, H-85*mm, "KITOBI")

    c.setFont("Times-Roman", 12)
    y = H - 115*mm

    start = 1
    for title, items in blocks:
        end = start + len(items) - 1
        c.drawString(50*mm, y, f"{start}–{end} topshiriqlar")
        c.drawString(100*mm, y, title)
        y -= 8*mm
        start = end + 1

    c.showPage()

    # ================= SAVOLLAR =================
    styles = getSampleStyleSheet()
    normal = styles["Normal"]

    qnum = 1

    for title, items in blocks:
        c.setFont("Times-Bold", 14)
        c.drawString(20*mm, H - PAGE_TOP, title.upper())
        y = H - PAGE_TOP - 10*mm

        for q in items:

            # 🟢 YANGI SAHIFA TEKSHIRUVI
            if y < PAGE_BOTTOM:
                c.showPage()
                c.setFont("Times-Bold", 14)
                c.drawString(20*mm, H - PAGE_TOP, title.upper())
                y = H - PAGE_TOP - 10*mm

            text = f"{qnum}. {q['q']}"
            p = Paragraph(text, normal)
            w, h = p.wrap(170*mm, y)
            p.drawOn(c, 20*mm, y - h)
            y -= h + 4*mm

            for opt in ["A", "B", "C", "D"]:
                if y < PAGE_BOTTOM:
                    c.showPage()
                    c.setFont("Times-Bold", 14)
                    c.drawString(20*mm, H - PAGE_TOP, title.upper())
                    y = H - PAGE_TOP - 10*mm

                c.setFont("Times-Roman", 12)
                c.drawString(30*mm, y, f"{opt}) {q[opt]}")
                y -= 6*mm

            y -= 4*mm
            qnum += 1

        c.showPage()

    c.save()
