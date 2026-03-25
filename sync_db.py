# sync_db.py
from app import app, db
from models import *

with app.app_context():
    # Esto creará las tablas que no existan
    db.create_all()
    print("✅ Base de datos sincronizada")