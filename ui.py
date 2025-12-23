from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMessageBox
)

class MainUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Blok test generatori")
        self.resize(420, 360)

        layout = QVBoxLayout(self)

        # Asosiy fanlar
        self.asosiy1 = QComboBox()
        self.asosiy2 = QComboBox()

        fanlar = [
            "Biologiya",
            "Kimyo",
            "Fizika",
            "Matematika",
            "Ingliz tili",
            "Geografiya",
            "Tarix",
            "Ona tili",
            "Ona tili va adabiyoti",
            "Rus tili",
            "Huquqshunoslik"
        ]

        self.asosiy1.addItems(fanlar)
        self.asosiy2.addItems(fanlar)

        # Tugmalar
        self.btn_file = QPushButton("Savollar faylini tanlash")
        self.btn_gen = QPushButton("PDF yaratish")

        # Layout
        layout.addWidget(QLabel("Asosiy fan 1:"))
        layout.addWidget(self.asosiy1)

        layout.addWidget(QLabel("Asosiy fan 2:"))
        layout.addWidget(self.asosiy2)

        layout.addWidget(self.btn_file)
        layout.addWidget(self.btn_gen)
