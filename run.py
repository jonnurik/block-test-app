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
    init_db,
    get_stats,
    get_questions_by_subject,
    update_question,
    delete_question
)
from importer import import_json
from generator import generate_block
from pdfgen import generate_pdf


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

    # statistika yangilanganda jadval ham yangilansin
    load_questions()


# =====================
# JSON IMPORT
# =====================
def handle_import():
    file_path, _ = QFileDialog.getOpenFileName(
        ui,
        "JSON test bazani tanlang",
        "",
        "JSON fayllar (*.json)"
    )

    if not file_path:
        return

    subject = ui.fan_select.currentText()
    block_type = ui.block_type.currentText()

    try:
        added = import_json(file_path, subject, block_type)

        QMessageBox.information(
            ui,
            "Import muvaffaqiyatli",
            f"{subject} ({block_type}) faniga {added} ta savol qo‘shildi."
        )

        refresh_stats()

    except Exception as e:
        QMessageBox.critical(
            ui,
            "Xatolik",
            f"Import paytida xato yuz berdi:\n{e}"
        )


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
# SAVOLNI TAHRIRLASH (SODDA)
# =====================
def handle_edit():
    row = ui.table.currentRow()

    if row < 0:
        return

    qid = int(ui.table.item(row, 0).text())

    new_text, ok = QInputDialog.getText(
        ui,
        "Savolni tahrirlash",
        "Yangi savol matni:",
        text=ui.table.item(row, 1).text()
    )

    if not ok or not new_text:
        return

    update_question(
        qid,
        new_text,
        ui.table.item(row, 2).text(),
        ui.table.item(row, 3).text(),
        ui.table.item(row, 4).text(),
        ui.table.item(row, 5).text(),
        ui.table.item(row, 6).text()
    )

    refresh_stats()


# =====================
# TEST GENERATSIYA (PDF)
# =====================
def handle_generate():
    asosiy1 = ui.asosiy1.currentText()
    asosiy2 = ui.asosiy2.currentText()

    if asosiy1 == asosiy2:
        QMessageBox.warning(
            ui,
            "Xatolik",
            "Asosiy fanlar bir xil bo‘lishi mumkin emas."
        )
        return

    blocks = [
        ("Ona tili (majburiy)", generate_block("Ona tili", "majburiy", 10)),
        ("Matematika (majburiy)", generate_block("Matematika", "majburiy", 10)),
        ("Tarix (majburiy)", generate_block("Tarix", "majburiy", 10)),
        (asosiy1, generate_block(asosiy1, "asosiy", 30)),
        (asosiy2, generate_block(asosiy2, "asosiy", 30)),
    ]

    for title, qs in blocks:
        if not qs or len(qs) == 0:
            QMessageBox.warning(
                ui,
                "Savollar yetarli emas",
                f"{title} fanidan yetarli savol yo‘q."
            )
            return

    save_path, _ = QFileDialog.getSaveFileName(
        ui,
        "PDF saqlash",
        "blok_test.pdf",
        "PDF fayllar (*.pdf)"
    )

    if not save_path:
        return

    try:
        generate_pdf(save_path, blocks)
        QMessageBox.information(
            ui,
            "Tayyor",
            "Test PDF muvaffaqiyatli yaratildi."
        )
    except Exception as e:
        QMessageBox.critical(
            ui,
            "Xatolik",
            f"PDF yaratishda xato:\n{e}"
        )


# =====================
# SIGNAL-LARNI ULLASH
# =====================
ui.btn_import.clicked.connect(handle_import)
ui.btn_delete.clicked.connect(handle_delete)
ui.btn_edit.clicked.connect(handle_edit)
ui.btn_pdf.clicked.connect(handle_generate)

# fan o‘zgarganda jadval avtomatik yangilansin
ui.fan_select.currentIndexChanged.connect(load_questions)


# =====================
# BOSHLANG‘ICH YUKLASH
# =====================
refresh_stats()
load_questions()

ui.show()
sys.exit(app.exec_())