# ======================================
# inicializar_db.py
# Script para crear bases y tablas necesarias
# ======================================

import sqlite3
import os

# -----------------------------
# Rutas de bases de datos
# -----------------------------
BASE_PATH = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS"
LEG_DB = os.path.join(BASE_PATH, "legajos_agentes.db")
DDJJ_DB = os.path.join(BASE_PATH, "ddjj.db")

# -----------------------------
# Crear carpeta si no existe
# -----------------------------
os.makedirs(BASE_PATH, exist_ok=True)

# ==========================
# Crear tabla 'agentes'
# ==========================
conn = sqlite3.connect(LEG_DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo TEXT NOT NULL UNIQUE,
    apellido_nombre TEXT,
    fecha_nacimiento TEXT,
    dni TEXT,
    categoria TEXT,
    fecha_ingreso TEXT
)
""")

conn.commit()
conn.close()
print("Tabla 'agentes' creada ✅")

# ==========================
# Crear tabla 'ddjj_agentes'
# ==========================
conn = sqlite3.connect(DDJJ_DB)
cur = conn.cursor()

# Lista de campos f1-f7 y ph1-ph6
campos_f = []
for i in range(1, 8):
    campos_f.extend([
        f"f{i}_apellido", f"f{i}_par", f"f{i}_convive", f"f{i}_fe_nac",
        f"f{i}_ed", f"f{i}_dni", f"f{i}_ni", f"f{i}_pri", f"f{i}_sec", f"f{i}_ter"
    ])

campos_ph = []
for i in range(1, 7):
    campos_ph.extend([
        f"ph{i}_apellido", f"ph{i}_parentesco", f"ph{i}_convive",
        f"ph{i}_fecha_nac", f"ph{i}_dni", f"ph{i}_observacion"
    ])

# Campos principales DDJJ
campos_principales = [
    "anio", "legajo", "apellido_nombre", "fecha_nacimiento", "lugar_nacimiento", "dni",
    "estado_civil", "estudios_completos", "estudios_incompletos", "primario", "secundario",
    "terciario", "universitario", "titulo", "anios_cursados",
    "domicilio_barrio", "domicilio_chacra", "domicilio_calle", "domicilio_numero",
    "domicilio_piso", "domicilio_depto", "domicilio_localidad", "telefono_fijo",
    "telefono_celular", "email", "telefono_referencia", "nombre_referencia",
    "parentesco_referencia", "fecha_ingr", "categ", "antig", "p_permanente", "p_temporaria",
    "lugar_dependencia", "actividad_realiza_dependencia", "enfermedad_preexistente",
    "vacuna_covid_dosis", "vacuna_gripe", "vacuna_neumonia",
    "percibe_asig_fliares_hcd", "servicios_anteriores", "antiguedad_servicios",
    "trabaja_otra_reparticion", "otra_reparticion_donde", "percibe_asig_fliares_otro",
    "soltero", "casado", "divorciado", "separado", "viudo", "conviviente",
    "conyuge_apellido_nombre", "conyuge_dni", "conyuge_fecha_enlace", "conyuge_lugar_enlace",
    "conyuge_trabaja", "conyuge_razon_social", "conyuge_percibe_asignaciones",
    "conyuge_observaciones",
    "lugar_declaracion", "fecha_declaracion", "sello_firma_director",
    "sello_organismo", "firma_agente", "sello_firma_director2",
    "sello_organismo2", "firma_agente2", "qr_validacion", "hash_documento"
]

# Unir todos los campos
todos_campos = campos_principales + campos_f + campos_ph

# Crear SQL dinámico
columnas_sql = ", ".join([f"{c} TEXT" for c in todos_campos])
sql = f"""
CREATE TABLE IF NOT EXISTS ddjj_agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    {columnas_sql}
)
"""

cur.execute(sql)
conn.commit()
conn.close()
print("Tabla 'ddjj_agentes' creada ✅")

print("¡Bases de datos inicializadas correctamente! 🎉")