# agregar_columnas_ddjj_datos.py
import sqlite3

print("="*60)
print("🔧 AGREGANDO COLUMNAS FALTANTES A TABLA ddjj_datos")
print("="*60)

conn = sqlite3.connect('legajos_agentes.db')
cur = conn.cursor()

# Verificar columnas actuales
cur.execute('PRAGMA table_info(ddjj_datos)')
columnas_existentes = [col[1] for col in cur.fetchall()]
print(f"\n📋 Columnas existentes en ddjj_datos: {len(columnas_existentes)}")
for col in columnas_existentes:
    print(f"   - {col}")

# Columnas que deberían existir según la función crear_ddjj_completa_final
columnas_necesarias = [
    ('fecha_nacimiento', 'TEXT'),
    ('lugar_nacimiento', 'TEXT'),
    ('estado_civil', 'TEXT'),
    ('estudios_completos', 'TEXT'),
    ('estudios_incompletos', 'TEXT'),
    ('estudios_nivel', 'TEXT'),
    ('titulo', 'TEXT'),
    ('anios_cursados', 'TEXT'),
    ('domicilio_barrio', 'TEXT'),
    ('domicilio_chacra', 'TEXT'),
    ('domicilio_piso', 'TEXT'),
    ('domicilio_depto', 'TEXT'),
    ('telefono_fijo', 'TEXT'),
    ('telefono_referencia', 'TEXT'),
    ('nombre_referencia', 'TEXT'),
    ('parentesco_referencia', 'TEXT'),
    ('categoria', 'TEXT'),
    ('antiguedad', 'TEXT'),
    ('planta_permanente', 'INTEGER DEFAULT 0'),
    ('planta_temporaria', 'INTEGER DEFAULT 0'),
    ('lugar_desempeno', 'TEXT'),
    ('actividad', 'TEXT'),
    ('enfermedad_preexistente', 'TEXT'),
    ('vacuna_covid_dosis', 'TEXT'),
    ('vacuna_gripe', 'TEXT'),
    ('vacuna_neumonia', 'TEXT'),
    ('percibe_asig_fliares_hcd', 'INTEGER DEFAULT 0'),
    ('servicios_anteriores', 'TEXT'),
    ('antiguedad_servicios', 'TEXT'),
    ('trabaja_otra_reparticion', 'INTEGER DEFAULT 0'),
    ('otra_reparticion_donde', 'TEXT'),
    ('percibe_asig_fliares_otro', 'INTEGER DEFAULT 0'),
    ('lugar', 'TEXT'),
    ('fecha_declaracion', 'TEXT'),
    ('firma_agente', 'TEXT'),
    ('fecha_ingreso', 'TEXT'),
    ('email', 'TEXT')
]

print(f"\n🔧 Agregando {len(columnas_necesarias)} columnas faltantes...")

for col_name, col_type in columnas_necesarias:
    if col_name not in columnas_existentes:
        try:
            cur.execute(f'ALTER TABLE ddjj_datos ADD COLUMN {col_name} {col_type}')
            print(f"   ✅ Agregada: {col_name} ({col_type})")
        except Exception as e:
            print(f"   ❌ Error agregando {col_name}: {e}")
    else:
        print(f"   ℹ️ Ya existe: {col_name}")

conn.commit()

# Verificar columnas finales
cur.execute('PRAGMA table_info(ddjj_datos)')
columnas_finales = [col[1] for col in cur.fetchall()]
print(f"\n📋 Columnas finales en ddjj_datos: {len(columnas_finales)}")
print("   (Mostrando primeras 15)")
for col in columnas_finales[:15]:
    print(f"   - {col}")
if len(columnas_finales) > 15:
    print(f"   ... y {len(columnas_finales)-15} más")

conn.close()

print("\n" + "="*60)
print("✅ ACTUALIZACIÓN COMPLETADA")
print("="*60)
print("\n🚀 Reinicia el servidor:")
print("   python run_server.py")