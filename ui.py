class AdminTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # ==== NEW: 5 file selectors for 5 blocks ====
        layout.addWidget(QLabel("Blok fayllarini yuklash (har bir blok uchun alohida):"))
        files_grid = QGridLayout()

        # Labels for blocks (you can change text)
        block_labels = [
            ("1 - Ona tili (majburiy)", "Ona tili"),
            ("2 - O'zbekiston tarixi (majburiy)", "O'zbekiston tarixi"),
            ("3 - Matematika (majburiy)", "Matematika"),
            ("4 - Asosiy fan 1 (30 ta)", None),   # None => user can set subject from file or we will use force_subject
            ("5 - Asosiy fan 2 (30 ta)", None)
        ]

        # store widgets to access later
        self.block_file_edits = []
        self.block_browse_buttons = []
        self.block_import_buttons = []
        self.block_subject_edits = []

        for i, (label_text, forced_subject) in enumerate(block_labels):
            row = i
            lbl = QLabel(label_text)
            files_grid.addWidget(lbl, row, 0)

            file_edit = QLineEdit()
            files_grid.addWidget(file_edit, row, 1)
            self.block_file_edits.append(file_edit)

            btn_browse = QPushButton("Fayl tanlash...")
            files_grid.addWidget(btn_browse, row, 2)
            self.block_browse_buttons.append(btn_browse)
            # bind with index
            btn_browse.clicked.connect(lambda checked, idx=i: self.browse_block_file(idx))

            # subject override: if forced_subject is None show an input to let user type subject name
            subj_edit = QLineEdit()
            if forced_subject:
                subj_edit.setText(forced_subject)
                subj_edit.setDisabled(True)
            else:
                subj_edit.setPlaceholderText("Agar faylda subject yo'q bo'lsa kiriting")
            files_grid.addWidget(subj_edit, row, 3)
            self.block_subject_edits.append(subj_edit)

            btn_import = QPushButton("Import (blok %d)" % (i+1))
            files_grid.addWidget(btn_import, row, 4)
            btn_import.clicked.connect(lambda checked, idx=i: self.import_block_file(idx))
            self.block_import_buttons.append(btn_import)

        layout.addLayout(files_grid)
        # ==== END NEW FILE SELECTORS ====

        # existing rest of admin UI...
        # ... (keep your previous fields: manual add question area, existing table etc.)
        # At the end, set layout
        self.setLayout(layout)
        self.refresh_subjects()

    def browse_block_file(self, idx):
        p, _ = QFileDialog.getOpenFileName(self, f"Fayl tanlash (blok {idx+1})", "", "Excel (*.xlsx *.xls);;CSV (*.csv)")
        if p:
            self.block_file_edits[idx].setText(p)

    def import_block_file(self, idx):
        path = self.block_file_edits[idx].text().strip()
        if not path or not os.path.exists(path):
            QMessageBox.warning(self, "Xato", "Faylni tanlang yoki mavjudligini tekshiring.")
            return
        # get subject override if provided
        subject_override = self.block_subject_edits[idx].text().strip() or None
        # if no subject_override and the file must be for a specific mandatory subject (for first 3 blocks),
        # you may want to set forced names. Example: block 0..2 are mandatory
        forced_subject = None
        if idx == 0:
            forced_subject = "Ona tili"
        elif idx == 1:
            forced_subject = "O'zbekiston tarixi"
        elif idx == 2:
            forced_subject = "Matematika"
        # prefer explicit override if user typed something
        if subject_override:
            forced_subject = subject_override

        # determine force_type for mandatory blocks
        force_type = 'mandatory' if idx in (0,1,2) else 'main'

        try:
            imp, skip = import_questions_from_file(path, force_subject=forced_subject, force_type=force_type)
            QMessageBox.information(self, "Import", f"Blok {idx+1}: {imp} savol import qilindi, {skip} ta o'tkazildi.")
            self.refresh_subjects()
        except Exception as e:
            QMessageBox.critical(self, "Xato", str(e))
