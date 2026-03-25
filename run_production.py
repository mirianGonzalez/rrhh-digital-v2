#!/usr/bin/env python
# run_production.py - Iniciar sistema en modo producción con Waitress

import os
import sys
from waitress import serve

# Asegurar que estamos en modo producción
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# Importar la aplicación
from app import app

print("="*60)
print("🚀 INICIANDO SISTEMA RRHH EN MODO PRODUCCIÓN")
print("="*60)
print("📌 Servidor: Waitress")
print("📌 Hilos: 4")
print("📌 Puerto: 5000")
print("📌 Host: 0.0.0.0 (accesible desde la red)")
print("="*60)
print("")
print("🌐 URL de acceso:")
print("   - Local: http://127.0.0.1:5000")
print("   - Red: http://192.168.x.x:5000")
print("")
print("⚠️  Presiona CTRL+C para detener el servidor")
print("="*60)
print("")

try:
    # Iniciar servidor Waitress
    serve(app, 
          host='0.0.0.0', 
          port=5000, 
          threads=4,
          connection_limit=1000,
          channel_timeout=120)
except KeyboardInterrupt:
    print("\n")
    print("="*60)
    print("🛑 Servidor detenido por el usuario")
    print("="*60)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)