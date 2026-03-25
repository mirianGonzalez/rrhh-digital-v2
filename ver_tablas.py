import sqlite3

ruta_legajos = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\legajos.db"
ruta_ddjj = r"G:\Mi unidad\RRHH_DIGITAL\BASE_DATOS\ddjj.db"

# Ver todas las tablas
for ruta in [ruta_legajos, ruta_ddjj]:
    conn = sqlite3.connect(ruta)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(f"\nTablas en {ruta}:")
    print(cur.fetchall())
    

# Ver columnas de tablas específicas en legajos.db
conn = sqlite3.connect(ruta_legajos)
cur = conn.cursor()
for tabla in ["agentes", "ddjj_agentes", "documentos_faltantes"]:
    cur.execute(f"PRAGMA table_info({tabla});")
    print(f"\nColumnas en {tabla}:")
    print(cur.fetchall())
