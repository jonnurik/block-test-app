import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from ui import MainUI
from importer import load_questions
from pdfgen import generate_pdf

app = QApplication(sys.argv)
ui = MainUI()
data = {}

def choose_file():
    global data
    f, _ = QFileDialog.getOpenFileName(
        ui, "Savollar fayli", "", "CSV/XLSX (*.csv *.xlsx)"
    )
    if f:
        data = load_questions(f)
        QMessageBox.information(ui, "OK", "Savollar muvaffaqiyatli yuklandi")

def generate():
    if not data:
        QMessageBox.warning(ui, "Xato", "Avval savollar faylini tanlang")
        return

    try:
        blocks = [
            ("Ona tili (majburiy)", data["Ona tili"][:10]),
            ("Matematika (majburiy)", data["Matematika"][:10]),
            ("Tarix (majburiy)", data["Tarix"][:10]),
            (ui.asosiy1.currentText(), data[ui.asosiy1.currentText()][:30]),
            (ui.asosiy2.currentText(), data[ui.asosiy2.currentText()][:30]),
        ]
    except KeyError as e:
        QMessageBox.critical(
            ui, "Xato",
            f"Savollar yetishmayapti: {e}"
        )
        return

    save, _ = QFileDialog.getSaveFileName(
        ui, "PDF saqlash", "block_test.pdf", "PDF (*.pdf)"
    )
    if save:
        generate_pdf(save, "assets/logo.png", blocks)
        QMessageBox.information(ui, "Tayyor", "PDF muvaffaqiyatli yaratildi")

ui.btn_file.clicked.connect(choose_file)
ui.btn_gen.clicked.connect(generate)

ui.show()
sys.exit(app.exec_())
