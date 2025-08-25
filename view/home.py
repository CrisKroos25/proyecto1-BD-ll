from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic

# ==========================
# Clase Home (pantalla simple)
# ==========================
class Home(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("ui/home.ui", self)

