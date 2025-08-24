from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from connect_db import Connect   # función que abre la conexión a MySQL
from datetime import datetime
import pymysql

# Clase que representa la ventana de "Productos"
class Products(QMainWindow):
    def __init__(self):
        super().__init__()
        # Cargar la interfaz creada en Qt Designer
        uic.loadUi("ui/product.ui", self)

        self.conn = None
        # Al iniciar la ventana, cargar los datos de la BD
        self.load_data()

        # Conectar el botón "Registrar" con la función que inserta datos
        self.btn_registrar.clicked.connect(self.add_info)
        self.reload.clicked.connect(self.load_data)

    # -------------------- CARGAR DATOS --------------------
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
                cursor.execute("SELECT * FROM producto")
                rows = cursor.fetchall()

                # Configurar la tabla en la UI
                self.tableWidget.setRowCount(len(rows))
                self.tableWidget.setColumnCount(7)
                self.tableWidget.setHorizontalHeaderLabels(
                    ["Id", "Codigo", "Nombre comercial", "Stock",
                     "Precio de venta", "Precio de costo", "Estado"]
                )

                # Insertar fila por fila en la tabla
                for row_idx, row in enumerate(rows):
                    # row puede ser dict o tupla, por eso se revisa
                    ide = row["id"] if isinstance(row, dict) else row[0]
                    cd  = row["codigo"] if isinstance(row, dict) else row[1]
                    nc  = row["nombre_comercial"] if isinstance(row, dict) else row[2]
                    st  = row["stock"] if isinstance(row, dict) else row[3]
                    pv  = row["precio_venta"] if isinstance(row, dict) else row[4]
                    pc  = row["precio_costo"] if isinstance(row, dict) else row[5]
                    est = row["estado"] if isinstance(row, dict) else row[6]

                    # Insertar valores en cada celda de la tabla
                    self.tableWidget.setItem(row_idx, 0, QTableWidgetItem(str(ide)))
                    self.tableWidget.setItem(row_idx, 1, QTableWidgetItem(str(cd)))
                    self.tableWidget.setItem(row_idx, 2, QTableWidgetItem(str(nc)))
                    self.tableWidget.setItem(row_idx, 3, QTableWidgetItem(str(st)))
                    self.tableWidget.setItem(row_idx, 4, QTableWidgetItem(str(pv)))
                    self.tableWidget.setItem(row_idx, 5, QTableWidgetItem(str(pc)))
                    self.tableWidget.setItem(row_idx, 6, QTableWidgetItem(str(est)))

        except Exception as e:
            # Si hay error, se imprime en consola
            print("Error cargando datos:", e)
        finally:
            # Cierra la conexión solo si fue creada en esta función
            if not reuse_tx and conn:
                conn.close()

    # -------------------- INSERTAR --------------------
    def add_info(self):
        """
        Inserta un nuevo producto en la tabla 'producto'.
        Usa transacciones: si hay error → rollback, si todo ok → commit.
        """
        cn = None
        cur = None
        try:
            cn = Connect()
            cn.begin()          # Iniciar transacción
            cur = cn.cursor()   # Crear cursor

            # --- INSERT ---
            sql = """
                INSERT INTO producto
                    (codigo, nombre_comercial, stock, precio_venta, precio_costo, estado)
                VALUES
                    (%s, %s, %s, %s, %s, %s)
            """

            # Los valores se toman directamente de los campos de la UI
            params = (
                self.codigo.text().strip(),
                self.nombre.text().strip(),
                self.stock.text().strip(),
                self.p_venta.text().strip(),
                (self.p_costo.text().strip() or None) if hasattr(self, "p_costo") else None,
                self.estado.text().strip(),  # si es QCheckBox usar 1/0
            )

            # Ejecutar el insert
            cur.execute(sql, params)
            cn.commit()  # Confirmar cambios

            QMessageBox.information(self, "OK", "Producto agregado correctamente → COMMIT")
            self.load_data()  # Recargar tabla para mostrar el nuevo producto

            # --- LOG (COMMIT) ---

            cur.execute("""
                INSERT INTO bitacora (usuario, operacion, tabla_afectada, datos, estado, comentario, punto_recuperacion)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                "usuario_root",
                "INSERT",
                "producto",
                str(params),  # aquí params es tu tupla de valores del INSERT original
                "COMMIT",
                "Producto insertado correctamente",
                f"punto_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            ))
            cn.commit()


        except pymysql.MySQLError as e:
            # Si ocurre un error de MySQL (clave duplicada, check, etc.)
            if cn:
                try:
                    cn.rollback()  # Revertir transacción
                except:
                    pass
            QMessageBox.critical(self, "MySQL", f"ROLLBACK (MySQL):\n{e!r}")
            cur.execute("""
                            INSERT INTO bitacora (usuario, operacion, tabla_afectada, datos, estado, comentario, punto_recuperacion)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                "usuario_root", "INSERT", "producto", str(params), "ROLLBACK", f"Error: {e}", f"punto_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            ))
            cn.commit()
        except Exception as e:
            # Sí ocurre otro error general
            if cn:
                try:
                    cn.rollback()
                except:
                    pass
            QMessageBox.critical(self, "Error", f"ROLLBACK (general):\n{e!r}")
            cur.execute("""
                            INSERT INTO bitacora (usuario, operacion, tabla_afectada, datos, estado, comentario, punto_recuperacion)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                "usuario_root", "INSERT", "producto", str(params), "ROLLBACK", f"Error: {e}", f"punto_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
            ))
            cn.commit()
        finally:
            # Cerrar cursor y conexión para liberar recursos
            if cur:
                try:
                    cur.close()
                except:
                    pass
            if cn:
                try:
                    cn.close()
                except:
                    pass
