from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QMessageBox
)
from importer import import_json
from generator import generate_test
from pdfgen import generate_pdf

SUBJECTS = [
    "Biologiya", "Kimyo", "Ona tili",
    "Matematika", "Fizika", "Tarix",
    "Ingliz tili", "Geografiya"
]

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.setMinimumWidth(400)

        layout = QVBoxLayout()

        # --- 1-qism ---
        layout.addWidget(QLabel("📥 Test bazasini shakllantirish"))
        self.subj = QComboBox()
        self.subj.addItems(SUBJECTS)
        layout.addWidget(self.subj)

        btn_import = QPushButton("JSON bazani import qilish")
        btn_import.clicked.connect(self.import_data)
        layout.addWidget(btn_import)

        # --- 2-qism ---
        layout.addWidget(QLabel("📄 Test generatsiyasi"))

        self.main1 = QComboBox()
        self.main2 = QComboBox()
        self.main1.addItems(SUBJECTS)
        self.main2.addItems(SUBJECTS)

        layout.addWidget(self.main1)
        layout.addWidget(self.main2)

        btn_pdf = QPushButton("PDF yaratish")
        btn_pdf.clicked.connect(self.create_pdf)
        layout.addWidget(btn_pdf)

        self.setLayout(layout)

    def import_data(self):
        file, _ = QFileDialog.getOpenFileName(self, "JSON tanlang", "", "JSON (*.json)")
        if file:
            import_json(file, self.subj.currentText(), "asosiy", "orta")
            QMessageBox.information(self, "OK", "Bazaga saqlandi")

    def create_pdf(self):
        questions = generate_test(
            self.main1.currentText(),
            self.main2.currentText()
        )
        generate_pdf(questions)
        QMessageBox.information(self, "Tayyor", "PDF yaratildi")
