import sqlite3
import os
from datetime import datetime

def verificar_y_crear_tabla_ddjj():
    """Verifica si existe la tabla DDJJ y la crea si es necesario"""
    
    # Ruta a tu base de datos (ajústala según tu configuración)
    db_path = 'instance/rrhh.db'  # O la ruta donde esté tu BD
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si existe la tabla
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='ddjj'
        """)
        
        existe = cursor.fetchone()
        
        if not existe:
            print("📝 Creando tabla ddjj...")
            
            # Crear tabla ddjj
            cursor.execute("""
                CREATE TABLE ddjj (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    legajo_id INTEGER NOT NULL,
                    anio INTEGER NOT NULL,
                    fecha_presentacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    archivo_nombre VARCHAR(255),
                    archivo_ruta VARCHAR(500),
                    estado VARCHAR(20) DEFAULT 'PENDIENTE',
                    observaciones TEXT,
                    FOREIGN KEY (legajo_id) REFERENCES legajos(id)
                )
            """)
            
            # Crear índices
            cursor.execute("""
                CREATE INDEX idx_ddjj_legajo ON ddjj(legajo_id)
            """)
            cursor.execute("""
                CREATE INDEX idx_ddjj_anio ON ddjj(anio)
            """)
            
            conn.commit()
            print("✅ Tabla ddjj creada exitosamente")
            
            # Insertar algunos datos de prueba para el año actual
            anio_actual = datetime.now().year
            
            cursor.execute("""
                INSERT INTO ddjj (legajo_id, anio, estado)
                SELECT id, ?, 'PENDIENTE'
                FROM legajos
                WHERE id NOT IN (
                    SELECT legajo_id FROM ddjj WHERE anio = ?
                )
            """, (anio_actual, anio_actual))
            
            conn.commit()
            print(f"✅ Se inicializaron {cursor.rowcount} registros de DDJJ para {anio_actual}")
            
        else:
            print("✅ La tabla ddjj ya existe")
            
            # Verificar estructura
            cursor.execute("PRAGMA table_info(ddjj)")
            columnas = [col[1] for col in cursor.fetchall()]
            
            # Agregar columnas faltantes si es necesario
            if 'estado' not in columnas:
                cursor.execute("ALTER TABLE ddjj ADD COLUMN estado VARCHAR(20) DEFAULT 'PENDIENTE'")
                print("✅ Columna 'estado' agregada")
                
            if 'observaciones' not in columnas:
                cursor.execute("ALTER TABLE ddjj ADD COLUMN observaciones TEXT")
                print("✅ Columna 'observaciones' agregada")
            
            conn.commit()
        
        # Mostrar estadísticas
        cursor.execute("SELECT COUNT(*) FROM ddjj")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ddjj WHERE anio = ?", (datetime.now().year,))
        total_anio = cursor.fetchone()[0]
        
        print(f"\n📊 Estadísticas DDJJ:")
        print(f"   Total registros: {total}")
        print(f"   Registros {datetime.now().year}: {total_anio}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    verificar_y_crear_tabla_ddjj()