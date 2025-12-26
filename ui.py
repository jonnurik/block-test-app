from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox,
    QTextEdit, QTableWidget, QTableWidgetItem, QLabel
)


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.resize(1000, 650)

        layout = QVBoxLayout(self)

        self.fan = QComboBox()
        self.fan.addItems([
            "Ona tili", "Matematika", "Tarix",
            "Biologiya", "Kimyo", "Fizika",
            "Ingliz tili", "Geografiya"
        ])

        self.block = QComboBox()
        self.block.addItems(["majburiy", "asosiy"])

        self.import_btn = QPushButton("JSON import")
        self.clear_btn = QPushButton("Blokni tozalash")
        self.edit_btn = QPushButton("Tahrirlash")
        self.delete_btn = QPushButton("Bitta savolni o‘chirish")

        self.stats = QTextEdit()
        self.stats.setReadOnly(True)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Savol", "A", "B", "C", "D", "To‘g‘ri", "Qiyinlik"]
        )

        self.gen_btn = QPushButton("PDF yaratish")

        for w in (
            QLabel("Fan"), self.fan,
            QLabel("Blok"), self.block,
            self.import_btn, self.clear_btn,
            QLabel("Statistika"), self.stats,
            self.table, self.edit_btn, self.delete_btn,
            self.gen_btn
        ):
            layout.addWidget(w)
