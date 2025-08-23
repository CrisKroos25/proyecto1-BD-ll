import sys
from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""QWidget { background: #000; color: #EAEAEA; }""")

    w = MainWindow()
    w.setMinimumWidth(900)
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
