import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from ui import MainUI
from db import init_db, get_stats
from importer import import_json
from generator import generate_block
from pdfgen import generate_pdf

init_db()

app = QApplication(sys.argv)
ui = MainUI()

def refresh_stats():
    rows = get_stats()
    text = ""
    for subject, block_type, count in rows:
        text += f"{subject} [{block_type}]: {count} ta savol\n"
    if not text:
        text = "Bazaga hali savollar qo‘shilmagan."
    ui.stats.setText(text)

def handle_import():
    file_path, _ = QFileDialog.getOpenFileName(
        ui, "JSON fayl tanlang", "", "JSON (*.json)"
    )
    if not file_path:
        return

    subject = ui.fan_select.currentText()
    block_type = ui.block_type.currentText()

    added = import_json(file_path, subject, block_type)

    QMessageBox.information(
        ui, "Import yakunlandi",
        f"{subject} ({block_type}) faniga {added} ta savol qo‘shildi"
    )
    refresh_stats()

def handle_generate():
    a1 = ui.asosiy1.currentText()
    a2 = ui.asosiy2.currentText()

    if a1 == a2:
        QMessageBox.warning(ui, "Xato", "Asosiy fanlar bir xil bo‘lmasin")
        return

    blocks = [
        ("Ona tili (majburiy)", generate_block("Ona tili", "majburiy", 10)),
        ("Matematika (majburiy)", generate_block("Matematika", "majburiy", 10)),
        ("Tarix (majburiy)", generate_block("Tarix", "majburiy", 10)),
        (a1, generate_block(a1, "asosiy", 30)),
        (a2, generate_block(a2, "asosiy", 30)),
    ]

    for title, qs in blocks:
        if len(qs) == 0:
            QMessageBox.warning(ui, "Xato", f"{title} fanidan savol yetarli emas")
            return

    save_path, _ = QFileDialog.getSaveFileName(
        ui, "PDF saqlash", "blok_test.pdf", "PDF (*.pdf)"
    )
    if not save_path:
        return

    generate_pdf(save_path, blocks)

    QMessageBox.information(ui, "Tayyor", "PDF muvaffaqiyatli yaratildi")

ui.btn_import.clicked.connect(handle_import)
ui.btn_pdf.clicked.connect(handle_generate)

refresh_stats()
ui.show()
sys.exit(app.exec_())
