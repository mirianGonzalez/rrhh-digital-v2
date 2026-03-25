import sqlite3
import hashlib

from config import DB_PATH


# ============================
# CONEXION BASE DE DATOS
# ============================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ============================
# INICIALIZAR BASE
# ============================

def init_db():

    db = get_db()

    # activar claves foraneas
    db.execute("PRAGMA foreign_keys = ON")

    # =============================
    # USUARIOS
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE,
        password TEXT,
        rol TEXT
    )
    """)

    # =============================
    # AGENTES
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS agentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        legajo INTEGER UNIQUE,
        nombre TEXT NOT NULL,
        dni TEXT,
        cuil TEXT,
        fecha_nacimiento DATE,
        sexo TEXT,
        cargo TEXT,
        dependencia TEXT,
        fecha_ingreso DATE,
        servicios_anteriores INTEGER DEFAULT 0,
        huella_registrada INTEGER DEFAULT 0,
        activo INTEGER DEFAULT 1
    )
    """)

    # =============================
    # DOCUMENTOS
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        legajo INTEGER,
        tipo TEXT,
        archivo TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        estado TEXT
    )
    """)

    # =============================
    # HISTORIAL DOCUMENTOS
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS historial_documentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        legajo INTEGER,
        tipo_documento TEXT,
        archivo TEXT,
        version INTEGER DEFAULT 1,
        reemplaza_documento INTEGER,
        usuario TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =============================
    # DOCUMENTOS REQUERIDOS
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS documentos_requeridos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_documento TEXT UNIQUE,
        obligatorio INTEGER DEFAULT 1
    )
    """)

    # =============================
    # DDJJ
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS ddjj (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        legajo INTEGER,
        anio INTEGER,
        archivo TEXT,
        hash TEXT,
        estado TEXT
    )
    """)

    # =============================
    # AUDITORIA
    # =============================

    db.execute("""
    CREATE TABLE IF NOT EXISTS auditoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        accion TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =============================
    # INDICES (busqueda rapida)
    # =============================

    db.execute("CREATE INDEX IF NOT EXISTS idx_legajo ON agentes(legajo)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_dni ON agentes(dni)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_nombre ON agentes(nombre)")

    # =============================
    # CREAR ADMIN SI NO EXISTE
    # =============================

    admin = db.execute(
        "SELECT * FROM usuarios WHERE usuario='admin'"
    ).fetchone()

    if not admin:

        password = hashlib.sha256("admin".encode()).hexdigest()

        db.execute(
            "INSERT INTO usuarios (usuario,password,rol) VALUES (?,?,?)",
            ("admin", password, "admin")
        )

        print("Usuario admin creado automáticamente")

    db.commit()
    db.close()



def crear_tablas():

    db = get_db()

    db.execute("""
    CREATE TABLE IF NOT EXISTS documentos_requeridos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT UNIQUE,
        nombre TEXT,
        obligatorio INTEGER
    )
    """)

    db.commit()
    db.close()