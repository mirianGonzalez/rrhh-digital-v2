import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, send_file
from database import get_db
from config import DOCUMENTOS_PATH


legajos_bp = Blueprint("legajos", __name__)


# =====================================================
# LISTA DE LEGAJOS
# =====================================================

@legajos_bp.route("/legajos")
def lista_legajos():

    db = get_db()

    agentes = db.execute(
        "SELECT * FROM agentes ORDER BY nombre"
    ).fetchall()

    return render_template("legajo_lista.html", agentes=agentes)


# =====================================================
# BUSCAR AGENTE
# =====================================================

@legajos_bp.route("/buscar_agente", methods=["POST"])
def buscar_agente():

    texto = request.form["buscar"]

    db = get_db()

    agentes = db.execute(
        """
        SELECT * FROM agentes
        WHERE nombre LIKE ?
        OR dni LIKE ?
        OR legajo LIKE ?
        LIMIT 50
        """,
        (f"%{texto}%", f"%{texto}%", f"%{texto}%")
    ).fetchall()

    return render_template("legajo_lista.html", agentes=agentes)


# =====================================================
# CREAR AGENTE
# =====================================================

@legajos_bp.route("/crear_agente", methods=["GET", "POST"])
def crear_agente():

    if request.method == "POST":

        legajo = request.form["legajo"]
        nombre = request.form["nombre"]
        dni = request.form["dni"]
        cuil = request.form["cuil"]
        cargo = request.form["cargo"]
        dependencia = request.form["dependencia"]

        db = get_db()

        db.execute("""
        INSERT INTO agentes
        (legajo,nombre,dni,cuil,cargo,dependencia,estado)
        VALUES (?,?,?,?,?,?,?)
        """,
        (legajo, nombre, dni, cuil, cargo, dependencia, "ACTIVO"))

        db.commit()

        carpeta = os.path.join(DOCUMENTOS_PATH, str(legajo))
        os.makedirs(carpeta, exist_ok=True)

        return redirect("/legajos")

    return render_template("crear_agente.html")


# =====================================================
# VER LEGAJO
# =====================================================

@legajos_bp.route("/legajo/<legajo>")
def ver_legajo(legajo):

    db = get_db()

    agente = db.execute(
        "SELECT * FROM agentes WHERE legajo=?",
        (legajo,)
    ).fetchone()

    documentos = db.execute("""

    SELECT
        dr.id,
        dr.tipo_documento,
        dr.obligatorio,

        d.id as id_doc,
        d.archivo,
        d.fecha,
        d.estado

    FROM documentos_requeridos dr

    LEFT JOIN documentos d
        ON d.tipo = dr.tipo_documento
        AND d.legajo = ?
        AND d.estado = 'ACTIVO'

    ORDER BY dr.id

    """, (legajo,)).fetchall()

    total = len(documentos)
    cargados = 0
    faltantes = []

    for doc in documentos:

        if doc["archivo"]:
            cargados += 1

        elif doc["obligatorio"] == 1:
            faltantes.append(doc["tipo_documento"])

    porcentaje = int((cargados / total) * 100)

    legajo_completo = len(faltantes) == 0

    return render_template(
        "legajo.html",
        agente=agente,
        documentos=documentos,
        faltantes=faltantes,
        legajo_completo=legajo_completo,
        porcentaje=porcentaje
    )


# =====================================================
# SUBIR DOCUMENTO
# =====================================================

@legajos_bp.route("/subir_documento/<legajo>/<tipo>", methods=["POST"])
def subir_documento(legajo, tipo):

    archivo = request.files.get("archivo")

    if not archivo or archivo.filename == "":
        return redirect(f"/legajo/{legajo}")

    extension = archivo.filename.split(".")[-1].lower()

    nombre_archivo = f"{tipo}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{extension}"

    carpeta = os.path.join(DOCUMENTOS_PATH, str(legajo))
    os.makedirs(carpeta, exist_ok=True)

    ruta = os.path.join(carpeta, nombre_archivo)

    archivo.save(ruta)

    db = get_db()

    # AUTO ANULAR DOCUMENTO ANTERIOR
    db.execute(
        """
        UPDATE documentos
        SET estado='ANULADO'
        WHERE legajo=? AND tipo=? AND estado='ACTIVO'
        """,
        (legajo, tipo)
    )

    # INSERTAR DOCUMENTO NUEVO
    db.execute("""
    INSERT INTO documentos
    (legajo,tipo,archivo,fecha,estado)
    VALUES (?,?,?,?,?)
    """,
    (legajo, tipo, nombre_archivo, datetime.now(), "ACTIVO"))

    db.commit()

    return redirect(f"/legajo/{legajo}")


