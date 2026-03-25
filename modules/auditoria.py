from flask import Blueprint, render_template
from database import get_db

auditoria_bp = Blueprint("auditoria", __name__)

@auditoria_bp.route("/auditoria")
def ver_auditoria():

    db = get_db()

    registros = db.execute(
        """
        SELECT *
        FROM auditoria
        ORDER BY fecha DESC
        """
    ).fetchall()

    return render_template(
        "auditoria.html",
        registros=registros
    )