import sqlite3
import os

DB_PATH = os.path.join("data", "db", "asistente_datos.db")

def mostrar_registros():
    if not os.path.exists(DB_PATH):
        print("❌ La base de datos no existe.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre_original, ruta_guardado, tamano_bytes, timestamp FROM archivos ORDER BY timestamp DESC")
    filas = cursor.fetchall()

    if not filas:
        print("📭 No hay registros.")
    else:
        print("📋 Registros en la tabla archivos:")
        for fila in filas:
            print(f"🗂️ ID: {fila[0]} | Nombre: {fila[1]} | Tamaño: {fila[3]} bytes | Fecha: {fila[4]}")

    conn.close()

if __name__ == "__main__":
    mostrar_registros()
