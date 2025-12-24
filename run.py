import sys
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QTableWidgetItem
)

from ui import MainUI
from db import (
    init_db, get_stats, get_questions_by_subject,
    update_question, delete_question
)
from importer import import_json
from generator import generate_block
from pdfgen import generate_pdf

init_db()

app = QApplication(sys.argv)
ui = MainUI()

def refresh_stats():
    rows = get_stats()
    text = ""
    for s, b, c in rows:
        text += f"{s} [{b}]: {c} ta\n"
    ui.stats.setText(text or "Bazaga savol kiritilmagan")
    load_questions()

def load_questions():
    subject = ui.fan_select.currentText()
    rows = get_questions_by_subject(subject)
    ui.table.setRowCount(len(rows))
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ui.table.setItem(r, c, QTableWidgetItem(str(val)))

def handle_import():
    path, _ = QFileDialog.getOpenFileName(ui, "JSON tanlang", "", "JSON (*.json)")
    if not path:
        return
    added = import_json(path, ui.fan_select.currentText(), ui.block_type.currentText())
    QMessageBox.information(ui, "Import", f"{added} ta savol qo‘shildi")
    refresh_stats()

def handle_delete():
    row = ui.table.currentRow()
    if row >= 0:
        delete_question(int(ui.table.item(row, 0).text()))
        refresh_stats()

def handle_edit():
    row = ui.table.currentRow()
    if row < 0:
        return
    qid = int(ui.table.item(row, 0).text())
    text, ok = QInputDialog.getText(ui, "Tahrirlash", "Savol:", text=ui.table.item(row,1).text())
    if ok:
        update_question(
            qid, text,
            ui.table.item(row,2).text(),
            ui.table.item(row,3).text(),
            ui.table.item(row,4).text(),
            ui.table.item(row,5).text(),
            ui.table.item(row,6).text()
        )
        refresh_stats()

def handle_generate():
    a1, a2 = ui.asosiy1.currentText(), ui.asosiy2.currentText()
    if a1 == a2:
        QMessageBox.warning(ui, "Xato", "Asosiy fanlar bir xil bo‘lmasin")
        return

    blocks = [
        ("Ona tili", generate_block("Ona tili", "majburiy", 10)),
        ("Matematika", generate_block("Matematika", "majburiy", 10)),
        ("Tarix", generate_block("Tarix", "majburiy", 10)),
        (a1, generate_block(a1, "asosiy", 30)),
        (a2, generate_block(a2, "asosiy", 30)),
    ]

    path, _ = QFileDialog.getSaveFileName(ui, "PDF saqlash", "blok_test.pdf", "PDF (*.pdf)")
    if path:
        generate_pdf(path, blocks)
        QMessageBox.information(ui, "Tayyor", "PDF yaratildi")

ui.btn_import.clicked.connect(handle_import)
ui.btn_delete.clicked.connect(handle_delete)
ui.btn_edit.clicked.connect(handle_edit)
ui.btn_pdf.clicked.connect(handle_generate)
ui.fan_select.currentIndexChanged.connect(load_questions)

refresh_stats()
ui.show()
sys.exit(app.exec_())
