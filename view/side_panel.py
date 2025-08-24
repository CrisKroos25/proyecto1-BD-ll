from PyQt6.QtWidgets import QFrame, QVBoxLayout, QPushButton

# =======================
# Estilos QSS
# =======================
# Color de fondo oscuro para el panel lateral
DARK_QSS_PANEL = "background-color: #222;"

# Estilo de los botones en modo oscuro
DARK_QSS_BUTTON = """
QPushButton {
    background-color: transparent;  /* fondo transparente */
    color: white;                   /* texto en blanco */
    text-align: left;               /* alineado a la izquierda */
    border: none;                   /* sin borde */
    padding: 10px;                  /* espacio interno */
}
QPushButton:hover {
    background-color: #333;         /* color al pasar el ratón */
}
"""

# =======================
# Clase del panel lateral
# =======================
class SidePanel(QFrame):
    def __init__(self):
        super().__init__()

        # Configuración base de tamaño
        self.setMinimumWidth(175)   # ancho mínimo del panel
        self.setMaximumWidth(1000)  # ancho máximo (para no deformar la UI)

        # Layout vertical que contendrá los botones
        layout = QVBoxLayout()

        # Datos de los botones: cada tupla es (icono, texto)
        buttons_data = [
            ("🏠", "Inicio"),
            ("📁", "Archivo"),
            ("📁", "Productos"),
            ("📁", "Cotizaciones"),
            ("📁", "Bitacora"),
            ("📁", "Backups"),
            ("⚙️", "Configuración"),
        ]

        # Lista para guardar referencias a los botones creados
        self.buttons = []

        # Crear y agregar cada botón al layout
        for icon, label in buttons_data:
            # Crear botón con un icono en forma de emoji + texto
            btn = QPushButton(f"{icon}  {label}")
            btn.setStyleSheet(DARK_QSS_BUTTON)  # aplicar estilo definido arriba
            layout.addWidget(btn)               # añadir al layout vertical
            self.buttons.append(btn)            # guardar referencia en lista

        # Establecer el layout construido al QFrame
        self.setLayout(layout)

        # Aplicar el estilo oscuro al panel completo
        self._apply_theme()

    # =======================
    # Métodos privados
    # =======================
    def _apply_theme(self):
        """
        Aplica el estilo del panel lateral.
        """
        self.setStyleSheet(DARK_QSS_PANEL)
