import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from ui import MainUI
from importer import import_json
from generator import generate_block
from db import count_by_subject
from pdfgen import generate_pdf

app = QApplication(sys.argv)
ui = MainUI()

def refresh_stats():
    data = count_by_subject()
    text = ""
    for k, v in data.items():
        text += f"{k}: {v} ta savol\n"
    ui.stats.setText(text)

def import_data():
    f, _ = QFileDialog.getOpenFileName(ui, "JSON tanlang", "", "JSON (*.json)")
    if f:
        fan = ui.fan_select.currentText()
        n = import_json(f, fan)
        QMessageBox.information(ui, "OK", f"{fan} uchun {n} ta savol qo‘shildi")
        refresh_stats()

def generate_pdf_file():
    blocks = [
        ("Ona tili (majburiy)", generate_block("Ona tili", 10)),
        ("Matematika (majburiy)", generate_block("Matematika", 10)),
        ("Tarix (majburiy)", generate_block("Tarix", 10)),
        (ui.asosiy1.currentText(), generate_block(ui.asosiy1.currentText(), 30)),
        (ui.asosiy2.currentText(), generate_block(ui.asosiy2.currentText(), 30)),
    ]

    save, _ = QFileDialog.getSaveFileName(ui, "PDF saqlash", "block_test.pdf", "PDF (*.pdf)")
    if save:
        generate_pdf(save, "assets/logo.png", blocks)

ui.btn_import.clicked.connect(import_data)
ui.btn_pdf.clicked.connect(generate_pdf_file)

ui.show()
refresh_stats()
sys.exit(app.exec_())
