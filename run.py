import sys
from PyQt5.QtWidgets import QApplication,QFileDialog,QMessageBox
from ui import MainUI
from db import init_db, stats
from importer import import_json
from generator import block
from pdfgen import generate_pdf
from editor import Editor

init_db()
app = QApplication(sys.argv)
ui = MainUI()

def refresh():
    t=""
    for s,b,c in stats():
        t+=f"{s} [{b}] : {c}\n"
    ui.stats.setText(t)

def imp():
    f,_=QFileDialog.getOpenFileName(ui,"JSON","","*.json")
    if f:
        n=import_json(f,ui.fan.currentText(),ui.type.currentText())
        QMessageBox.information(ui,"OK",f"{n} ta qo‘shildi")
        refresh()

def gen():
    blocks=[
        ("Ona tili",block("Ona tili","majburiy",10)),
        ("Matematika",block("Matematika","majburiy",10)),
        ("Tarix",block("Tarix","majburiy",10)),
        (ui.a1.currentText(),block(ui.a1.currentText(),"asosiy",30)),
        (ui.a2.currentText(),block(ui.a2.currentText(),"asosiy",30)),
    ]
    p,_=QFileDialog.getSaveFileName(ui,"PDF","","*.pdf")
    if p: generate_pdf(p,blocks)

ui.btn_import.clicked.connect(imp)
ui.btn_pdf.clicked.connect(gen)
ui.btn_edit.clicked.connect(lambda: Editor().show())

refresh()
ui.show()
sys.exit(app.exec_())
