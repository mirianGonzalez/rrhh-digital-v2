# agregar_columnas_declaraciones.py
import sqlite3

print("="*60)
print("🔧 AGREGANDO COLUMNAS FALTANTES A TABLA declaraciones_juradas")
print("="*60)

conn = sqlite3.connect('legajos_agentes.db')
cur = conn.cursor()

# Verificar columnas actuales
cur.execute('PRAGMA table_info(declaraciones_juradas)')
columnas_existentes = [col[1] for col in cur.fetchall()]
print(f"\n📋 Columnas existentes en declaraciones_juradas: {len(columnas_existentes)}")
for col in columnas_existentes:
    print(f"   - {col}")

# Columnas que deberían existir según app.py
columnas_necesarias = [
    ('version', 'INTEGER DEFAULT 1'),
    ('datos_json', 'TEXT'),
    ('hash_datos', 'TEXT'),
    ('archivo_docx', 'TEXT'),
    ('qr_path', 'TEXT'),
    ('ip_generacion', 'TEXT'),
    ('user_agent', 'TEXT'),
    ('alerta_enviada', 'INTEGER DEFAULT 0'),
    ('fecha_alerta', 'TEXT'),
    ('es_historica', 'INTEGER DEFAULT 0')
]

print(f"\n🔧 Agregando columnas faltantes...")

for col_name, col_type in columnas_necesarias:
    if col_name not in columnas_existentes:
        try:
            cur.execute(f'ALTER TABLE declaraciones_juradas ADD COLUMN {col_name} {col_type}')
            print(f"   ✅ Agregada: {col_name} ({col_type})")
        except Exception as e:
            print(f"   ❌ Error agregando {col_name}: {e}")
    else:
        print(f"   ℹ️ Ya existe: {col_name}")

conn.commit()

# Verificar columnas finales
cur.execute('PRAGMA table_info(declaraciones_juradas)')
columnas_finales = [col[1] for col in cur.fetchall()]
print(f"\n📋 Columnas finales: {len(columnas_finales)}")
for col in columnas_finales:
    print(f"   - {col}")

conn.close()

print("\n" + "="*60)
print("✅ ACTUALIZACIÓN COMPLETADA")
print("="*60)
print("\n🚀 Reinicia el servidor y prueba nuevamente:")
print("   python run_server.py")