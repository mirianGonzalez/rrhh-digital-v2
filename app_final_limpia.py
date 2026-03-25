"""
SISTEMA DE GESTIÓN DE LEGAJOS - ARCHIVO Y DECLARACIONES JURADAS
VERSIÓN REALIZADA POR MIRIAN YOLANDA GONZALEZ
CON MÓDULO DE FIRMA DIGITAL PKI
"""

# ==========================
# PRIMERO: TODOS LOS IMPORTS
# ==========================
import io
import os
import sys
import sqlite3
import uuid
import json
import hashlib
import shutil
import subprocess
import tempfile
import logging
import smtplib
import schedule
import threading
import time
import traceback
import random
import base64
from functools import wraps
from datetime import datetime, timedelta
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from flask import Flask, flash, make_response, render_template, request, redirect, send_file, session, send_from_directory, url_for, g, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# ==========================
# LIBRERÍAS PDF Y FIRMA DIGITAL
# ==========================
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal, letter
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DictionaryObject, NameObject, BooleanObject, TextStringObject, create_string_object
from pypdf.annotations import Text

# Librerías para firma digital PKI
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import pkcs12

# ==========================
# LIBRERÍAS DOCX
# ==========================
from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from docx.shared import Mm
from docx import Document
from PIL import Image, ImageDraw, ImageFont

# ==========================
# QR
# ==========================
import qrcode

# ==========================
# CONFIGURACIÓN DE LOGGING
# ==========================
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('LOGS/sistema.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ==========================
# IMPORTAR VARIABLES DE ENTORNO
# ==========================

# Cargar variables del archivo .env
load_dotenv()

# ==========================
# CONFIGURACIÓN FLASK
# ==========================
app = Flask(__name__,
            static_folder='static',
            static_url_path='/static')

# Usar variable de entorno para SECRET_KEY
app.secret_key = os.getenv('SECRET_KEY', 'MI_CLAVE_SECRETA_SUPER_SEGURA_2026_MIRIAN')

# Configuración de sesión
app.config['SESSION_COOKIE_NAME'] = 'rrhh_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=8)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# ==========================
# RUTAS Y BASES DE DATOS
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "legajos_agentes.db")

# Configurar carpeta de documentos (usar ruta local por defecto)
DOCUMENTOS_AGENTES_PATH = os.path.join(BASE_DIR, "DOCUMENTOS_AGENTES")
app.config['UPLOAD_FOLDER'] = DOCUMENTOS_AGENTES_PATH
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Configuración adicional
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'tu-secret-key-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///legajos_agentes.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ==========================
# CONFIGURACIÓN DE FIRMA DIGITAL
# ==========================
CERTIFICADOS_PATH = os.path.join(BASE_DIR, "CERTIFICADOS")
os.makedirs(CERTIFICADOS_PATH, exist_ok=True)

# ==========================
# CONTEXTO GLOBAL PARA TEMPLATES
# ==========================
@app.context_processor
@app.route("/legajo/<legajo_id>/certificado/generar", methods=["GET", "POST"])
@login_requerido

@app.route("/ddjj/<int:ddjj_id>/firmar", methods=["GET", "POST"])
@login_requerido

@app.route("/ddjj/<int:ddjj_id>/cofirmar", methods=["GET", "POST"])
@login_requerido
@rol_permitido(["ADMIN", "DIRECTOR"])

@app.route("/ddjj/<int:ddjj_id>/verificar_firma")
@login_requerido

@app.route("/", methods=["GET", "POST"])

@app.route("/logout")
@login_requerido

@app.route("/panel")
@login_requerido

@app.route("/legajos")
@login_requerido

@app.route("/legajo/nuevo", methods=["GET", "POST"])
@login_requerido
@rol_permitido(["ADMIN", "RRHH"])

@app.route("/ddjj/<int:ddjj_id>/nueva", methods=["GET"])
@login_requerido

@app.route("/ddjj/<int:ddjj_id>/ver")
@login_requerido

@app.route("/ddjj/descargar/<int:ddjj_id>")
@login_requerido

@app.route("/validar/<codigo>")

@app.route("/legajo/crear", methods=["POST"])
@login_requerido
@rol_permitido(["ADMIN", "RRHH"])

@app.route("/legajo/<legajo_id>")
@login_requerido

@app.route("/legajo/<legajo_id>/subir_documento", methods=["POST"])
@login_requerido
@rol_permitido(["ADMIN", "RRHH"])

@app.route("/documento/<int:doc_id>/ver")
@login_requerido

@app.route("/documento/<int:doc_id>/descargar")
@login_requerido

@app.route("/documento/<int:doc_id>/anular", methods=["POST"])
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/legajo/<legajo_id>/ddjj/nueva", methods=["GET", "POST"])
@login_requerido

@app.route("/ddjj/<int:ddjj_id>/editar", methods=["GET", "POST"])
@login_requerido

@app.route("/ddjj/<int:ddjj_id>")
@login_requerido

@app.route("/ddjj/<int:ddjj_id>/finalizar", methods=["POST"])
@login_requerido

@app.route("/legajo/<legajo_id>/ddjj/historial")
@login_requerido

@app.route("/auditoria")
@login_requerido
@rol_permitido(["ADMIN", "AUDITOR"])

@app.route("/manual")
@login_requerido

@app.route("/manual_tester")
@login_requerido

@app.route("/admin/backup")
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/reset_password")

@app.route("/cambiar_password", methods=["GET", "POST"])
@login_requerido

@app.route("/test_email")
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/admin/usuarios")
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/admin/usuario/nuevo", methods=["GET", "POST"])
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/admin/usuario/<int:user_id>/editar", methods=["GET", "POST"])
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/admin/usuario/<int:user_id>/reset_password", methods=["POST"])
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/admin/usuario/<int:user_id>/eliminar", methods=["POST"])
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/inicializar_prueba")
@login_requerido
@rol_permitido(["ADMIN"])

@app.route("/crear_ddjj_completa_final/<legajo_id>")

@app.route("/generar_pdf_ddjj_auto/<int:ddjj_id>")
@login_requerido

@app.route("/resetear_testers")

@app.route("/resetear_tester1")

@app.route("/desbloquear_testers")

@app.route("/cambiar_rol_tester")

@app.route("/legajo/<legajo_id>/editar", methods=["GET", "POST"])
@login_requerido

@app.route("/actualizar_tester1")

@app.route("/actualizar_tester1_final")

@app.route('/listar_ddjj')
@login_requerido

@app.route('/ddjj/ver/<int:ddjj_id>')
@login_requerido

@app.route('/ddjj/descargar/<int:id>')
@login_requerido

@app.route('/api/notificaciones')
@login_requerido
