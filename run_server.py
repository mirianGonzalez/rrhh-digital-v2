# run_server.py - Versión definitiva
import os
import sys
from waitress import serve

# Configurar entorno
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_DEBUG'] = '0'

# Importar la aplicación
from app import app

print("="*60)
print("🚀 SISTEMA LEGAJOS Y ARCHIVO DIGITAL - CREADO POR MIRIAN YOLANDA GONZALEZ")
print("="*60)

# Modificar la app para aceptar conexiones externas
@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

print("📌 Servidor: Waitress")
print("📌 Hilos: 8")
print("📌 Puerto: 5000")
print("="*60)
print("")
print("🌐 URL DE ACCESO:")
print("   📍 Local (misma PC): http://127.0.0.1:5000")
print("   📍 Red WiFi: http://192.168.1.117:5000")
print("   📍 Desde celular: http://192.168.1.117:5000")
print("")
print("⚠️  Presiona CTRL+C para detener")
print("="*60)
print("")

# Iniciar servidor con configuración para red local
try:
    serve(app, 
          host='0.0.0.0',          # Escucha en todas las interfaces
          port=5000,               # Puerto
          threads=8,               # Hilos
          connection_limit=1000,
          channel_timeout=120,
          url_scheme='http',
          ident='RRHH Digital Server',
          expose_tracebacks=False,
          asyncore_use_poll=True,
          backlog=1024)
          
except KeyboardInterrupt:
    print("\n")
    print("="*60)
    print("🛑 Servidor detenido")
    print("="*60)
except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)