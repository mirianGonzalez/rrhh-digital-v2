# verificar_tablas.py
import sqlite3

print("="*60)
print("VERIFICANDO ESTRUCTURA DE TABLAS")
print("="*60)

conn = sqlite3.connect('legajos_agentes.db')
cur = conn.cursor()

# Verificar todas las tablas
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
tablas = [t[0] for t in cur.fetchall()]

for tabla in tablas:
    cur.execute(f'PRAGMA table_info({tabla})')
    columnas = [col[1] for col in cur.fetchall()]
    print(f'\n📋 {tabla}: {len(columnas)} columnas')
    # Mostrar todas las columnas
    for col in columnas:
        print(f'   - {col}')

conn.close()
print("\n" + "="*60)