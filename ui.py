from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox,
    QTextEdit, QTableWidget, QTableWidgetItem, QLabel
)


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.resize(900, 600)

        layout = QVBoxLayout(self)

        self.fan = QComboBox()
        self.fan.addItems([
            "Ona tili", "Matematika", "Tarix",
            "Biologiya", "Kimyo", "Fizika", "Ingliz tili"
        ])

        self.block = QComboBox()
        self.block.addItems(["majburiy", "asosiy"])

        self.import_btn = QPushButton("JSON import")
        self.clear_btn = QPushButton("Blokni tozalash")

        self.stats = QTextEdit()
        self.stats.setReadOnly(True)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Savol", "A", "B", "C", "D", "To‘g‘ri", "Qiyinlik"]
        )

        layout.addWidget(QLabel("Fan"))
        layout.addWidget(self.fan)
        layout.addWidget(QLabel("Blok"))
        layout.addWidget(self.block)
        layout.addWidget(self.import_btn)
        layout.addWidget(self.clear_btn)
        layout.addWidget(QLabel("Statistika"))
        layout.addWidget(self.stats)
        layout.addWidget(self.table)
