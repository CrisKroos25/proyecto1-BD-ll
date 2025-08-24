import subprocess
import os
from glob import glob

MYSQL_USER = "root"
MYSQL_PASSWORD = ""
DATABASE_NAME = "tienda"
MYSQL_PATH = r"C:\Program Files\MySQL\MySQL Server 8.0\bin"
BACKUP_DIR = r"D:\BackupsMySQL"

backup_files = glob(os.path.join(BACKUP_DIR, f"{DATABASE_NAME}_*.sql"))
if not backup_files:
    print("No se encontraron backups en la carpeta.")
    exit()

backup_file = max(backup_files, key=os.path.getctime)
print(f"Restaurando desde: {backup_file}")

with open(backup_file, 'r') as f:
    result = subprocess.run(
        [f"{MYSQL_PATH}\\mysql", f"-u{MYSQL_USER}", f"-p{MYSQL_PASSWORD}", DATABASE_NAME],
        stdin=f
    )

if result.returncode == 0:
    print("Base de datos restaurada correctamente")
else:
    print("Error al restaurar la base de datos")