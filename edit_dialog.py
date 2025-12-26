from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton
from db import update_question


class EditDialog(QDialog):
    def __init__(self, q):
        super().__init__()
        self.qid = q[0]

        layout = QVBoxLayout(self)

        self.q = QLineEdit(q[1])
        self.A = QLineEdit(q[2])
        self.B = QLineEdit(q[3])
        self.C = QLineEdit(q[4])
        self.D = QLineEdit(q[5])
        self.correct = QLineEdit(q[6])
        self.diff = QLineEdit(q[7])

        for w in (self.q, self.A, self.B, self.C, self.D, self.correct, self.diff):
            layout.addWidget(w)

        btn = QPushButton("Saqlash")
        btn.clicked.connect(self.save)
        layout.addWidget(btn)

    def save(self):
        update_question(
            self.qid,
            self.q.text(),
            self.A.text(),
            self.B.text(),
            self.C.text(),
            self.D.text(),
            self.correct.text(),
            self.diff.text()
        )
        self.accept()
