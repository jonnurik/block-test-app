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
    get_subject_stats,
    get_questions,
    delete_question,
    clear_block
)
from importer import import_json
from generator import generate_block
from pdfgen import generate_pdf


# =====================
# DASTURNI ISHGA TUSHIRISH
# =====================

init_db()

app = QApplication(sys.argv)
ui = MainUI()


# =====================
# YORDAMCHI FUNKSIYALAR
# =====================

def refresh_stats():
    """
    Statistika oynasini yangilash
    """
    stats = get_subject_stats()
    text = ""
    for subject, block, count in stats:
        text += f"{subject} [{block}]: {count} ta\n"

    if not text:
        text = "Bazaga hali savollar qo‘shilmagan."

    ui.stats.setText(text)


def load_questions():
    """
    Tanlangan fan + blok bo‘yicha savollarni jadvalga yuklash
    """
    subject = ui.fan_select.currentText()
    block = ui.block_type.currentText()

    questions = get_questions(subject, block)

    ui.table.setRowCount(0)

    for row_idx, q in enumerate(questions):
        ui.table.insertRow(row_idx)
        for col_idx, value in enumerate(q):
            ui.table.setItem(
                row_idx,
                col_idx,
                QTableWidgetItem(str(value))
            )


def refresh():
    refresh_stats()
    load_questions()


# =====================
# 1-QISM: JSON IMPORT
# =====================

def handle_import():
    try:
        file_path, _ = QFileDialog.getOpenFileName(
            ui,
            "JSON test bazani tanlang",
            "",
            "JSON fayllar (*.json)"
        )

        if not file_path:
            return

        subject = ui.fan_select.currentText()
        block = ui.block_type.currentText()

        # Majburiy blok tekshiruvi
        if block == "majburiy" and subject not in (
            "Ona tili", "Matematika", "Tarix"
        ):
            QMessageBox.warning(
                ui,
                "Xatolik",
                "Majburiy blok faqat Ona tili, Matematika va Tarix uchun."
            )
            return

        added = import_json(file_path, subject, block)

        QMessageBox.information(
            ui,
            "Import bajarildi",
            f"{subject} [{block}] faniga {added} ta savol qo‘shildi."
        )

        refresh()

    except Exception as e:
        QMessageBox.critical(
            ui,
            "Import xatosi",
            str(e)
        )


# =====================
# SAVOLNI O‘CHIRISH
# =====================

def handle_delete():
    row = ui.table.currentRow()
    if row < 0:
        QMessageBox.warning(ui, "Xatolik", "Savol tanlanmagan")
        return

    qid = int(ui.table.item(row, 0).text())

    delete_question(qid)
    refresh()


# =====================
# BLOKNI TOZALASH
# =====================

def handle_clear_block():
    subject = ui.fan_select.currentText()
    block = ui.block_type.currentText()

    reply = QMessageBox.question(
        ui,
        "Tasdiqlash",
        f"{subject} [{block}] blokidagi BARCHA savollar o‘chirilsinmi?",
        QMessageBox.Yes | QMessageBox.No
    )

    if reply == QMessageBox.Yes:
        clear_block(subject, block)
        refresh()


# =====================
# 2-QISM: TEST GENERATSIYA
# =====================

def handle_generate():
    try:
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
            if len(qs) == 0:
                QMessageBox.warning(
                    ui,
                    "Savollar yetarli emas",
                    f"{title} fanidan savollar yo‘q."
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

        generate_pdf(
            save_path,
            "assets/logo.png",
            blocks
        )

        QMessageBox.information(
            ui,
            "Tayyor",
            "Test PDF muvaffaqiyatli yaratildi."
        )

    except Exception as e:
        QMessageBox.critical(
            ui,
            "Xatolik",
            str(e)
        )


# =====================
# SIGNAL-LARNI ULLASH
# =====================

ui.btn_import.clicked.connect(handle_import)
ui.btn_delete.clicked.connect(handle_delete)
ui.btn_clear.clicked.connect(handle_clear_block)
ui.btn_pdf.clicked.connect(handle_generate)

ui.fan_select.currentIndexChanged.connect(load_questions)
ui.block_type.currentIndexChanged.connect(load_questions)


# =====================
# BOSHLANG‘ICH YUKLASH
# =====================

refresh()
ui.show()
sys.exit(app.exec_())
