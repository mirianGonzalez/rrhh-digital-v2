from database import get_db
import sqlite3

db = get_db()

documentos = [

("dni_frente",1),
("dni_dorso",1),
("partida_nacimiento",1),
("cuil",1),
("foto_4x4",1),
("matrimonio_convivencia",0),
("hijos_nacimientos",0),
("alumno_regular",0),
("titulo_secundario",1),
("titulo_terciario_universitario",0),
("certificado_analitico_titulo",1),
("croquis_domicilio",1),
("telefono",1),
("correo_electronico",1),
("telefono_referencia",0),
("parentesco_referencia",0),
("ddjj_anual",1),
("seguro_vida",1),
("servicios_anteriores",0),
("cert_medico_aptitud_psicofisico",1),
("cert_obra_social_ips",1),
("autoridad_diploma_electoral_decreto",0),
("contrato",0),
("contrato_nominado",0),
("decreto_designacion",1),
("pase_planta_permanente",0),
("licencias",0),
("cortes_licencia",0),
("franquicias",0),
("sanciones",0),
("resoluciones",0),
("circulares",0),
("memorandum",0)

]

for d in documentos:

    db.execute(
        "INSERT OR IGNORE INTO documentos_requeridos (tipo_documento, obligatorio) VALUES (?,?)",
        d
    )

db.commit()

print("✔ Requisitos oficiales del legajo cargados correctamente")



conn = sqlite3.connect("BASE_DATOS/legajos.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS ddjj (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    legajo INTEGER,
    archivo TEXT,
    fecha TEXT,
    estado TEXT
)
""")

conn.commit()
conn.close()

print("Tabla DDJJ creada")