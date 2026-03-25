# ==========================================
# CREACIÓN BASE DE DATOS DDJJ
# ==========================================

import sqlite3
import os

# Ruta absoluta de la base de datos
ruta_db = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\ddjj.db"

# Asegurarnos que la carpeta exista
os.makedirs(os.path.dirname(ruta_db), exist_ok=True)

# Conectar a la base (SQLite la crea si no existe)
conn = sqlite3.connect(ruta_db)
cur = conn.cursor()

# Crear tabla completa de Declaración Jurada
cur.execute("""
CREATE TABLE IF NOT EXISTS ddjj_agentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    anio INTEGER,
    legajo TEXT,
    apellido_nombre TEXT,
    fecha_nacimiento TEXT,
    lugar_nacimiento TEXT,
    dni TEXT,
    estado_civil TEXT,
    estudios_completos INTEGER,
    estudios_incompletos INTEGER,
    primario INTEGER,
    secundario INTEGER,
    terciario INTEGER,
    universitario INTEGER,
    titulo TEXT,
    anios_cursados INTEGER,
    domicilio_barrio TEXT,
    domicilio_chacra TEXT,
    domicilio_calle TEXT,
    domicilio_numero TEXT,
    domicilio_piso TEXT,
    domicilio_depto TEXT,
    domicilio_localidad TEXT,
    telefono_fijo TEXT,
    telefono_celular TEXT,
    email TEXT,
    telefono_referencia TEXT,
    nombre_referencia TEXT,
    parentesco_referencia TEXT,
    fecha_ingr TEXT,
    categ TEXT,
    antig REAL,
    p_permanente INTEGER,
    p_temporaria INTEGER,
    lugar_dependencia TEXT,
    actividad_realiza_dependencia TEXT,
    enfermedad_preexistente TEXT,
    vacuna_covid_dosis INTEGER,
    vacuna_gripe INTEGER,
    vacuna_neumonia INTEGER,
    percibe_asig_fliares_hcd INTEGER,
    servicios_anteriores TEXT,
    antiguedad_servicios REAL,
    trabaja_otra_reparticion INTEGER,
    otra_reparticion_donde TEXT,
    percibe_asig_fliares_otro INTEGER,
    soltero INTEGER,
    casado INTEGER,
    divorciado INTEGER,
    separado INTEGER,
    viudo INTEGER,
    conviviente INTEGER,
    conyuge_apellido_nombre TEXT,
    conyuge_dni TEXT,
    conyuge_fecha_enlace TEXT,
    conyuge_lugar_enlace TEXT,
    conyuge_trabaja TEXT,
    conyuge_razon_social TEXT,
    conyuge_percibe_asignaciones INTEGER,
    conyuge_observaciones TEXT,

    -- Familiares a cargo f1-f7
    f1_apellido TEXT, f1_par TEXT, f1_convive INTEGER, f1_fe_nac TEXT, f1_ed INTEGER, f1_dni TEXT, f1_ni INTEGER, f1_pri INTEGER, f1_sec INTEGER, f1_ter INTEGER,
    f2_apellido TEXT, f2_par TEXT, f2_convive INTEGER, f2_fe_nac TEXT, f2_ed INTEGER, f2_dni TEXT, f2_ni INTEGER, f2_pri INTEGER, f2_sec INTEGER, f2_ter INTEGER,
    f3_apellido TEXT, f3_par TEXT, f3_convive INTEGER, f3_fe_nac TEXT, f3_ed INTEGER, f3_dni TEXT, f3_ni INTEGER, f3_pri INTEGER, f3_sec INTEGER, f3_ter INTEGER,
    f4_apellido TEXT, f4_par TEXT, f4_convive INTEGER, f4_fe_nac TEXT, f4_ed INTEGER, f4_dni TEXT, f4_ni INTEGER, f4_pri INTEGER, f4_sec INTEGER, f4_ter INTEGER,
    f5_apellido TEXT, f5_par TEXT, f5_convive INTEGER, f5_fe_nac TEXT, f5_ed INTEGER, f5_dni TEXT, f5_ni INTEGER, f5_pri INTEGER, f5_sec INTEGER, f5_ter INTEGER,
    f6_apellido TEXT, f6_par TEXT, f6_convive INTEGER, f6_fe_nac TEXT, f6_ed INTEGER, f6_dni TEXT, f6_ni INTEGER, f6_pri INTEGER, f6_sec INTEGER, f6_ter INTEGER,
    f7_apellido TEXT, f7_par TEXT, f7_convive INTEGER, f7_fe_nac TEXT, f7_ed INTEGER, f7_dni TEXT, f7_ni INTEGER, f7_pri INTEGER, f7_sec INTEGER, f7_ter INTEGER,

    -- Padres y hermanos ph1-ph6
    ph1_apellido TEXT, ph1_parentesco TEXT, ph1_convive INTEGER, ph1_fecha_nac TEXT, ph1_dni TEXT, ph1_observacion TEXT,
    ph2_apellido TEXT, ph2_parentesco TEXT, ph2_convive INTEGER, ph2_fecha_nac TEXT, ph2_dni TEXT, ph2_observacion TEXT,
    ph3_apellido TEXT, ph3_parentesco TEXT, ph3_convive INTEGER, ph3_fecha_nac TEXT, ph3_dni TEXT, ph3_observacion TEXT,
    ph4_apellido TEXT, ph4_parentesco TEXT, ph4_convive INTEGER, ph4_fecha_nac TEXT, ph4_dni TEXT, ph4_observacion TEXT,
    ph5_apellido TEXT, ph5_parentesco TEXT, ph5_convive INTEGER, ph5_fecha_nac TEXT, ph5_dni TEXT, ph5_observacion TEXT,
    ph6_apellido TEXT, ph6_parentesco TEXT, ph6_convive INTEGER, ph6_fecha_nac TEXT, ph6_dni TEXT, ph6_observacion TEXT,

    -- Firma, hash y QR
    firma_base64 TEXT,
    qr_validacion TEXT,
    hash_documento TEXT,

    -- Lugar y fecha de declaración
    lugar_declaracion TEXT,
    fecha_declaracion TEXT
)
""")

conn.commit()
conn.close()

print("Base de datos y tabla DDJJ creada correctamente ✅")