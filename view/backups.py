from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow

class Backups(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/backup.ui", self)

        self.backup_combo
        self.btn_backup_export
        self.btn_backup_import

