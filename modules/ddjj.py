from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash, session
from pdf.generar_ddjj import generar_ddjj
import sqlite3

ddjj_bp = Blueprint("ddjj", __name__)

DB = "BASE_DATOS/legajos_agentes.db"


# =========================
# CONEXIÓN DB
# =========================

def obtener_conexion():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


# =========================
# FORMULARIO DDJJ
# =========================

@ddjj_bp.route("/formulario_ddjj/<int:legajo_id>")
def formulario_ddjj(legajo_id):

    # Si no hay sesión, volver al panel
    if "usuario_id" not in session:
        return redirect("/panel_rrhh")

    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute(
        "SELECT apellido_nombre, dni FROM agentes WHERE id=?",
        (legajo_id,)
    )

    agente = cur.fetchone()

    conn.close()

    if not agente:
        return "Agente no encontrado"

    return render_template(
        "formulario_ddjj.html",
        legajo_id=legajo_id,
        agente=agente
    )


# =========================
# GENERAR / PREVIEW PDF
# =========================

@ddjj_bp.route("/preview_ddjj", methods=["POST"])
def preview_ddjj():

    if "usuario_id" not in session:
        return redirect("/panel_rrhh")

    datos = request.form.to_dict()

    legajo_id = int(datos.get("legajo_id"))

    pdf = generar_ddjj(datos, legajo_id)

    return send_file(pdf)


# =========================
# ENVIAR DEFINITIVO
# =========================

@ddjj_bp.route("/enviar_ddjj/<int:legajo_id>", methods=["POST"])
def enviar_ddjj(legajo_id):

    if "usuario_id" not in session:
        return redirect("/panel_rrHH")

    conn = obtener_conexion()
    cur = conn.cursor()

    cur.execute("""
        UPDATE agentes
        SET estado_ddjj='FINALIZADO'
        WHERE id=?
    """, (legajo_id,))

    conn.commit()
    conn.close()

    flash("Declaración Jurada enviada correctamente")

    return redirect(
        url_for("ddjj.formulario_ddjj", legajo_id=legajo_id)
    )