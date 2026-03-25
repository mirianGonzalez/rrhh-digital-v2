"""
AUTORIDAD CERTIFICANTE INTERNA - VERSIÓN SIMULADA
Para pruebas de flujo de doble firma
"""

import os
import json
import hashlib
import uuid
from datetime import datetime
import sqlite3

class AutoridadCertificante:
    """Versión simplificada para pruebas de flujo"""
    
    def __init__(self, app):
        self.app = app
        self.cert_dir = os.path.join(app.config.get('BASE_DIR', os.getcwd()), 'CERTIFICADOS')
        os.makedirs(self.cert_dir, exist_ok=True)
    
    def get_db(self):
        """Obtiene conexión a la base de datos usando el path directo"""
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'legajos_agentes.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def emitir_certificado_agente(self, legajo_id, nombre_completo, dni, cargo):
        """Versión simulada - solo registra en BD"""
        
        serial = str(uuid.uuid4()).replace('-', '')[:16].upper()
        pin_inicial = f"PIN{legajo_id[-4:]}" if legajo_id else "1234"
        
        # Guardar metadata en BD
        conn = self.get_db()
        cur = conn.cursor()
        
        # Verificar si ya existe certificado activo
        cur.execute("""
            SELECT * FROM certificados_digitales 
            WHERE legajo_id = ? AND estado = 'ACTIVO'
        """, (legajo_id,))
        
        if cur.fetchone():
            # Actualizar existente
            cur.execute("""
                UPDATE certificados_digitales
                SET serial_number = ?, estado = 'ACTIVO', fecha_emision = ?
                WHERE legajo_id = ? AND estado = 'ACTIVO'
            """, (serial, datetime.now().isoformat(), legajo_id))
        else:
            # Crear nuevo
            cur.execute("""
                INSERT INTO certificados_digitales
                (legajo_id, serial_number, subject_dn, issuer_dn,
                 estado, pin_hash, fecha_emision)
                VALUES (?, ?, ?, ?, 'ACTIVO', ?, ?)
            """, (
                legajo_id, serial,
                f"CN={nombre_completo}, OU=Agente, O=HCD Posadas",
                "CN=AC HCD Posadas, O=HCD Posadas",
                hashlib.sha256(pin_inicial.encode()).hexdigest(),
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
        # Crear archivo simbólico .p12 (archivo de texto con instrucciones)
        p12_path = os.path.join(self.cert_dir, f"cert_{legajo_id}.p12")
        with open(p12_path, 'w') as f:
            f.write(f"""CERTIFICADO SIMULADO - MODO PRUEBA
================================
Legajo: {legajo_id}
Agente: {nombre_completo}
DNI: {dni}
Cargo: {cargo}

PIN DE FIRMA: {pin_inicial}
SERIAL: {serial}

INSTRUCCIONES:
1. Use este PIN para firmar documentos en el sistema
2. En producción, este archivo sería un certificado PKCS#12 real
3. Guarde este PIN de forma segura
""")
        
        return {
            'success': True,
            'serial': serial,
            'p12_path': p12_path,
            'p12_password': pin_inicial,
            'cert_path': p12_path
        }
    
    def validar_pin(self, legajo_id, pin):
        """Valida PIN del agente (versión simulada)"""
        conn = self.get_db()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT pin_hash FROM certificados_digitales
            WHERE legajo_id = ? AND estado = 'ACTIVO'
        """, (legajo_id,))
        
        result = cur.fetchone()
        conn.close()
        
        if result:
            pin_hash_esperado = result['pin_hash']
            pin_hash_ingresado = hashlib.sha256(pin.encode()).hexdigest()
            return pin_hash_ingresado == pin_hash_esperado
        
        # Si no hay certificado, usar PIN por defecto para pruebas
        return pin == "1234" or pin == "4321"