# forzar_inicializacion.py
import sqlite3
import os
from werkzeug.security import generate_password_hash
from app import app

print("="*60)
print("🚀 FORZANDO INICIALIZACIÓN DE BASE DE DATOS")
print("="*60)

# Eliminar base de datos antigua si existe
if os.path.exists('legajos_agentes.db'):
    os.remove('legajos_agentes.db')
    print("✅ Base de datos antigua eliminada")

# Ejecutar init_db dentro del contexto de la app
with app.app_context():
    # Importar la función init_db desde app
    from app import init_db
    init_db()
    print("✅ init_db() ejecutado correctamente")

# Verificar que se crearon las tablas
conn = sqlite3.connect('legajos_agentes.db')
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = [t[0] for t in cur.fetchall()]
print(f"\n📋 Tablas creadas: {len(tablas)}")
for t in sorted(tablas):
    print(f"   - {t}")

# Verificar usuarios
cur.execute("SELECT username, rol FROM usuarios")
usuarios = cur.fetchall()
print(f"\n👤 Usuarios creados: {len(usuarios)}")
for u in usuarios:
    print(f"   - {u[0]} ({u[1]})")

conn.close()

print("\n" + "="*60)
print("✅ INICIALIZACIÓN COMPLETADA")
print("="*60)
print("\n🔐 Credenciales:")
print("   admin / Admin2026!")
print("   director / Director2026!")