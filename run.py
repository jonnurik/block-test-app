import sys
from PyQt5.QtWidgets import (
    QApplication, QFileDialog, QMessageBox, QTableWidgetItem
)

from ui import MainUI
from db import (
    init_db,
    get_questions,
    get_stats_filtered,
    update_question,
    delete_question,
    clear_questions
)
from importer import import_json
from generator import generate_block
from pdfgen import generate_pdf
from edit_dialog import EditDialog


init_db()
app = QApplication(sys.argv)
ui = MainUI()


# =====================
# JADVAL + STATISTIKA
# =====================
def refresh():
    subject = ui.fan_select.currentText()
    block = ui.block_type.currentText()

    count = get_stats_filtered(subject, block)
    ui.stats.setText(f"{subject} [{block}]: {count} ta")

    rows = get_questions(subject, block)
    ui.table.setRowCount(len(rows))

    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ui.table.setItem(r, c, QTableWidgetItem(str(val)))


# =====================
# IMPORT
# =====================
def handle_import():
    path, _ = QFileDialog.getOpenFileName(
        ui, "JSON tanlang", "", "JSON (*.json)"
    )
    if not path:
        return

    subject = ui.fan_select.currentText()
    block = ui.block_type.currentText()

    import_json(path, subject, block)
    refresh()


# =====================
# TOZALASH
# =====================
def handle_clear():
    subject = ui.fan_select.currentText()
    block = ui.block_type.currentText()

    if QMessageBox.question(
        ui,
        "Tasdiqlash",
        f"{subject} [{block}] tozalanadi. Davom etasizmi?",
        QMessageBox.Yes | QMessageBox.No
    ) == QMessageBox.Yes:
        clear_questions(subject, block)
        refresh()


# =====================
# O‘CHIRISH
# =====================
def handle_delete():
    r = ui.table.currentRow()
    if r < 0:
        return
    qid = int(ui.table.item(r, 0).text())
    delete_question(qid)
    refresh()


# =====================
# TAHRIRLASH
# =====================
def handle_edit():
    r = ui.table.currentRow()
    if r < 0:
        return

    qid = int(ui.table.item(r, 0).text())

    dlg = EditDialog({
        "q": ui.table.item(r, 1).text(),
        "A": ui.table.item(r, 2).text(),
        "B": ui.table.item(r, 3).text(),
        "C": ui.table.item(r, 4).text(),
        "D": ui.table.item(r, 5).text(),
        "correct": ui.table.item(r, 6).text(),
        "difficulty": ui.table.item(r, 7).text()
    }, ui)

    if dlg.exec_():
        d = dlg.result_data()
        update_question(
            qid, d["q"], d["A"], d["B"], d["C"],
            d["D"], d["correct"], d["difficulty"]
        )
        refresh()


# =====================
# PDF
# =====================
def handle_pdf():
    a1 = ui.asosiy1.currentText()
    a2 = ui.asosiy2.currentText()

    blocks = [
        ("Ona tili", generate_block("Ona tili", "majburiy", 10)),
        ("Matematika", generate_block("Matematika", "majburiy", 10)),
        ("Tarix", generate_block("Tarix", "majburiy", 10)),
        (a1, generate_block(a1, "asosiy", 30)),
        (a2, generate_block(a2, "asosiy", 30)),
    ]

    path, _ = QFileDialog.getSaveFileName(
        ui, "PDF saqlash", "blok_test.pdf", "PDF (*.pdf)"
    )
    if path:
        generate_pdf(path, blocks)


# =====================
# SIGNAL
# =====================
ui.btn_import.clicked.connect(handle_import)
ui.btn_clear.clicked.connect(handle_clear)
ui.btn_delete.clicked.connect(handle_delete)
ui.btn_edit.clicked.connect(handle_edit)
ui.btn_pdf.clicked.connect(handle_pdf)

ui.fan_select.currentIndexChanged.connect(refresh)
ui.block_type.currentIndexChanged.connect(refresh)

refresh()
ui.show()
sys.exit(app.exec_())
