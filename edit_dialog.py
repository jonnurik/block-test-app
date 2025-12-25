from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox
)

class EditDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Savolni tahrirlash")
        self.resize(500, 420)

        self.data = data  # dict: id, q, A, B, C, D, correct, difficulty

        layout = QVBoxLayout(self)

        self.q_edit = QTextEdit(data["q"])
        layout.addWidget(QLabel("Savol:"))
        layout.addWidget(self.q_edit)

        self.A = QLineEdit(data["A"])
        self.B = QLineEdit(data["B"])
        self.C = QLineEdit(data["C"])
        self.D = QLineEdit(data["D"])

        for lbl, w in [("A", self.A), ("B", self.B), ("C", self.C), ("D", self.D)]:
            layout.addWidget(QLabel(lbl + ":"))
            layout.addWidget(w)

        self.correct = QComboBox()
        self.correct.addItems(["A", "B", "C", "D"])
        self.correct.setCurrentText(data["correct"])
        layout.addWidget(QLabel("To‘g‘ri javob:"))
        layout.addWidget(self.correct)

        self.diff = QComboBox()
        self.diff.addItems(["oson", "orta", "qiyin"])
        self.diff.setCurrentText(data.get("difficulty", "orta"))
        layout.addWidget(QLabel("Qiyinlik:"))
        layout.addWidget(self.diff)

        btns = QHBoxLayout()
        self.ok = QPushButton("Saqlash")
        self.cancel = QPushButton("Bekor qilish")
        btns.addWidget(self.ok)
        btns.addWidget(self.cancel)
        layout.addLayout(btns)

        self.ok.clicked.connect(self.accept)
        self.cancel.clicked.connect(self.reject)

    def result_data(self):
        return {
            "q": self.q_edit.toPlainText().strip(),
            "A": self.A.text(),
            "B": self.B.text(),
            "C": self.C.text(),
            "D": self.D.text(),
            "correct": self.correct.currentText(),
            "difficulty": self.diff.currentText()
        }