import sys
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox,
    QTableWidgetItem
)

from ui import MainUI
from db import (
    init_db,
    get_stats,
    get_questions_by_subject,
    update_question,
    delete_question
)
from importer import import_json
from generator import generate_block
from pdfgen import generate_pdf
from edit_dialog import EditDialog


# =====================
# BAZANI ISHGA TUSHIRISH
# =====================
init_db()


# =====================
# APP + UI
# =====================
app = QApplication(sys.argv)
ui = MainUI()


# =====================
# JADVALGA SAVOLLARNI YUKLASH
# =====================
def load_questions():
    subject = ui.fan_select.currentText()
    rows = get_questions_by_subject(subject)

    ui.table.setRowCount(len(rows))

    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ui.table.setItem(r, c, QTableWidgetItem(str(val)))


# =====================
# STATISTIKANI YANGILASH
# =====================
def refresh_stats():
    rows = get_stats()
    text = ""

    for subject, block_type, count in rows:
        text += f"{subject} [{block_type}]: {count} ta\n"

    if not text:
        text = "Bazaga hali savollar kiritilmagan."

    ui.stats.setText(text)
    load_questions()


# =====================
# JSON IMPORT
# =====================
def handle_edit():
    row = ui.table.currentRow()
    if row < 0:
        return

    qid = int(ui.table.item(row, 0).text())

    data = {
        "q": ui.table.item(row, 1).text(),
        "A": ui.table.item(row, 2).text(),
        "B": ui.table.item(row, 3).text(),
        "C": ui.table.item(row, 4).text(),
        "D": ui.table.item(row, 5).text(),
        "correct": ui.table.item(row, 6).text(),
        "difficulty": ui.table.item(row, 7).text()
    }

    dlg = EditDialog(data, ui)
    if dlg.exec_():
        r = dlg.result_data()
        update_question(
            qid,
            r["q"],
            r["A"],
            r["B"],
            r["C"],
            r["D"],
            r["correct"],
            r["difficulty"]
        )
        refresh_stats()


# =====================
# SAVOLNI O‘CHIRISH
# =====================
def handle_delete():
    row = ui.table.currentRow()
    if row < 0:
        return

    qid = int(ui.table.item(row, 0).text())
    delete_question(qid)
    refresh_stats()


# =====================
# SAVOLNI TO‘LIQ TAHRIRLASH
# =====================
def handle_edit():
    row = ui.table.currentRow()
    if row < 0:
        return

    qid = int(ui.table.item(row, 0).text())

    data = {
        "q": ui.table.item(row, 1).text(),
        "A": ui.table.item(row, 2).text(),
        "B": ui.table.item(row, 3).text(),
        "C": ui.table.item(row, 4).text(),
        "D": ui.table.item(row, 5).text(),
        "correct": ui.table.item(row, 6).text(),
        "difficulty": ui.table.item(row, 7).text()
    }

    dlg = EditDialog(data, ui)
    if dlg.exec_():
        r = dlg.result_data()
        update_question(
            qid,
            r["q"],
            r["A"],
            r["B"],
            r["C"],
            r["D"],
            r["correct"],
            r["difficulty"]
        )
        refresh_stats()


# =====================
# TEST GENERATSIYA (PDF)
# =====================
def handle_generate():
    a1 = ui.asosiy1.currentText()
    a2 = ui.asosiy2.currentText()

    if a1 == a2:
        QMessageBox.warning(ui, "Xato", "Asosiy fanlar bir xil bo‘lishi mumkin emas.")
        return

    blocks = [
        ("Ona tili (majburiy)", generate_block("Ona tili", "majburiy", 10)),
        ("Matematika (majburiy)", generate_block("Matematika", "majburiy", 10)),
        ("Tarix (majburiy)", generate_block("Tarix", "majburiy", 10)),
        (a1, generate_block(a1, "asosiy", 30)),
        (a2, generate_block(a2, "asosiy", 30)),
    ]

    save_path, _ = QFileDialog.getSaveFileName(
        ui,
        "PDF saqlash",
        "blok_test.pdf",
        "PDF (*.pdf)"
    )

    if save_path:
        generate_pdf(save_path, blocks)
        QMessageBox.information(ui, "Tayyor", "PDF muvaffaqiyatli yaratildi.")


# =====================
# SIGNAL-LARNI ULLASH
# =====================
ui.btn_import.clicked.connect(handle_import)
ui.btn_delete.clicked.connect(handle_delete)
ui.btn_edit.clicked.connect(handle_edit)
ui.btn_pdf.clicked.connect(handle_generate)
ui.fan_select.currentIndexChanged.connect(load_questions)


# =====================
# BOSHLANG‘ICH YUKLASH
# =====================
refresh_stats()
load_questions()

ui.show()
sys.exit(app.exec_())
