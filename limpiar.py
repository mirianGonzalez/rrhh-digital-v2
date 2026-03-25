import re

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Diccionario para rastrear funciones ya definidas
funciones_vistas = {}
lineas_limpias = []
eliminadas = 0

for i, line in enumerate(lines, 1):
    # Buscar definiciones de rutas
    match_route = re.search(r'@app\.route\(["\'](.*?)["\']', line)
    match_func = re.search(r'def\s+(\w+)\s*\(', line)
    
    if match_route and match_func:
        endpoint = match_func.group(1)
        if endpoint in funciones_vistas:
            print(f"⚠️ Eliminando duplicado: {endpoint} en línea {i}")
            eliminadas += 1
            continue
        else:
            funciones_vistas[endpoint] = i
            lineas_limpias.append(line)
    else:
        lineas_limpias.append(line)

# Guardar archivo limpio
with open('app_clean.py', 'w', encoding='utf-8') as f:
    f.writelines(lineas_limpias)

print(f"✅ Limpieza completada. Se eliminaron {eliminadas} funciones duplicadas.")
print("📁 Archivo guardado como app_clean.py")