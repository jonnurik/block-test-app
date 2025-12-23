import sys
from PyQt5.QtWidgets import QApplication
from db import init_db
from ui import MainWindow

init_db()

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
