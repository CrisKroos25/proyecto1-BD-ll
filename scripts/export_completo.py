import subprocess
import os
from datetime import datetime

MYSQL_USER = "root"
MYSQL_PASSWORD = ""
DATABASE_NAME = "tienda"
MYSQL_PATH = r"C:\Program Files\MySQL\MySQL Server 8.0\bin"
BACKUP_DIR = r"D:\BackupsMySQL"

os.makedirs(BACKUP_DIR, exist_ok=True)

date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = os.path.join(BACKUP_DIR, f"{DATABASE_NAME}_{date_str}.sql")

export_cmd = f'"{MYSQL_PATH}\\mysqldump" -u {MYSQL_USER} -p{MYSQL_PASSWORD} {DATABASE_NAME} > "{backup_file}"'
result = subprocess.run(export_cmd, shell=True)

if result.returncode == 0:
    print(f"Backup creado correctamente: {backup_file}")
else:
    print("Error al crear el backup")