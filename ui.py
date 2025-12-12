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

        # options
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
        # aniq requsted asosiy fanlar ro'yxati
        subs = [
            "Biologiya",
            "Kimyo",
            "Ona tili va adabiyoti",
            "Matematika",
            "Fizika",
            "Rus tili",
            "Huquqshunoslik",
            "Ingliz tili",
            "Geografiya",
            "Tarix"
        ]
        # agar ma'lumotlar bazasida boshqa fanlar bo'lsa, ularni ham qo'shish mumkin:
        try:
            from db import list_subjects
            db_subs = [s[1] for s in list_subjects()]
            # Qo'shimcha: bazadagi nomlar bilan duplikatlarni yo'q qilamiz
            for s in db_subs:
                if s and s not in subs:
                    subs.append(s)
        except Exception:
            # agar db dan olinmasa, shunchaki oldingi ro'yxat bilan ishlaymiz
            pass

        # to'liq ro'yxatni combo-larga qo'yamiz
        self.main1.clear(); self.main2.clear()
        self.main1.addItems(subs); self.main2.addItems(subs)

    def generate_clicked(self):
        m1 = self.main1.currentText().strip()
        m2 = self.main2.currentText().strip()
        if not m1 or not m2:
            QMessageBox.warning(self, "Xato", "Iltimos ikkala asosiy fanni tanlang.")
            return
        if m1 == m2:
            res = QMessageBox.question(self, "Diqqat", "Ikkala asosiy fan bir xil tanlandi. Davom ettirishni xohlaysizmi?")
            if res != QMessageBox.Yes:
                return

        structure = [
            ("Ona tili", 10),
            ("O'zbekiston tarixi", 10),
            ("Matematika", 10),
            (m1, 30),
            (m2, 30)
        ]
        insufficient = []
        from db import count_questions_by_subject
        for subj, need in structure:
            avail = count_questions_by_subject(subj)
            if avail == 0:
                insufficient.append((subj, need, avail))
        if insufficient:
            msg = "Quyidagi fanlarda savol mavjud emas yoki yetarli emas:\n"
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
            from pdfgen import generate_block_pdf
            generate_block_pdf(path, mapping, shuffle_options=self.shuffle_check.isChecked())
            self.log.append(f"PDF yaratildi: {path}")
            QMessageBox.information(self, "Tayyor", f"PDF yaratildi:\n{path}")
        except Exception as e:
            QMessageBox.critical(self, "Xato", str(e))
            self.log.append("Xato: " + str(e))
