import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from ui import MainUI
from db import *
from importer import import_json
from generator import generate_blocks
from pdfgen import generate_pdf
from edit_dialog import EditDialog

init_db()
app = QApplication(sys.argv)
ui = MainUI()


def refresh():
    ui.stats.clear()
    for s, b, c in get_stats():
        ui.stats.append(f"{s} [{b}]: {c}")

    qs = get_questions(ui.fan.currentText(), ui.block.currentText())
    ui.table.setRowCount(0)
    for r, q in enumerate(qs):
        ui.table.insertRow(r)
        for c, v in enumerate(q):
            ui.table.setItem(r, c, QTableWidgetItem(str(v)))


def do_import():
    try:
        path, _ = QFileDialog.getOpenFileName(ui, "JSON", "", "*.json")
        if not path:
            return

        if ui.block.currentText() == "majburiy" and ui.fan.currentText() not in (
            "Ona tili", "Matematika", "Tarix"
        ):
            QMessageBox.warning(ui, "Xato", "Majburiy blok faqat Ona tili, Matematika, Tarix")
            return

        import_json(path, ui.fan.currentText(), ui.block.currentText())
        refresh()

    except Exception as e:
        QMessageBox.critical(ui, "Xato", str(e))


def do_clear():
    clear_block(ui.fan.currentText(), ui.block.currentText())
    refresh()


def do_delete():
    r = ui.table.currentRow()
    if r < 0:
        return
    qid = int(ui.table.item(r, 0).text())
    delete_question(qid)
    refresh()


def do_edit():
    r = ui.table.currentRow()
    if r < 0:
        return
    q = [ui.table.item(r, c).text() for c in range(8)]
    dlg = EditDialog(q)
    if dlg.exec_():
        refresh()


def do_generate():
    path, _ = QFileDialog.getSaveFileName(ui, "PDF", "blok_test.pdf", "*.pdf")
    if not path:
        return
    blocks = generate_blocks("Biologiya", "Kimyo")
    generate_pdf(path, blocks)


ui.import_btn.clicked.connect(do_import)
ui.clear_btn.clicked.connect(do_clear)
ui.delete_btn.clicked.connect(do_delete)
ui.edit_btn.clicked.connect(do_edit)
ui.gen_btn.clicked.connect(do_generate)
ui.fan.currentIndexChanged.connect(refresh)
ui.block.currentIndexChanged.connect(refresh)

refresh()
ui.show()
sys.exit(app.exec_())
