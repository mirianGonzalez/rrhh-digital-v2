# verificar_tablas_ddjj.py
import sqlite3

def verificar_tablas():
    """Verifica las tablas relacionadas con DDJJ"""
    
    db_path = 'legajos_agentes.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        
        print("📋 Tablas relacionadas con DDJJ:")
        tablas_ddjj = [t for t in tablas if 'ddjj' in t.lower() or 'declaracion' in t.lower()]
        
        for tabla in tablas_ddjj:
            print(f"\n📊 Tabla: {tabla}")
            cursor.execute(f"PRAGMA table_info({tabla})")
            columnas = cursor.fetchall()
            print("   Columnas:")
            for col in columnas:
                print(f"      - {col[1]} ({col[2]})")
            
            # Mostrar algunos datos de ejemplo
            cursor.execute(f"SELECT * FROM {tabla} LIMIT 3")
            datos = cursor.fetchall()
            if datos:
                print(f"   Datos de ejemplo: {len(datos)} registros")
                for dato in datos:
                    print(f"      {dato}")
        
        # Verificar también la tabla 'auditoria' para ver actividades
        if 'auditoria' in tablas:
            print(f"\n📊 Tabla: auditoria")
            cursor.execute("SELECT * FROM auditoria ORDER BY fecha DESC LIMIT 5")
            auditoria = cursor.fetchall()
            cursor.execute("PRAGMA table_info(auditoria)")
            cols = [col[1] for col in cursor.fetchall()]
            print(f"   Últimas actividades:")
            for act in auditoria:
                print(f"      {dict(zip(cols, act))}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verificar_tablas()