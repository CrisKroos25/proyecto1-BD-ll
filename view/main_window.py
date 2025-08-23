from PyQt6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QStackedWidget)
from view.side_panel import SidePanel
from view.main_content import MainContent
from view.home import Home
from view.products import Products
from view.backups import Backups

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Título y tamaño inicial de la ventana
        self.setWindowTitle("Gestión de Configuración de Usuario")
        self.setGeometry(200, 100, 700, 600)

        # QMainWindow necesita un central widget para poder ponerle layouts
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # --- Layout principal (horizontal): [SidePanel | Stack] ---
        self.main_layout = QHBoxLayout(self)       # layout padre
        central_widget.setLayout(self.main_layout) # asigna el layout al central widget

        # Pila de pantallas; cada índice es una “vista”
        self.stack = QStackedWidget()
        self.stack.addWidget(Home())                    # 0: Inicio
        self.stack.addWidget(MainContent("Archivo"))    # 1: Archivo
        self.stack.addWidget(Products())               # 2: Productos
        self.stack.addWidget(MainContent("Cotizaciones")) # 3: Cotizaciones
        self.stack.addWidget(MainContent("Edición"))    # 4: Edición
        self.stack.addWidget(Backups())                # 5: Backups
        self.stack.addWidget(MainContent("Configuracion")) # 6: Configuración

        # Panel lateral con botones
        self.panel = SidePanel()

        # Conecta cada botón del panel a su índice en el stack.
        # El orden de botones en SidePanel debe coincidir con el orden de addWidget arriba.
        for i, btn in enumerate(self.panel.buttons):
            # Usamos default arg (ix=i) para “capturar” el índice correcto en el lambda
            btn.clicked.connect(lambda _, ix=i: self.stack.setCurrentIndex(ix))

        # Inserta panel y stack en el layout principal
        self.main_layout.addWidget(self.panel)
        self.main_layout.addWidget(self.stack)
