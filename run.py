import sys
from PyQt5.QtWidgets import (
    QApplication, QFileDialog,
    QMessageBox, QTableWidgetItem
)

from ui import MainUI
from db import (
    init_db,
    get_stats,
    get_questions,
    delete_question,
    clear_block
)
from importer import import_xlsx
from generator import generate_blocks
from pdfgen import generate_pdf


# =====================
# START
# =====================
init_db()
app = QApplication(sys.argv)
ui = MainUI()


# =====================
# REFRESH
# =====================
def refresh():
    ui.stats.clear()
    for s, b, c in get_stats():
        ui.stats.append(f"{s} [{b}]: {c} ta")

    qs = get_questions(ui.fan.currentText(), ui.block.currentText())
    ui.table.setRowCount(0)

    for r, q in enumerate(qs):
        ui.table.insertRow(r)
        for c, v in enumerate(q):
            ui.table.setItem(r, c, QTableWidgetItem(str(v)))


# =====================
# IMPORT EXCEL
# =====================
def do_import():
    try:
        path, _ = QFileDialog.getOpenFileName(
            ui,
            "Excel faylni tanlang",
            "",
            "Excel fayllar (*.xlsx)"
        )
        if not path:
            return

        added = import_xlsx(path)

        QMessageBox.information(
            ui,
            "Muvaffaqiyatli",
            f"{added} ta savol bazaga qo‘shildi"
        )
        refresh()

    except Exception as e:
        QMessageBox.critical(ui, "Xatolik", str(e))


# =====================
# CLEAR BLOCK
# =====================
def do_clear():
    clear_block(ui.fan.currentText(), ui.block.currentText())
    refresh()


# =====================
# DELETE ONE
# =====================
def do_delete():
    row = ui.table.currentRow()
    if row < 0:
        QMessageBox.warning(ui, "Xato", "Savol tanlanmagan")
        return

    qid = int(ui.table.item(row, 0).text())
    delete_question(qid)
    refresh()


# =====================
# PDF
# =====================
def do_generate():
    path, _ = QFileDialog.getSaveFileName(
        ui,
        "PDF saqlash",
        "blok_test.pdf",
        "PDF (*.pdf)"
    )
    if not path:
        return

    blocks = generate_blocks("Biologiya", "Kimyo")
    generate_pdf(
    save_path,
    "assets/logo.png",
    blocks
    )
    QMessageBox.information(ui, "Tayyor", "PDF yaratildi")


# =====================
# SIGNALS
# =====================
ui.import_btn.clicked.connect(do_import)
ui.clear_btn.clicked.connect(do_clear)
ui.delete_btn.clicked.connect(do_delete)
ui.gen_btn.clicked.connect(do_generate)
ui.fan.currentIndexChanged.connect(refresh)
ui.block.currentIndexChanged.connect(refresh)

refresh()
ui.show()
sys.exit(app.exec_())
