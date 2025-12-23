from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QTextEdit
)

FANLAR = [
    "Biologiya", "Kimyo", "Ona tili",
    "Matematika", "Fizika", "Rus tili",
    "Huquqshunoslik", "Ingliz tili",
    "Geografiya", "Tarix"
]

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok test generatori")
        self.resize(520, 420)

        tabs = QTabWidget(self)

        # 1-QISM: BAZA
        tab1 = QWidget()
        l1 = QVBoxLayout(tab1)
        self.fan_select = QComboBox()
        self.fan_select.addItems(FANLAR)
        self.btn_import = QPushButton("JSON bazani import qilish")
        l1.addWidget(QLabel("Fan tanlang:"))
        l1.addWidget(self.fan_select)
        l1.addWidget(self.btn_import)

        # 2-QISM: GENERATSIYA
        tab2 = QWidget()
        l2 = QVBoxLayout(tab2)
        self.asosiy1 = QComboBox()
        self.asosiy2 = QComboBox()
        self.asosiy1.addItems(FANLAR)
        self.asosiy2.addItems(FANLAR)
        self.stats = QTextEdit()
        self.stats.setReadOnly(True)
        self.btn_pdf = QPushButton("PDF yaratish")

        l2.addWidget(QLabel("Asosiy fan 1:"))
        l2.addWidget(self.asosiy1)
        l2.addWidget(QLabel("Asosiy fan 2:"))
        l2.addWidget(self.asosiy2)
        l2.addWidget(QLabel("Bazadagi savollar holati:"))
        l2.addWidget(self.stats)
        l2.addWidget(self.btn_pdf)

        tabs.addTab(tab1, "1. Savollar bazasi")
        tabs.addTab(tab2, "2. Test generatsiya")

        main = QVBoxLayout(self)
        main.addWidget(tabs)
