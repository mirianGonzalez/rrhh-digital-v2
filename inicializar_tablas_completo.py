import sqlite3
import os

# ==========================
# Rutas de bases de datos
# ==========================
ruta_legajos = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\legajos.db"
ruta_ddjj = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\ddjj.db"

# ==========================
# Crear tablas en legajos.db
# ==========================
conn = sqlite3.connect(ruta_legajos)
cur = conn.cursor()

# Tabla agentes
cur.execute("""
CREATE TABLE IF NOT EXISTS agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo INTEGER NOT NULL,
    nombre TEXT,
    dni TEXT,
    cuil TEXT,
    cargo TEXT,
    dependencia TEXT,
    estado TEXT,
    estado_ddjj TEXT DEFAULT 'pendiente'
)
""")

# Tabla documentos_faltantes
cur.execute("""
CREATE TABLE IF NOT EXISTS documentos_faltantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo INTEGER NOT NULL,
    documento TEXT,
    fecha_falta TEXT
)
""")

conn.commit()
conn.close()
print("Tablas en legajos.db creadas o verificadas ✅")

# ==========================
# Crear tablas en ddjj.db
# ==========================
conn = sqlite3.connect(ruta_ddjj)
cur = conn.cursor()

# Crear tabla ddjj_agentes con columnas f1-f7 y ph1-ph6
campos_f = []
for i in range(1, 8):
    campos_f.append(f"f{i}_nombre TEXT")
    campos_f.append(f"f{i}_apellido TEXT")
    campos_f.append(f"f{i}_dni TEXT")
    campos_f.append(f"f{i}_parentesco TEXT")

campos_ph = []
for i in range(1, 7):
    campos_ph.append(f"ph{i}_nombre TEXT")
    campos_ph.append(f"ph{i}_apellido TEXT")
    campos_ph.append(f"ph{i}_dni TEXT")
    campos_ph.append(f"ph{i}_parentesco TEXT")

# Columnas principales de DDJJ
campos_principales = [
    "legajo INTEGER NOT NULL",
    "anio INTEGER NOT NULL",
    "hash_documento TEXT",
    "qr_validacion TEXT",
    "fecha_presentacion TEXT",
    "observaciones TEXT"
]

# Combinar todos los campos
todos_campos = campos_principales + campos_f + campos_ph

# Crear tabla
cur.execute(f"""
CREATE TABLE IF NOT EXISTS ddjj_agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    {', '.join(todos_campos)}
)
""")

conn.commit()
conn.close()
print("Tabla ddjj_agentes creada o verificada ✅")

# ==========================
# Mensaje final
# ==========================
print("\n✅ Base de datos inicializada completamente. Ahora podés arrancar app.py sin errores.")