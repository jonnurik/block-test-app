import sys
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMessageBox
)

from ui import MainUI
from db import init_db, get_subject_stats
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
# STATISTIKANI YANGILASH
# =====================

def refresh_stats():
    stats = get_subject_stats()
    text = ""
    for subject, count in stats:
        text += f"{subject}: {count} ta savol\n"
    if not text:
        text = "Bazaga hali savollar qo‘shilmagan."
    ui.stats.setText(text)


# =====================
# 1-QISM: JSON IMPORT
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

    try:
        added = import_json(file_path, subject)
        QMessageBox.information(
            ui,
            "Import muvaffaqiyatli",
            f"{subject} faniga {added} ta savol qo‘shildi."
        )
        refresh_stats()

    except Exception as e:
        QMessageBox.critical(
            ui,
            "Xatolik",
            f"Import paytida xato yuz berdi:\n{e}"
        )


# =====================
# 2-QISM: TEST GENERATSIYA
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

    try:
        blocks = [
            ("Ona tili (majburiy)", generate_block("Ona tili", 10)),
            ("Matematika (majburiy)", generate_block("Matematika", 10)),
            ("Tarix (majburiy)", generate_block("Tarix", 10)),
            (asosiy1, generate_block(asosiy1, 30)),
            (asosiy2, generate_block(asosiy2, 30)),
        ]

        # Savollar yetarliligini tekshirish
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
            f"PDF yaratishda xato yuz berdi:\n{e}"
        )


# =====================
# SIGNAL-LARNI ULLASH
# =====================

ui.btn_import.clicked.connect(handle_import)
ui.btn_pdf.clicked.connect(handle_generate)


# =====================
# BOSHLANG‘ICH STATISTIKA
# =====================

refresh_stats()

ui.show()
sys.exit(app.exec_())
