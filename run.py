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
from edit_dialog import EditDialog


# =====================
# ISHGA TUSHIRISH
# =====================
init_db()
app = QApplication(sys.argv)
ui = MainUI()


# =====================
# YANGILASH
# =====================
def refresh():
    # Statistika
    ui.stats.clear()
    for s, b, c in get_stats():
        ui.stats.append(f"{s} [{b}]: {c} ta")

    # Jadval
    qs = get_questions(ui.fan.currentText(), ui.block.currentText())
    ui.table.setRowCount(0)

    for r, q in enumerate(qs):
        ui.table.insertRow(r)
        for c, v in enumerate(q):
            ui.table.setItem(r, c, QTableWidgetItem(str(v)))


# =====================
# EXCEL IMPORT
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
            "Import bajarildi",
            f"{added} ta savol bazaga qo‘shildi"
        )
        refresh()

    except Exception as e:
        QMessageBox.critical(ui, "Xato", str(e))


# =====================
# BLOKNI TOZALASH
# =====================
def do_clear():
    reply = QMessageBox.question(
        ui,
        "Tasdiqlash",
        f"{ui.fan.currentText()} [{ui.block.currentText()}] "
        f"blokidagi barcha savollar o‘chirilsinmi?",
        QMessageBox.Yes | QMessageBox.No
    )
    if reply == QMessageBox.Yes:
        clear_block(ui.fan.currentText(), ui.block.currentText())
        refresh()


# =====================
# BITTA SAVOLNI O‘CHIRISH
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
# SAVOLNI TAHRIRLASH
# =====================
def do_edit():
    row = ui.table.currentRow()
    if row < 0:
        QMessageBox.warning(ui, "Xato", "Savol tanlanmagan")
        return

    q = [ui.table.item(row, c).text() for c in range(8)]
    dlg = EditDialog(q)
    if dlg.exec_():
        refresh()


# =====================
# PDF YARATISH
# =====================
def do_generate():
    path, _ = QFileDialog.getSaveFileName(
        ui,
        "PDF saqlash",
        "blok_test.pdf",
        "PDF fayllar (*.pdf)"
    )
    if not path:
        return

    try:
        # Asosiy fanlar (hozircha statik, keyin UI’dan tanlanadi)
        blocks = generate_blocks("Biologiya", "Kimyo")
        generate_pdf(path, blocks)
        QMessageBox.information(ui, "Tayyor", "PDF yaratildi")

    except Exception as e:
        QMessageBox.critical(ui, "Xato", str(e))


# =====================
# SIGNAL-LAR
# =====================
ui.import_btn.clicked.connect(do_import)
ui.clear_btn.clicked.connect(do_clear)
ui.delete_btn.clicked.connect(do_delete)
ui.edit_btn.clicked.connect(do_edit)
ui.gen_btn.clicked.connect(do_generate)

ui.fan.currentIndexChanged.connect(refresh)
ui.block.currentIndexChanged.connect(refresh)


# =====================
# BOSHLASH
# =====================
refresh()
ui.show()
sys.exit(app.exec_())
