# ======================================
# actualizar_tablas.py
# Agrega columnas necesarias a 'agentes'
# ======================================

import sqlite3
import os

BASE_PATH = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS"
LEG_DB = os.path.join(BASE_PATH, "legajos_agentes.db")

conn = sqlite3.connect(LEG_DB)
cur = conn.cursor()

# Lista de columnas nuevas esperadas por app.py
nuevas_columnas = {
    "estado_legajo": "TEXT",
    "documentos_completos": "INTEGER",
    "documentos_faltantes": "INTEGER",
    "fecha_actualizacion": "TEXT"
}

for col, tipo in nuevas_columnas.items():
    try:
        cur.execute(f"ALTER TABLE agentes ADD COLUMN {col} {tipo}")
        print(f"Columna '{col}' agregada ✅")
    except sqlite3.OperationalError:
        print(f"Columna '{col}' ya existe, se omite ✅")

conn.commit()
conn.close()
print("¡Tabla 'agentes' actualizada correctamente! 🎉")