# =====================================================
# DESCARGAR DOCUMENTO
# =====================================================

@legajos_bp.route("/descargar/<legajo>/<archivo>")
def descargar_documento(legajo, archivo):

    carpeta = os.path.join(DOCUMENTOS_PATH, str(legajo))
    ruta = os.path.join(carpeta, archivo)

    if not os.path.exists(ruta):
        return f"Documento no encontrado: {ruta}"

    return send_file(ruta, as_attachment=True)


# =====================================================
# VER DOCUMENTO
# =====================================================

@legajos_bp.route("/ver/<legajo>/<archivo>")
def ver_documento(legajo, archivo):

    carpeta = os.path.join(DOCUMENTOS_PATH, str(legajo))
    ruta = os.path.join(carpeta, archivo)

    return send_file(ruta)


# =====================================================
# ANULAR DOCUMENTO
# =====================================================

@legajos_bp.route("/anular/<int:id_doc>")
def anular_documento(id_doc):

    db = get_db()

    doc = db.execute(
        "SELECT legajo FROM documentos WHERE id=?",
        (id_doc,)
    ).fetchone()

    if not doc:
        return "Documento inexistente"

    db.execute(
        "UPDATE documentos SET estado='ANULADO' WHERE id=?",
        (id_doc,)
    )

    db.commit()

    return redirect(f"/legajo/{doc['legajo']}")


# =====================================================
# HISTORIAL DOCUMENTO
# =====================================================

@legajos_bp.route("/historial/<legajo>/<tipo>")
def historial_documento(legajo, tipo):

    db = get_db()

    historial = db.execute(
        """
        SELECT archivo, fecha, estado
        FROM documentos
        WHERE legajo=? AND tipo=?
        ORDER BY fecha DESC
        """,
        (legajo, tipo)
    ).fetchall()

    return render_template(
        "historial.html",
        documentos=historial,
        legajo=legajo,
        tipo=tipo
    )


# =====================================================
# HISTORIAL COMPLETO DEL LEGAJO
# =====================================================

@legajos_bp.route("/historial_legajo/<legajo>")
def historial_legajo(legajo):

    db = get_db()

    historial = db.execute("""
    SELECT tipo, archivo, fecha, estado
    FROM documentos
    WHERE legajo=?
    ORDER BY fecha DESC
    """, (legajo,)).fetchall()

    return render_template(
        "historial_legajo.html",
        documentos=historial,
        legajo=legajo
    )


# =====================================================
# PANEL INTELIGENTE RRHH
# =====================================================

@legajos_bp.route("/panel_rrhh")
def panel_rrhh():

    db = get_db()

    # TOTAL DE AGENTES
    total_agentes = db.execute("""
        SELECT COUNT(*) as total
        FROM agentes
    """).fetchone()["total"]

    # DOCUMENTOS ANULADOS
    anulados = db.execute("""
        SELECT legajo,tipo,archivo,fecha
        FROM documentos
        WHERE estado='ANULADO'
        ORDER BY fecha DESC
        LIMIT 10
    """).fetchall()

    total_anulados = db.execute("""
        SELECT COUNT(*) as total
        FROM documentos
        WHERE estado='ANULADO'
    """).fetchone()["total"]

    # DOCUMENTOS FALTANTES OBLIGATORIOS
    faltantes = db.execute("""
    SELECT a.legajo, a.nombre, dr.tipo_documento
    FROM agentes a
    CROSS JOIN documentos_requeridos dr
    LEFT JOIN documentos d
        ON d.legajo = a.legajo
        AND d.tipo = dr.tipo_documento
        AND d.estado='ACTIVO'
    WHERE dr.obligatorio=1
    AND d.id IS NULL
    ORDER BY a.legajo
    """).fetchall()

    total_faltantes = len(faltantes)

    # LEGAJOS INCOMPLETOS
    legajos_incompletos = db.execute("""
    SELECT DISTINCT a.legajo, a.nombre
    FROM agentes a
    CROSS JOIN documentos_requeridos dr
    LEFT JOIN documentos d
        ON d.legajo = a.legajo
        AND d.tipo = dr.tipo_documento
        AND d.estado='ACTIVO'
    WHERE dr.obligatorio=1
    AND d.id IS NULL
    """).fetchall()

    total_incompletos = len(legajos_incompletos)

    return render_template(
        "panel_rrhh.html",
        total_agentes=total_agentes,
        total_anulados=total_anulados,
        total_faltantes=total_faltantes,
        total_incompletos=total_incompletos,
        anulados=anulados,
        faltantes=faltantes,
        incompletos=legajos_incompletos
    )