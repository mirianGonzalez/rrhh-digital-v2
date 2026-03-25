import os
import hashlib
from datetime import datetime

from docxtpl import DocxTemplate
from docx2pdf import convert
import qrcode


PLANTILLA = "BASE_DATOS/plantillas/plantilla_ddjj_posadas.docx"
CARPETA_DOCS = "documentos"


def generar_hash(legajo):
    texto = legajo + str(datetime.now())
    return hashlib.sha256(texto.encode()).hexdigest()[:16]


def generar_qr(hash_doc):

    url = f"http://127.0.0.1:5000/validar/{hash_doc}"

    ruta_qr = f"{CARPETA_DOCS}/qr_{hash_doc}.png"

    img = qrcode.make(url)
    img.save(ruta_qr)

    return ruta_qr


def generar_ddjj(contexto):

    if not os.path.exists(CARPETA_DOCS):
        os.makedirs(CARPETA_DOCS)

    legajo = str(contexto["legajo"])
    anio = str(contexto["anio"])

    hash_doc = generar_hash(legajo)

    qr = generar_qr(hash_doc)

    contexto["hash_documento"] = hash_doc
    contexto["qr_validacion"] = qr

    for i in range(1, 8):

        clave = f"f{i}"

        if clave not in contexto:
            contexto[clave] = {
                "apellido": "",
                "par": "",
                "convive": "",
                "fe_nac": "",
                "ed": "",
                "dni": "",
                "ni": "",
                "pri": "",
                "sec": "",
                "ter": "",
            }

    for i in range(1, 7):

        for campo in [
            "apellido",
            "parentesco",
            "convive",
            "fecha_nac",
            "dni",
            "observacion",
        ]:

            clave = f"ph_{i}_{campo}"

            if clave not in contexto:
                contexto[clave] = ""

    plantilla = DocxTemplate(PLANTILLA)

    plantilla.render(contexto)

    archivo_docx = f"{CARPETA_DOCS}/DDJJ_{legajo}_{anio}.docx"

    plantilla.save(archivo_docx)

    archivo_pdf = f"{CARPETA_DOCS}/DDJJ_{legajo}_{anio}.pdf"

    convert(archivo_docx, archivo_pdf)

    return archivo_pdf, hash_doc