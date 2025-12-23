import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from ui import MainUI
from importer import import_json
from db import get_questions
from pdfgen import generate_pdf

def generate_block(subject, total):
    part = total // 3
    return (
        get_questions(subject, "oson", part) +
        get_questions(subject, "orta", part) +
        get_questions(subject, "qiyin", part)
    )

app = QApplication(sys.argv)
ui = MainUI()

def import_data():
    f, _ = QFileDialog.getOpenFileName(
        ui, "JSON bazani tanlang", "", "JSON (*.json)"
    )
    if f:
        count = import_json(f)
        QMessageBox.information(ui, "OK", f"{count} ta savol import qilindi")

def generate_pdf_file():
    blocks = [
        ("Ona tili (majburiy)", generate_block("Ona tili", 10)),
        ("Matematika (majburiy)", generate_block("Matematika", 10)),
        ("Tarix (majburiy)", generate_block("Tarix", 10)),
        (ui.asosiy1.currentText(), generate_block(ui.asosiy1.currentText(), 30)),
        (ui.asosiy2.currentText(), generate_block(ui.asosiy2.currentText(), 30)),
    ]

    save, _ = QFileDialog.getSaveFileName(
        ui, "PDF saqlash", "block_test.pdf", "PDF (*.pdf)"
    )
    if save:
        generate_pdf(save, "assets/logo.png", blocks)

ui.btn_file.clicked.connect(import_data)
ui.btn_gen.clicked.connect(generate_pdf_file)

ui.show()
sys.exit(app.exec_())
