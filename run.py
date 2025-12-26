import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from ui import MainUI
from db import init_db, get_stats, get_questions, clear_block
from importer import import_json


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
        added = import_json(path, ui.fan.currentText(), ui.block.currentText())
        QMessageBox.information(ui, "OK", f"{added} ta savol qo‘shildi")
        refresh()
    except Exception as e:
        QMessageBox.critical(ui, "Xato", str(e))


def do_clear():
    clear_block(ui.fan.currentText(), ui.block.currentText())
    refresh()


ui.import_btn.clicked.connect(do_import)
ui.clear_btn.clicked.connect(do_clear)
ui.fan.currentIndexChanged.connect(refresh)
ui.block.currentIndexChanged.connect(refresh)

refresh()
ui.show()
sys.exit(app.exec_())
