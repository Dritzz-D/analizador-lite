# scripts/inicializar_db.py
import sqlite3
import os

DB_PATH = os.path.join("data", "db", "asistente_datos.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS archivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_original TEXT,
    ruta_guardado TEXT,
    tamano_bytes INTEGER,
    formato TEXT,
    proyecto TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()
print("✅ Base de datos inicializada correctamente en", DB_PATH)

