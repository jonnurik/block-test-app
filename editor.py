from PyQt5.QtWidgets import QWidget,QVBoxLayout,QListWidget,QInputDialog
from db import get_all, update

class Editor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test tahrirlash")
        self.resize(600,400)

        self.list = QListWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.list)

        self.data = get_all()
        for q in self.data:
            self.list.addItem(f"{q[0]}. {q[4][:60]}")

        self.list.itemDoubleClicked.connect(self.edit)

    def edit(self):
        idx = self.list.currentRow()
        q = self.data[idx]

        newq, ok = QInputDialog.getText(self,"Savol","Savol:", text=q[4])
        if ok:
            update(q[0], (q[1],q[2],q[3],newq,q[5],q[6],q[7],q[8],q[9]))
