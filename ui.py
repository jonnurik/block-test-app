import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox,
    QFileDialog, QMessageBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QTabWidget
)
from db import import_questions_from_file, list_subjects, add_question, count_questions_by_subject, init_db, get_subject_id
from pdfgen import generate_block_pdf
from datetime import datetime

class AdminTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        imp_h = QHBoxLayout()
        self.import_path_edit = QLineEdit()
        btn_browse = QPushButton("Fayl tanlash...")
        btn_browse.clicked.connect(self.browse_file)
        btn_import = QPushButton("Fayldan import")
        btn_import.clicked.connect(self.import_file)
        imp_h.addWidget(QLabel("CSV/XLSX fayl:"))
        imp_h.addWidget(self.import_path_edit)
        imp_h.addWidget(btn_browse)
        imp_h.addWidget(btn_import)
        layout.addLayout(imp_h)

        layout.addWidget(QLabel("Qo'lda savol qo'shish"))
        f_h = QHBoxLayout()
        left = QVBoxLayout()
        right = QVBoxLayout()
        self.s_edit = QLineEdit()
        self.q_edit = QTextEdit()
        self.a_edit = QLineEdit(); self.b_edit = QLineEdit(); self.c_edit = QLineEdit(); self.d_edit = QLineEdit()
        self.correct_combo = QComboBox(); self.correct_combo.addItems(['A','B','C','D'])
        left.addWidget(QLabel("Fan nomi:")); left.addWidget(self.s_edit)
        left.addWidget(QLabel("Savol:")); left.addWidget(self.q_edit)
        right.addWidget(QLabel("A:")); right.addWidget(self.a_edit)
        right.addWidget(QLabel("B:")); right.addWidget(self.b_edit)
        right.addWidget(QLabel("C:")); right.addWidget(self.c_edit)
        right.addWidget(QLabel("D:")); right.addWidget(self.d_edit)
        right.addWidget(QLabel("To'g'ri:")); right.addWidget(self.correct_combo)
        f_h.addLayout(left,2); f_h.addLayout(right,1)
        layout.addLayout(f_h)

        btn_add = QPushButton("Savol qo'shish")
        btn_add.clicked.connect(self.add_question_clicked)
        layout.addWidget(btn_add)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Fan", "Savollar soni"])
        layout.addWidget(QLabel("Mavjud fanlar:"))
        layout.addWidget(self.table)

        btn_refresh = QPushButton("Yangilash")
        btn_refresh.clicked.connect(self.refresh_subjects)
        layout.addWidget(btn_refresh)

        self.setLayout(layout)
        self.refresh_subjects()

    def browse_file(self):
        p, _ = QFileDialog.getOpenFileName(self, "Fayl tanlash", "", "Excel (*.xlsx *.xls);;CSV (*.csv)")
        if p:
            self.import_path_edit.setText(p)

    def import_file(self):
        path = self.import_path_edit.text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Xato", "Faylni tanlang.")
            return
        try:
            imp, skip = import_questions_from_file(path)
            QMessageBox.information(self, "Import", f"{imp} savol import qilindi, {skip} ta o'tkazildi.")
            self.refresh_subjects()
        except Exception as e:
            QMessageBox.critical(self, "Xato", str(e))

    def add_question_clicked(self):
        subj = self.s_edit.text().strip()
        q = self.q_edit.toPlainText().strip()
        a = self.a_edit.text().strip(); b = self.b_edit.text().strip(); c = self.c_edit.text().strip(); d = self.d_edit.text().strip()
        correct = self.correct_combo.currentText().strip()
        if not subj or not q or not a or not b or not c or not d:
            QMessageBox.warning(self, "Xato", "Barcha maydonlar to'ldirilishi kerak.")
            return
        add_question(subj, q, a, b, c, d, correct)
        QMessageBox.information(self, "OK", "Savol qo'shildi.")
        self.s_edit.clear(); self.q_edit.clear(); self.a_edit.clear(); self.b_edit.clear(); self.c_edit.clear(); self.d_edit.clear()
        self.refresh_subjects()

    def refresh_subjects(self):
        subs = list_subjects()
        self.table.setRowCount(len(subs))
        for i, (_, name, _) in enumerate(subs):
            cnt = count_questions_by_subject(name)
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(str(cnt)))

class GeneratorTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Majburiy fanlar avtomatik qo'shiladi: Ona tili, O'zbekiston tarixi, Matematika"))
        layout.addWidget(QLabel("Iltimos ikkita asosiy fan tanlang (har biri 30 ta)."))

        sel_h = QHBoxLayout()
        self.main1 = QComboBox(); self.main2 = QComboBox()
        btn_refresh = QPushButton("Fanlarni yangilash"); btn_refresh.clicked.connect(self.populate)
        sel_h.addWidget(QLabel("Asosiy fan 1:")); sel_h.addWidget(self.main1)
        sel_h.addWidget(QLabel("Asosiy fan 2:")); sel_h.addWidget(self.main2)
        sel_h.addWidget(btn_refresh)
        layout.addLayout(sel_h)

        opt_h = QHBoxLayout()
        self.shuffle_check = QtWidgets.QCheckBox("Variantlarni aralashtirish (shuffle)")
        self.shuffle_check.setChecked(True)
        opt_h.addWidget(self.shuffle_check)
        layout.addLayout(opt_h)

        btn_gen = QPushButton("PDF generatsiya qilish")
        btn_gen.clicked.connect(self.generate_clicked)
        layout.addWidget(btn_gen)

        self.log = QTextEdit(); self.log.setReadOnly(True)
        layout.addWidget(QLabel("Log:")); layout.addWidget(self.log)

        self.setLayout(layout)
        self.populate()

    def populate(self):
        self.main1.clear(); self.main2.clear()
        subs = list_subjects()
        names = [s[1] for s in subs]
        self.main1.addItems(names); self.main2.addItems(names)

    def generate_clicked(self):
        m1 = self.main1.currentText().strip()
        m2 = self.main2.currentText().strip()
        if not m1 or not m2:
            QMessageBox.warning(self, "Xato", "Iltimos ikkala asosiy fanni tanlang.")
            return
        structure = [
            ("Ona tili", 10),
            ("O'zbekiston tarixi", 10),
            ("Matematika", 10),
            (m1, 30),
            (m2, 30)
        ]
        insufficient = []
        for subj, need in structure:
            avail = count_questions_by_subject(subj)
            if avail == 0:
                insufficient.append((subj, need, avail))
        if insufficient:
            msg = "Quyidagi fanlarda savol mavjud emas:\n"
            for s,n,a in insufficient:
                msg += f"- {s}: kerak {n}, mavjud {a}\n"
            res = QMessageBox.question(self, "Yetishmayapti", msg + "\nDavom ettirish (mavjud savollar bilan)?")
            if res != QMessageBox.Yes:
                return
        path, _ = QFileDialog.getSaveFileName(self, "PDF saqlash", f"block_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", "PDF (*.pdf)")
        if not path:
            return
        mapping = {s:n for s,n in structure}
        try:
            self.log.append("PDF yaratilmoqda ...")
            generate_block_pdf(path, mapping, shuffle_options=self.shuffle_check.isChecked())
            self.log.append(f"PDF yaratildi: {path}")
            QMessageBox.information(self, "Tayyor", f"PDF yaratildi:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Xato", str(e))
            self.log.append("Xato: " + str(e))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Blok-test generatori (Desktop)")
        self.resize(980, 680)
        tabs = QTabWidget()
        self.admin = AdminTab(); self.gen = GeneratorTab()
        tabs.addTab(self.admin, "Admin (Savollar)")
        tabs.addTab(self.gen, "Test generatsiya")
        self.setCentralWidget(tabs)
