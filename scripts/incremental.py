import os
import subprocess
from datetime import datetime


MYSQL_USER = "root"
MYSQL_PASSWORD = ""
DATABASE_NAME = "test_backup"
MYSQL_PATH = r"C:\Program Files\MySQL\MySQL Server 8.0\bin"
BACKUP_DIR = r"C:\BackupsMySQL"

os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_incremental():
    cmd = [
        f"{MYSQL_PATH}\\mysql",
        f"-u{MYSQL_USER}",
        f"-p{MYSQL_PASSWORD}",
        "-e", "SHOW MASTER STATUS\\G"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error al obtener el binlog actual")
        return

    output = result.stdout
    binlog_file = None
    for line in output.splitlines():
        if "mysql-bin" in line:
            binlog_file = line.split(":")[-1].strip()
            break

    if not binlog_file:
        print("No se encontró el binlog activo")
        return

    # Crear archivo incremental
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_DIR, f"INCREMENTAL_{date_str}.sql")

    cmd = [f"{MYSQL_PATH}\\mysqlbinlog", binlog_file]
    with open(backup_file, "w", encoding="utf-8") as f:
        result = subprocess.run(cmd, stdout=f)

    if result.returncode == 0:
        print(f"Backup incremental creado: {backup_file}")
    else:
        print("Error al crear el backup incremental")

backup_incremental()
