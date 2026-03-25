# ==============================================
# SETUP COMPLETO RRHH_DIGITAL: BASE + DDJJ + PDF
# ==============================================
import os
import sqlite3
from datetime import datetime

# ----------------------------
# Rutas
# ----------------------------
BASE_DB = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\legajos.db"
DDJJ_DB = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\ddjj.db"
PLANTILLA_DDJJ = r"G:\Mi unidad\RRHH_DIGITAL\PLANTILLAS\plantilla_ddjj.docx"
SALIDA_DOCX = r"G:\Mi unidad\RRHH_DIGITAL\DOCUMENTOS_AGENTES\1001\ddjj_prueba.docx"
SALIDA_PDF = r"G:\Mi unidad\RRHH_DIGITAL\DOCUMENTOS_AGENTES\1001\ddjj_prueba.pdf"

# ----------------------------
# Asegurar directorios
# ----------------------------
os.makedirs(os.path.dirname(SALIDA_DOCX), exist_ok=True)

# ----------------------------
# Import PDF modules
# ----------------------------
import sys
ruta_pdf = r"G:\Mi unidad\RRHH_DIGITAL\pdf"
if ruta_pdf not in sys.path:
    sys.path.append(ruta_pdf)

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert
from generar_qr import generar_qr
from hash_documentos import generar_hash

# ===========================
# CREAR TABLAS LEGALOGOS
# ===========================
conn = sqlite3.connect(BASE_DB)
cur = conn.cursor()

# ----------------------------    
# Tabla agentes
cur.execute("""
CREATE TABLE IF NOT EXISTS agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo INTEGER UNIQUE,
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
    legajo INTEGER,
    documento TEXT,
    fecha_actualizacion TEXT
)
""")

conn.commit()
conn.close()

# ===========================
# CREAR TABLA DDJJ_AGENTES con f1-f7, ph1-ph6
# ===========================
conn = sqlite3.connect(DDJJ_DB)
cur = conn.cursor()

# Construir columnas f1-f7
cols_f = ", ".join([f"f{i}_campo1 TEXT, f{i}_campo2 TEXT, f{i}_campo3 TEXT" for i in range(1, 8)])
cols_ph = ", ".join([f"ph{i}_campo1 TEXT, ph{i}_campo2 TEXT" for i in range(1, 7)])

# Campos principales adicionales
campos_principales = """
legajo INTEGER,
anio INTEGER,
hash_documento TEXT,
qr_validacion TEXT
"""

sql_ddjj = f"""
CREATE TABLE IF NOT EXISTS ddjj_agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    {campos_principales},
    {cols_f},
    {cols_ph}
)
"""

cur.execute(sql_ddjj)
conn.commit()
conn.close()

# ===========================
# INSERTAR AGENTE DE PRUEBA
# ===========================
conn = sqlite3.connect(BASE_DB)
cur = conn.cursor()

cur.execute("INSERT OR IGNORE INTO agentes (legajo, nombre, dni, cuil, cargo, dependencia, estado) VALUES (?,?,?,?,?,?,?)",
            (1001, "Juan Perez", "12345678", "20-12345678-9", "Analista", "RRHH", "Activo"))
conn.commit()
conn.close()

# ===========================
# INSERTAR DDJJ DE PRUEBA
# ===========================
ddjj_dict = {
    "legajo": 1001,
    "anio": datetime.now().year,
}

# Llenar f1-f7 y ph1-ph6 con datos ficticios
for i in range(1, 8):
    ddjj_dict[f"f{i}"] = {"campo1": f"F{i}1", "campo2": f"F{i}2", "campo3": f"F{i}3"}
for i in range(1, 7):
    ddjj_dict[f"ph{i}"] = {"campo1": f"PH{i}1", "campo2": f"PH{i}2"}

# ----------------------------
# Generar hash y QR
# ----------------------------
hash_doc = generar_hash(str(ddjj_dict))
ddjj_dict["hash_documento"] = hash_doc
qr_path = SALIDA_DOCX.replace(".docx", "_qr.png")
generar_qr(hash_doc, qr_path)
ddjj_dict["qr_validacion"] = qr_path
ddjj_dict["qr_image"] = None  # se asigna en doc.render

# ----------------------------
# Generar PDF DDJJ desde plantilla
# ----------------------------
doc = DocxTemplate(PLANTILLA_DDJJ)
from copy import deepcopy
ddjj_render = deepcopy(ddjj_dict)
ddjj_render["qr_image"] = InlineImage(doc, qr_path, width=Mm(30))
doc.render(ddjj_render)
doc.save(SALIDA_DOCX)
convert(SALIDA_DOCX, SALIDA_PDF)

# ----------------------------
# Guardar DDJJ en base de datos
# ----------------------------
conn = sqlite3.connect(DDJJ_DB)
cur = conn.cursor()

# Preparar campos planos
campos = {}
for i in range(1, 8):
    f = ddjj_dict.get(f"f{i}", {})
    for k, v in f.items():
        campos[f"f{i}_{k}"] = v
for i in range(1, 7):
    ph = ddjj_dict.get(f"ph{i}", {})
    for k, v in ph.items():
        campos[f"ph{i}_{k}"] = v
for k, v in ddjj_dict.items():
    if not k.startswith("f") and not k.startswith("ph"):
        campos[k] = v

columnas = ", ".join(campos.keys())
placeholders = ", ".join(["?"] * len(campos))
sql = f"INSERT INTO ddjj_agentes ({columnas}) VALUES ({placeholders})"
cur.execute(sql, tuple(campos.values()))
conn.commit()
conn.close()

print("=== SETUP COMPLETO FINALIZADO ✅ ===")
print("Agente de prueba y DDJJ generados con PDF + QR.")