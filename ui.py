from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox,
    QTextEdit, QTableWidget, QLabel
)


class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.resize(1000, 650)

        layout = QVBoxLayout(self)

        # ===== FANLAR =====
        self.all_subjects = [
            "Ona tili", "Matematika", "Tarix",
            "Biologiya", "Kimyo", "Fizika",
            "Ingliz tili", "Geografiya"
        ]

        self.mandatory_subjects = [
            "Ona tili", "Matematika", "Tarix"
        ]

        self.fan = QComboBox()
        self.fan.addItems(self.mandatory_subjects)

        # ===== BLOK =====
        self.block = QComboBox()
        self.block.addItems(["majburiy", "asosiy"])
        self.block.currentTextChanged.connect(self.update_subjects)

        # ===== TUGMALAR =====
        self.import_btn = QPushButton("Excel (.xlsx) import")
        self.clear_btn = QPushButton("Blokni tozalash")

        # ===== STATISTIKA =====
        self.stats = QTextEdit()
        self.stats.setReadOnly(True)

        # ===== JADVAL =====
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Savol", "A", "B", "C", "D", "To‘g‘ri", "Qiyinlik"]
        )

        self.edit_btn = QPushButton("Tahrirlash")
        self.delete_btn = QPushButton("Bitta savolni o‘chirish")
        self.gen_btn = QPushButton("PDF yaratish")

        # ===== JOYLASH =====
        for w in (
            QLabel("Fan"), self.fan,
            QLabel("Blok"), self.block,
            self.import_btn, self.clear_btn,
            QLabel("Statistika"), self.stats,
            self.table,
            self.edit_btn, self.delete_btn,
            self.gen_btn
        ):
            layout.addWidget(w)

    # ===== MAJBURIY BLOKDA FANLARNI CHEKLASH =====
    def update_subjects(self, block):
        self.fan.clear()
        if block == "majburiy":
            self.fan.addItems(self.mandatory_subjects)
        else:
            self.fan.addItems(self.all_subjects)
