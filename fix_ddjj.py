# fix_ddjj.py
import sqlite3
import os

def fix_declaraciones_juradas():
    """Verifica y arregla la tabla declaraciones_juradas"""
    
    db_path = 'legajos_agentes.db'
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='declaraciones_juradas'")
        existe = cursor.fetchone()
        
        if existe:
            print("✅ La tabla declaraciones_juradas ya existe")
            
            # Verificar estructura
            cursor.execute("PRAGMA table_info(declaraciones_juradas)")
            columnas = [col[1] for col in cursor.fetchall()]
            print(f"📋 Columnas: {', '.join(columnas)}")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) FROM declaraciones_juradas")
            total = cursor.fetchone()[0]
            print(f"📊 Total registros: {total}")
            
            # Contar por año
            cursor.execute("SELECT anio, COUNT(*) FROM declaraciones_juradas GROUP BY anio")
            for row in cursor.fetchall():
                print(f"   Año {row[0]}: {row[1]} registros")
            
            # Contar por estado
            cursor.execute("SELECT estado, COUNT(*) FROM declaraciones_juradas GROUP BY estado")
            for row in cursor.fetchall():
                print(f"   Estado {row[0]}: {row[1]} registros")
                
        else:
            print("⚠️ La tabla declaraciones_juradas NO existe")
            print("📝 Creando tabla...")
            
            # Crear la tabla con la estructura correcta
            cursor.execute("""
                CREATE TABLE declaraciones_juradas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    legajo_id TEXT NOT NULL,
                    anio INTEGER NOT NULL,
                    version INTEGER DEFAULT 1,
                    estado TEXT DEFAULT 'BORRADOR',
                    datos_json TEXT,
                    hash_datos TEXT,
                    archivo_docx TEXT,
                    archivo_pdf TEXT,
                    hash_pdf TEXT,
                    codigo_validacion TEXT,
                    qr_path TEXT,
                    fecha_generacion TEXT,
                    fecha_envio TEXT,
                    usuario_genero TEXT,
                    usuario_finalizo TEXT,
                    ip_generacion TEXT,
                    user_agent TEXT,
                    alerta_enviada INTEGER DEFAULT 0,
                    fecha_alerta TEXT,
                    observaciones TEXT,
                    activa INTEGER DEFAULT 1,
                    es_historica INTEGER DEFAULT 0
                )
            """)
            
            # Crear índices
            cursor.execute("CREATE INDEX idx_ddjj_legajo ON declaraciones_juradas(legajo_id)")
            cursor.execute("CREATE INDEX idx_ddjj_anio ON declaraciones_juradas(anio)")
            cursor.execute("CREATE INDEX idx_ddjj_estado ON declaraciones_juradas(estado)")
            
            conn.commit()
            print("✅ Tabla creada exitosamente")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Verificando tabla declaraciones_juradas")
    print("=" * 50)
    fix_declaraciones_juradas()