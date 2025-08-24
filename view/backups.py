from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtCore import QProcess

class Backups(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/backup.ui", self)

        # --- Conexiones de botones ---
        self.btn_backup_export.clicked.connect(self.run_export)
        self.btn_backup_import.clicked.connect(self.run_import)

    def run_export(self):
        opcion = self.backup_combo.currentText()
        if not opcion:
            QMessageBox.warning(self, "Advertencia", "Seleccione una opción de backup.")
            return

        # Ejecutar script de export (ajusta con la ruta real de tu script)
        process = QProcess(self)
        process.startDetached("python", ["scripts/export_completo.py", opcion])

        QMessageBox.information(self, "Éxito", f"Backup exportado con opción: {opcion}")

    def run_import(self):
        opcion = self.backup_combo.currentText()
        if not opcion:
            QMessageBox.warning(self, "Advertencia", "Seleccione una opción de backup.")
            return

        # Ejecutar script de import (ajusta con la ruta real de tu script)
        process = QProcess(self)
        process.startDetached("python", ["scripts/import_completo.py", opcion])

        QMessageBox.information(self, "Éxito", f"Backup importado con opción: {opcion}")