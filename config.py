import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ===============================
# BASE DE DATOS
# ===============================

DB_PATH = os.path.join(BASE_DIR, "BASE_DATOS", "legajos.db")

# ===============================
# DOCUMENTOS AGENTES
# ===============================

DOCUMENTOS_PATH = os.path.join(BASE_DIR, "DOCUMENTOS_AGENTES")

# ===============================
# PLANTILLAS
# ===============================

PLANTILLAS_PATH = os.path.join(BASE_DIR, "PLANTILLAS")

# ===============================
# SEGURIDAD
# ===============================

SECRET_KEY = "rrhh_digital_secret_2025"