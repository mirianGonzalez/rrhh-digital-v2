# agregar_columnas.py
import sqlite3

print("="*60)
print("🔧 AGREGANDO COLUMNAS FALTANTES A TABLA legajos")
print("="*60)

conn = sqlite3.connect('legajos_agentes.db')
cur = conn.cursor()

# Verificar columnas actuales
cur.execute('PRAGMA table_info(legajos)')
columnas_existentes = [col[1] for col in cur.fetchall()]
print(f"\n📋 Columnas existentes: {len(columnas_existentes)}")
for col in columnas_existentes:
    print(f"   - {col}")

# Columnas que faltan según el código de inicializar_prueba
columnas_faltantes = [
    ('lugar_nacimiento', 'TEXT'),
    ('nacionalidad', 'TEXT'),
    ('estado_civil', 'TEXT'),
    ('domicilio_piso', 'TEXT'),
    ('domicilio_depto', 'TEXT'),
    ('domicilio_barrio', 'TEXT'),
    ('croquis_domicilio', 'TEXT'),
    ('foto_path', 'TEXT'),
    ('tipo_personal', 'TEXT'),
    ('categoria', 'TEXT'),
    ('antiguedad', 'TEXT'),
    ('lugar_desempeno', 'TEXT'),
    ('actividad', 'TEXT'),
    ('planta_permanente', 'INTEGER DEFAULT 0'),
    ('planta_temporaria', 'INTEGER DEFAULT 0'),
    ('enfermedad_preexistente', 'TEXT'),
    ('vacuna_covid_dosis', 'TEXT'),
    ('vacuna_gripe', 'INTEGER DEFAULT 0'),
    ('vacuna_neumonia', 'INTEGER DEFAULT 0'),
    ('seguro_vida', 'INTEGER DEFAULT 0'),
    ('servicios_anteriores', 'TEXT'),
    ('antiguedad_servicios', 'TEXT'),
    ('trabaja_otra_reparticion', 'INTEGER DEFAULT 0'),
    ('otra_reparticion_donde', 'TEXT'),
    ('percibe_asig_fliares_hcd', 'INTEGER DEFAULT 0'),
    ('percibe_asig_fliares_otro', 'INTEGER DEFAULT 0'),
    ('observaciones', 'TEXT'),
    ('hash_legajo', 'TEXT'),
    ('fecha_actualizacion', 'TEXT'),
    ('usuario_actualizacion', 'TEXT'),
    ('telefono_fijo', 'TEXT'),
    ('telefono_referencia', 'TEXT'),
    ('parentesco_referencia', 'TEXT')
]

print(f"\n🔧 Agregando {len(columnas_faltantes)} columnas faltantes...")

for col_name, col_type in columnas_faltantes:
    if col_name not in columnas_existentes:
        try:
            cur.execute(f'ALTER TABLE legajos ADD COLUMN {col_name} {col_type}')
            print(f"   ✅ Agregada: {col_name} ({col_type})")
        except Exception as e:
            print(f"   ❌ Error agregando {col_name}: {e}")
    else:
        print(f"   ℹ️ Ya existe: {col_name}")

conn.commit()

# Verificar columnas finales
cur.execute('PRAGMA table_info(legajos)')
columnas_finales = [col[1] for col in cur.fetchall()]
print(f"\n📋 Columnas finales: {len(columnas_finales)}")
print("   Primeras 20 columnas:")
for col in columnas_finales[:20]:
    print(f"   - {col}")

conn.close()

print("\n" + "="*60)
print("✅ COLUMNAS AGREGADAS CORRECTAMENTE")
print("="*60)
print("\n🚀 Ahora reinicia el servidor y prueba:")
print("   http://192.168.1.117:5000/inicializar_prueba")