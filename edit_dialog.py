from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox
)

class EditDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Savolni tahrirlash")
        self.resize(500, 430)

        self.data = data

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Savol:"))
        self.q_edit = QTextEdit(data["q"])
        layout.addWidget(self.q_edit)

        self.A = QLineEdit(data["A"])
        self.B = QLineEdit(data["B"])
        self.C = QLineEdit(data["C"])
        self.D = QLineEdit(data["D"])

        for name, field in [("A", self.A), ("B", self.B), ("C", self.C), ("D", self.D)]:
            layout.addWidget(QLabel(name + ":"))
            layout.addWidget(field)

        layout.addWidget(QLabel("To‘g‘ri javob:"))
        self.correct = QComboBox()
        self.correct.addItems(["A", "B", "C", "D"])
        self.correct.setCurrentText(data["correct"])
        layout.addWidget(self.correct)

        layout.addWidget(QLabel("Qiyinlik darajasi:"))
        self.diff = QComboBox()
        self.diff.addItems(["oson", "orta", "qiyin"])
        self.diff.setCurrentText(data.get("difficulty", "orta"))
        layout.addWidget(self.diff)

        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Saqlash")
        self.btn_cancel = QPushButton("Bekor qilish")
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)

        layout.addLayout(btns)

        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

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