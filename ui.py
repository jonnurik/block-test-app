from PyQt5.QtWidgets import *

FANLAR = ["Ona tili","Matematika","Tarix","Biologiya","Kimyo","Fizika"]

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Generator")
        self.resize(520,420)

        tabs = QTabWidget(self)

        # TAB 1 – IMPORT
        t1 = QWidget()
        l1 = QVBoxLayout(t1)
        self.fan = QComboBox(); self.fan.addItems(FANLAR)
        self.type = QComboBox(); self.type.addItems(["majburiy","asosiy"])
        self.btn_import = QPushButton("JSON Import")
        self.stats = QTextEdit(); self.stats.setReadOnly(True)

        l1.addWidget(self.fan)
        l1.addWidget(self.type)
        l1.addWidget(self.btn_import)
        l1.addWidget(self.stats)

        # TAB 2 – GENERATOR
        t2 = QWidget()
        l2 = QVBoxLayout(t2)
        self.a1 = QComboBox(); self.a1.addItems(FANLAR)
        self.a2 = QComboBox(); self.a2.addItems(FANLAR)
        self.btn_pdf = QPushButton("PDF yaratish")
        self.btn_edit = QPushButton("Testlarni tahrirlash")

        l2.addWidget(self.a1)
        l2.addWidget(self.a2)
        l2.addWidget(self.btn_pdf)
        l2.addWidget(self.btn_edit)

        tabs.addTab(t1,"1. Baza")
        tabs.addTab(t2,"2. Generator")

        main = QVBoxLayout(self)
        main.addWidget(tabs)
