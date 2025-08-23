from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel)
from PyQt6.QtGui import QFont

class MainContent(QWidget):
    def __init__(self, texto):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(texto)
        layout.addWidget(label)
        self.setLayout(layout)