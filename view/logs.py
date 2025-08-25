from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QInputDialog
from PyQt6.QtCore import QProcess
from connect_db import Connect

class Logs(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/log.ui", self)

        self.conn = None
        self.load_data()
        self.reload.clicked.connect(self.load_data)
        self.new_point.clicked.connect(self.mark_point)
        self.return_point.clicked.connect(self.get_back_point)


    def load_data(self, use_active_tx=True):
        """
        Carga todos los productos de la tabla 'producto'
        y los muestra en el QTableWidget de la interfaz.
        """
        # Si ya existe una conexión activa, se reutiliza
        reuse_tx = use_active_tx and (self.conn is not None)
        conn = self.conn if reuse_tx else None

        try:
            # Si no hay conexión activa, abrir una nueva
            if not reuse_tx:
                conn = Connect()

            # Crear cursor y ejecutar SELECT
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM bitacora")
                rows = cursor.fetchall()

                # Configurar la tabla en la UI
                self.tableWidget.setRowCount(len(rows))
                self.tableWidget.setColumnCount(9)
                self.tableWidget.setHorizontalHeaderLabels(
                    ["id", "fecha", "usuario", "operacion",
                     "tabla_afectada", "datos", "estado", "comentario", "punto_recuperacion"]
                )

                # Insertar fila por fila en la tabla
                for row_idx, row in enumerate(rows):
                    # row puede ser dict o tupla, por eso se revisa
                    ide = row["id"] if isinstance(row, dict) else row[0]
                    f = row["fecha"] if isinstance(row, dict) else row[1]
                    u = row["usuario"] if isinstance(row, dict) else row[2]
                    op = row["operacion"] if isinstance(row, dict) else row[3]
                    ta = row["tabla_afectada"] if isinstance(row, dict) else row[4]
                    dt = row["datos"] if isinstance(row, dict) else row[5]
                    est = row["estado"] if isinstance(row, dict) else row[6]
                    cmt = row["comentario"] if isinstance(row, dict) else row[7]
                    pr = row["punto_recuperacion"] if isinstance(row, dict) else row[8]

                    # Insertar valores en cada celda de la tabla
                    self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(ide)))
                    self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(str(f)))
                    self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(str(u)))
                    self.tableWidget.setItem(row_idx, 3, QTableWidgetItem(str(op)))
                    self.tableWidget.setItem(row_idx, 4, QTableWidgetItem(str(ta)))
                    self.tableWidget.setItem(row_idx, 5, QTableWidgetItem(str(dt)))
                    self.tableWidget.setItem(row_idx, 6, QTableWidgetItem(str(est)))
                    self.tableWidget.setItem(row_idx, 7, QTableWidgetItem(str(cmt)))
                    self.tableWidget.setItem(row_idx, 8, QTableWidgetItem(str(pr)))

        except Exception as e:
            # Si hay error, se imprime en consola
            print("Error cargando datos:", e)
        finally:
            # Cierra la conexión solo si fue creada en esta función
            if not reuse_tx and conn:
                conn.close()

    def mark_point(self):
        nombre_punto, ok1 = QInputDialog.getText(self, "Nuevo punto", "Ingresa un nombre para el nuevo punto:")
        comentario, ok2 = QInputDialog.getText(self, "Comentario", "Ingresa un comentario para el nuevo punto:")

        if not (ok1 and ok2):  # si canceló alguno de los diálogos
            return

        cn = Connect()
        cur = cn.cursor()
        cur.execute("""
            INSERT INTO bitacora (usuario, operacion, tabla_afectada, datos, estado, comentario, punto_recuperacion)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            "usuario_root", "PUNTO", "-", None, "COMMIT",
            comentario, nombre_punto
        ))
        cn.commit()
        cur.close()
        cn.close()

        QMessageBox.information(self, "OK", "Punto agregado correctamente")
        self.load_data()  # Recargar tabla para mostrar el nuevo producto

    def get_back_point(self):
        nombre_punto, ok1 = QInputDialog.getText(self, "Buscar punto", "Ingresa el nombre del punto a regresar:")

        if not ok1:  # si canceló alguno de los diálogos
            return

        cn = Connect()
        cur = cn.cursor()

        # Obtener ID del punto de recuperación
        cur.execute("SELECT id FROM bitacora WHERE punto_recuperacion=%s ORDER BY id DESC LIMIT 1", (nombre_punto,))
        row = cur.fetchone()
        if not row:
            print("No existe el punto de recuperación")
            return
        id_punto = row["id"]

        # Buscar operaciones posteriores a ese punto
        cur.execute("SELECT * FROM bitacora WHERE id > %s ORDER BY id ASC", (id_punto,))
        rows = cur.fetchall()

        #Simular un rollback manual
        for log in rows:
            if log["operacion"] == "INSERT" and log["estado"] == "COMMIT" and log["tabla_afectada"] == "producto":
                datos = eval(log["datos"])
                codigo = datos[0]
                cur.execute("DELETE FROM producto WHERE codigo=%s", (codigo,))
                print(f"Eliminado producto {codigo} para volver a {nombre_punto}")

        cn.commit()
        cur.close()
        cn.close()

