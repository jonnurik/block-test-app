from PyQt5.QtWidgets import *

FANLAR = [
    "Ona tili", "Matematika", "Tarix",
    "Biologiya", "Kimyo", "Fizika",
    "Ingliz tili", "Geografiya"
]

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.resize(700, 520)

        tabs = QTabWidget(self)

        # ===== TAB 1 =====
        t1 = QWidget()
        l1 = QVBoxLayout(t1)

        self.fan_select = QComboBox()
        self.fan_select.addItems(FANLAR)

        self.block_type = QComboBox()
        self.block_type.addItems(["majburiy", "asosiy"])

        self.btn_import = QPushButton("JSON Import")

        self.stats = QTextEdit()
        self.stats.setReadOnly(True)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Savol", "A", "B", "C", "D", "To‘g‘ri", "Qiyinlik"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)

        self.btn_edit = QPushButton("✏️ Tahrirlash")
        self.btn_delete = QPushButton("🗑 O‘chirish")

        l1.addWidget(QLabel("Fan:"))
        l1.addWidget(self.fan_select)
        l1.addWidget(QLabel("Blok turi:"))
        l1.addWidget(self.block_type)
        l1.addWidget(self.btn_import)
        l1.addWidget(QLabel("Statistika:"))
        l1.addWidget(self.stats)
        l1.addWidget(QLabel("Kiritilgan savollar:"))
        l1.addWidget(self.table)

        btns = QHBoxLayout()
        btns.addWidget(self.btn_edit)
        btns.addWidget(self.btn_delete)
        l1.addLayout(btns)

        # ===== TAB 2 =====
        t2 = QWidget()
        l2 = QVBoxLayout(t2)

        self.asosiy1 = QComboBox()
        self.asosiy2 = QComboBox()
        self.asosiy1.addItems(FANLAR)
        self.asosiy2.addItems(FANLAR)

        self.btn_pdf = QPushButton("PDF yaratish")

        l2.addWidget(QLabel("Asosiy fan 1"))
        l2.addWidget(self.asosiy1)
        l2.addWidget(QLabel("Asosiy fan 2"))
        l2.addWidget(self.asosiy2)
        l2.addWidget(self.btn_pdf)

        tabs.addTab(t1, "1. Savollar bazasi")
        tabs.addTab(t2, "2. Test generatsiya")

        main = QVBoxLayout(self)
        main.addWidget(tabs)
