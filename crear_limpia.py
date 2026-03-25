import re

def crear_app_limpia():
    with open('app.py', 'r', encoding='utf-8') as f:
        contenido = f.read()
    
    # Separar el contenido en secciones
    lineas = contenido.split('\n')
    
    # Mantener la configuración inicial (todo hasta el primer @app.route)
    config = []
    rutas = []
    en_config = True
    
    # Lista de rutas que queremos mantener (las más importantes)
    rutas_a_mantener = [
        '/', '/logout', '/panel', '/legajos', '/legajo/', 
        '/legajo/nuevo', '/legajo/crear', '/legajo/<legajo_id>/editar',
        '/legajo/<legajo_id>/subir_documento', '/documento/<int:doc_id>/ver',
        '/documento/<int:doc_id>/descargar', '/documento/<int:doc_id>/anular',
        '/legajo/<legajo_id>/ddjj/nueva', '/ddjj/<int:ddjj_id>/editar',
        '/ddjj/<int:ddjj_id>/finalizar', '/ddjj/<int:ddjj_id>',
        '/legajo/<legajo_id>/ddjj/historial', '/auditoria', '/manual',
        '/validar/<codigo>', '/admin/backup', '/cambiar_password', '/test_email',
        '/admin/usuarios', '/admin/usuario/nuevo', '/admin/usuario/<int:user_id>/editar',
        '/admin/usuario/<int:user_id>/reset_password', '/admin/usuario/<int:user_id>/eliminar',
        '/legajo/<legajo_id>/certificado/generar', '/ddjj/<int:ddjj_id>/firmar',
        '/ddjj/<int:ddjj_id>/cofirmar', '/ddjj/<int:ddjj_id>/verificar_firma',
        '/listar_ddjj', '/ddjj/descargar/<int:ddjj_id>'
    ]
    
    # Reconstruir el archivo línea por línea
    nuevas_lineas = []
    saltar_hasta = -1
    
    for i, linea in enumerate(lineas):
        if i < saltar_hasta:
            continue
            
        # Mantener configuración inicial
        if '@app.route' not in linea and not linea.strip().startswith('def ') and en_config:
            nuevas_lineas.append(linea)
            continue
        else:
            en_config = False
            
        # Si encontramos una ruta
        if '@app.route' in linea:
            # Verificar si es una ruta que queremos mantener
            mantener = False
            for ruta in rutas_a_mantener:
                if ruta in linea:
                    mantener = True
                    break
            
            if mantener:
                # Buscar el bloque completo de la función
                j = i
                bloque = []
                while j < len(lineas):
                    bloque.append(lineas[j])
                    if j > i and (lineas[j].strip().startswith('@app.route') or 
                                  (lineas[j].strip().startswith('def ') and not lineas[j].startswith('    '))):
                        if len(bloque) > 1:
                            bloque.pop()
                        break
                    j += 1
                
                nuevas_lineas.extend(bloque)
                nuevas_lineas.append('')
                saltar_hasta = j
            else:
                # Saltar esta ruta
                j = i
                while j < len(lineas):
                    if j > i and (lineas[j].strip().startswith('@app.route') or 
                                  (lineas[j].strip().startswith('def ') and not lineas[j].startswith('    '))):
                        break
                    j += 1
                saltar_hasta = j
    
    # Guardar archivo limpio
    with open('app_final_limpia.py', 'w', encoding='utf-8') as f:
        f.write('\n'.join(nuevas_lineas))
    
    print("✅ Archivo creado: app_final_limpia.py")
    print(f"📊 Líneas totales: {len(nuevas_lineas)}")
    print("\n📌 Ahora ejecuta:")
    print("   mv app_final_limpia.py app.py")
    print("   python app.py")

if __name__ == "__main__":
    crear_app_limpia()