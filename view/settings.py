from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6.QtCore import QProcess

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/setting.ui", self)
