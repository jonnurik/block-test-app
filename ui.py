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
        self.resize(520, 420)

        tabs = QTabWidget(self)

        # ===== TAB 1: IMPORT =====
        t1 = QWidget()
        l1 = QVBoxLayout(t1)

        self.fan_select = QComboBox()
        self.fan_select.addItems(FANLAR)

        self.block_type = QComboBox()
        self.block_type.addItems(["majburiy", "asosiy"])

        self.btn_import = QPushButton("JSON Import qilish")
        self.stats = QTextEdit()
        self.stats.setReadOnly(True)

        l1.addWidget(QLabel("Fan tanlang:"))
        l1.addWidget(self.fan_select)
        l1.addWidget(QLabel("Blok turi:"))
        l1.addWidget(self.block_type)
        l1.addWidget(self.btn_import)
        l1.addWidget(QLabel("Bazadagi savollar holati:"))
        l1.addWidget(self.stats)

        # ===== TAB 2: GENERATOR =====
        t2 = QWidget()
        l2 = QVBoxLayout(t2)

        self.asosiy1 = QComboBox()
        self.asosiy2 = QComboBox()
        self.asosiy1.addItems(FANLAR)
        self.asosiy2.addItems(FANLAR)

        self.btn_pdf = QPushButton("PDF yaratish")

        l2.addWidget(QLabel("Asosiy fan 1:"))
        l2.addWidget(self.asosiy1)
        l2.addWidget(QLabel("Asosiy fan 2:"))
        l2.addWidget(self.asosiy2)
        l2.addWidget(self.btn_pdf)

        tabs.addTab(t1, "1. Savollar bazasi")
        tabs.addTab(t2, "2. Test generatsiya")

        main = QVBoxLayout(self)
        main.addWidget(tabs)
