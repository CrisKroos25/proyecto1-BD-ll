# save_full_marker.py
import subprocess, os

MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_PATH = r"C:\Program Files\MySQL\MySQL Server 8.0\bin"
BACKUP_DIR = r"D:\BackupsMySQL"

os.makedirs(BACKUP_DIR, exist_ok=True)
MARKER_PATH = os.path.join(BACKUP_DIR, "full_marker.txt")

cmd = f'"{MYSQL_PATH}\\mysql" -u {MYSQL_USER} -p{MYSQL_PASSWORD} -e "SHOW MASTER STATUS;"'
res = subprocess.run(cmd, shell=True, capture_output=True, text=True)

if res.returncode != 0:
    print(" Error al leer MASTER STATUS")
    print(res.stderr)
    raise SystemExit(1)

lines = [l for l in res.stdout.splitlines() if l.strip()]
if len(lines) < 2:
    print("❌ No hay binlog activo (¿está habilitado log_bin?)")
    raise SystemExit(1)

# Encabezado: File  Position  Binlog_Do_DB  Binlog_Ignore_DB  Executed_Gtid_Set
# Tomamos la primera fila de datos
parts = lines[1].split()
binlog_file = parts[0]
binlog_pos  = parts[1]

with open(MARKER_PATH, "w", encoding="utf-8") as f:
    f.write(f"{binlog_file} {binlog_pos}\n")

print(f"Marcador FULL guardado en {MARKER_PATH}: {binlog_file} @ {binlog_pos}")
