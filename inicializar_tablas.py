import sqlite3
import os

# Rutas de bases de datos
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

# Tabla ddjj_agentes
cur.execute("""
CREATE TABLE IF NOT EXISTS ddjj_agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    hash_documento TEXT,
    qr_validacion TEXT,
    f1_nombre TEXT,
    f1_apellido TEXT,
    f2_nombre TEXT,
    f2_apellido TEXT,
    ph1_nombre TEXT,
    ph1_apellido TEXT,
    ph2_nombre TEXT,
    ph2_apellido TEXT
    -- Agregá aquí más columnas según tu estructura de DDJJ
)
""")

conn.commit()
conn.close()
print("Tablas en ddjj.db creadas o verificadas ✅")