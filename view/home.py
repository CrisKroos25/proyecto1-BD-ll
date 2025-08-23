from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout

# ==========================
# Clase Home (pantalla simple)
# ==========================
class Home(QWidget):
    def __init__(self):
        super().__init__()

        # --- Widgets que se mostrarán ---
        self.label = QLabel("Esto es un texto")         # etiqueta de texto
        self.btn = QPushButton("Esto es un boton")      # botón

        self.label1 = QLabel("Esto es un texto")        # otra etiqueta
        self.btn1 = QPushButton("Esto es un boton")     # otro botón

        self.label2 = QLabel("Esto es un texto")        # otra etiqueta
        self.btn2 = QPushButton("Esto es un boton")     # otro botón

        # --- Layout vertical ---
        layout = QVBoxLayout()
        layout.addWidget(self.label)    # añadir widgets en orden vertical
        layout.addWidget(self.btn)
        layout.addWidget(self.label1)
        layout.addWidget(self.btn1)
        layout.addWidget(self.label2)
        layout.addWidget(self.btn2)

        # Asignar layout al QWidget
        self.setLayout(layout)
