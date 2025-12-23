from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
)

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.resize(420, 260)

        layout = QVBoxLayout(self)

        self.asosiy1 = QComboBox()
        self.asosiy2 = QComboBox()

        fanlar = [
            "Biologiya", "Kimyo", "Ona tili va adabiyoti",
            "Matematika", "Fizika", "Rus tili",
            "Huquqshunoslik", "Ingliz tili",
            "Geografiya", "Tarix"
        ]

        self.asosiy1.addItems(fanlar)
        self.asosiy2.addItems(fanlar)

        self.btn_file = QPushButton("Savollar faylini tanlash (.json)")
        self.btn_gen = QPushButton("PDF yaratish")

        layout.addWidget(QLabel("Asosiy fan 1:"))
        layout.addWidget(self.asosiy1)
        layout.addWidget(QLabel("Asosiy fan 2:"))
        layout.addWidget(self.asosiy2)
        layout.addWidget(self.btn_file)
        layout.addWidget(self.btn_gen)
