# ======================================
# MÓDULO PARA GENERAR PDF DDJJ DESDE PLANTILLA
# ======================================

import sys
import os
import sqlite3

# -----------------------------
# Asegurar que Python encuentre pdf/
# -----------------------------
ruta_pdf = r"G:\Mi unidad\RRHH_DIGITAL\pdf"
if ruta_pdf not in sys.path:
    sys.path.append(ruta_pdf)

# -----------------------------
# Librerías externas
# -----------------------------
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from docx2pdf import convert

# -----------------------------
# Módulos propios
# -----------------------------
from generar_qr import generar_qr
from hash_documentos import generar_hash

# -----------------------------
# Ruta base de la base de datos
# -----------------------------
DB_PATH = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\ddjj.db"

# ===========================
# Función para insertar/actualizar DDJJ en DB
# ===========================
def guardar_ddjj_en_db(ddjj_dict: dict):
    """
    Inserta o actualiza un DDJJ en la base de datos ddjj.db
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Preparar campos: f1-f7
    campos = {}
    for i in range(1, 8):
        f = ddjj_dict.get(f"f{i}", {})
        for k, v in f.items():
            campos[f"f{i}_{k}"] = v

    # Preparar campos: ph1-ph6
    for i in range(1, 7):
        ph = ddjj_dict.get(f"ph{i}", {})
        for k, v in ph.items():
            campos[f"ph{i}_{k}"] = v

    # Campos principales
    for k, v in ddjj_dict.items():
        if not k.startswith("f") and not k.startswith("ph"):
            campos[k] = v

    # Verificar si ya existe (legajo + año)
    cur.execute("SELECT id FROM ddjj_agentes WHERE legajo=? AND anio=?", 
                (ddjj_dict["legajo"], ddjj_dict["anio"]))
    row = cur.fetchone()
    
    if row:
        # UPDATE
        set_clause = ", ".join([f"{k}=?" for k in campos.keys()])
        sql = f"UPDATE ddjj_agentes SET {set_clause} WHERE id={row[0]}"
        cur.execute(sql, tuple(campos.values()))
    else:
        # INSERT
        columnas = ", ".join(campos.keys())
        placeholders = ", ".join(["?"] * len(campos))
        sql = f"INSERT INTO ddjj_agentes ({columnas}) VALUES ({placeholders})"
        cur.execute(sql, tuple(campos.values()))
    
    conn.commit()


# ===========================
# Función principal para generar DDJJ
# ===========================
def generar_ddjj(ddjj_dict: dict, plantilla_path: str, salida_docx: str, salida_pdf: str):
    """
    Genera un PDF DDJJ desde plantilla .docx usando diccionario de datos.
    También genera hash y QR y guarda en base de datos.
    """
    # 1️⃣ Crear hash del documento
    hash_doc = generar_hash(str(ddjj_dict))
    ddjj_dict["hash_documento"] = hash_doc

    # 2️⃣ Generar QR
    qr_path = salida_docx.replace(".docx", "_qr.png")
    generar_qr(hash_doc, qr_path)
    ddjj_dict["qr_validacion"] = qr_path

    # 3️⃣ Rellenar plantilla
    doc = DocxTemplate(plantilla_path)
    # Incluir imagen QR
    ddjj_dict["qr_image"] = InlineImage(doc, qr_path, width=Mm(30))
    doc.render(ddjj_dict)
    doc.save(salida_docx)

    # 4️⃣ Convertir a PDF
    convert(salida_docx, salida_pdf)

    # 5️⃣ Guardar DDJJ en base de datos
    guardar_ddjj_en_db(ddjj_dict)



