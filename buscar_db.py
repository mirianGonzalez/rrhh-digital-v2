# buscar_db.py
import os
import sqlite3

def buscar_base_datos():
    """Busca archivos .db en tu proyecto"""
    
    # Rutas comunes donde podría estar la BD
    rutas_posibles = [
        'instance/rrhh.db',
        'rrhh.db',
        'database.db',
        'app.db',
        'data.db',
        'instance/app.db',
        'instance/database.db',
        '../rrhh.db',
        './rrhh.db'
    ]
    
    print("🔍 Buscando base de datos...\n")
    
    encontradas = []
    
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            tamaño = os.path.getsize(ruta)
            encontradas.append((ruta, tamaño))
            print(f"✅ Encontrada: {ruta} ({tamaño} bytes)")
    
    if not encontradas:
        print("❌ No se encontró ninguna base de datos en las rutas comunes")
        print("\nBuscando recursivamente...")
        
        # Búsqueda recursiva
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.db'):
                    ruta_completa = os.path.join(root, file)
                    tamaño = os.path.getsize(ruta_completa)
                    encontradas.append((ruta_completa, tamaño))
                    print(f"✅ Encontrada: {ruta_completa} ({tamaño} bytes)")
    
    if encontradas:
        print(f"\n📊 Total de bases de datos encontradas: {len(encontradas)}")
        return encontradas[0][0]  # Retorna la primera encontrada
    
    return None

if __name__ == "__main__":
    ruta_db = buscar_base_datos()
    
    if ruta_db:
        print(f"\n💡 Usa esta ruta en el script: {ruta_db}")
        
        # Intentar conectar para verificar
        try:
            conn = sqlite3.connect(ruta_db)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = cursor.fetchall()
            print(f"\n📋 Tablas existentes: {[t[0] for t in tablas]}")
            conn.close()
        except Exception as e:
            print(f"Error al conectar: {e}")