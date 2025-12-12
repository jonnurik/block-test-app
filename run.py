import sys
from PyQt5.QtWidgets import QApplication
from ui import MainWindow
from db import init_db, get_subject_id

def ensure_mandatory_subjects():
    for name in ["Ona tili", "O'zbekiston tarixi", "Matematika"]:
        get_subject_id(name, create_if_missing=True, type_hint='mandatory')

def main():
    init_db()
    ensure_mandatory_subjects()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
