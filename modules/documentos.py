from flask import Blueprint, request, redirect, send_from_directory
import os
from database import get_db

documentos_bp = Blueprint("documentos", __name__)

UPLOAD_FOLDER = "DOCUMENTOS_AGENTES"


@documentos_bp.route("/subir_documento/<legajo>", methods=["POST"])
def subir_documento(legajo):

    archivo = request.files["archivo"]
    tipo = request.form["tipo"]

    if archivo.filename == "":
        return "Archivo inválido"

    nombre = f"{legajo}_{tipo}_{archivo.filename}"

    ruta = os.path.join(UPLOAD_FOLDER, nombre)

    archivo.save(ruta)

    db = get_db()

    db.execute(
        """
        INSERT INTO documentos
        (legajo,tipo,archivo)
        VALUES (?,?,?)
        """,
        (legajo,tipo,nombre)
    )

    db.commit()

    return redirect(f"/legajo/{legajo}")


# @documentos_bp.route("/descargar/<tipo>/<legajo>")
# def descargar(tipo, legajo):
#
#     db = get_db()
#
#     doc = db.execute(
#         """
#         SELECT archivo
#         FROM documentos
#         WHERE legajo=? AND tipo=?
#         ORDER BY id DESC
#         """,
#         (legajo,tipo)
#     ).fetchone()
#
#     if not doc:
#         return "Documento no encontrado"
#
#     return send_from_directory(
#         UPLOAD_FOLDER,
#         doc["archivo"],
#         as_attachment=True
#     )