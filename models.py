# models.py - Archivo completo con todos los modelos
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Crear la instancia de db que será importada
db = SQLAlchemy()

class Usuario(db.Model):
    """Modelo de usuarios del sistema"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(20), default='USER')  # ADMIN, USER, TESTER
    activo = db.Column(db.Integer, default=1)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.usuario}>'


class Legajo(db.Model):
    """Modelo de legajos de agentes"""
    __tablename__ = 'legajos'
    
    id = db.Column(db.Integer, primary_key=True)
    legajo_id = db.Column(db.String(20), unique=True, nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20))
    cuil = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.String(20))
    domicilio = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.String(20))
    cargo = db.Column(db.String(100))
    area = db.Column(db.String(100))
    estado = db.Column(db.String(20), default='ACTIVO')  # ACTIVO, INACTIVO, SUSPENDIDO
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Legajo {self.legajo_id} - {self.apellido}, {self.nombre}>'


class Documento(db.Model):
    """Modelo de documentos de legajos"""
    __tablename__ = 'documentos'
    
    id = db.Column(db.Integer, primary_key=True)
    legajo_id = db.Column(db.String(20), db.ForeignKey('legajos.legajo_id'), nullable=False)
    tipo_documento = db.Column(db.String(50), nullable=False)  # DNI, TITULO, CERTIFICADO, etc.
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    fecha_carga = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_carga = db.Column(db.String(50))
    observaciones = db.Column(db.Text)
    hash_archivo = db.Column(db.String(256))
    
    # Relación
    legajo = db.relationship('Legajo', backref='documentos')
    
    def __repr__(self):
        return f'<Documento {self.tipo_documento} - {self.nombre_archivo}>'


class DeclaracionJurada(db.Model):
    """Modelo para declaraciones juradas"""
    __tablename__ = 'declaraciones_juradas'
    
    id = db.Column(db.Integer, primary_key=True)
    legajo_id = db.Column(db.String(20), db.ForeignKey('legajos.legajo_id'), nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    version = db.Column(db.Integer, default=1)
    estado = db.Column(db.String(20), default='BORRADOR')  # BORRADOR, FINALIZADA, OBSERVADA
    datos_json = db.Column(db.Text)
    hash_datos = db.Column(db.String(256))
    archivo_docx = db.Column(db.String(500))
    archivo_pdf = db.Column(db.String(500))
    hash_pdf = db.Column(db.String(256))
    codigo_validacion = db.Column(db.String(50))
    qr_path = db.Column(db.String(500))
    fecha_generacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_envio = db.Column(db.DateTime)
    usuario_genero = db.Column(db.String(50))
    usuario_finalizo = db.Column(db.String(50))
    ip_generacion = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    alerta_enviada = db.Column(db.Integer, default=0)
    fecha_alerta = db.Column(db.DateTime)
    observaciones = db.Column(db.Text)
    activa = db.Column(db.Integer, default=1)
    es_historica = db.Column(db.Integer, default=0)
    
    # Relación con legajo
    legajo = db.relationship('Legajo', backref='declaraciones_juradas')
    
    def __repr__(self):
        return f'<DeclaracionJurada {self.legajo_id} - {self.anio} v{self.version}>'


class DDJJDatos(db.Model):
    """Datos personales de la declaración jurada"""
    __tablename__ = 'ddjj_datos'
    
    id = db.Column(db.Integer, primary_key=True)
    ddjj_id = db.Column(db.Integer, db.ForeignKey('declaraciones_juradas.id'), nullable=False)
    fecha_nacimiento = db.Column(db.String(20))
    lugar_nacimiento = db.Column(db.String(100))
    dni = db.Column(db.String(20))
    estado_civil = db.Column(db.String(20))
    estudios_completos = db.Column(db.String(10))
    estudios_incompletos = db.Column(db.Text)
    estudios_nivel = db.Column(db.String(50))
    titulo = db.Column(db.String(100))
    anios_cursados = db.Column(db.String(10))
    domicilio_barrio = db.Column(db.String(100))
    domicilio_chacra = db.Column(db.String(100))
    domicilio_calle = db.Column(db.String(100))
    domicilio_numero = db.Column(db.String(20))
    domicilio_piso = db.Column(db.String(10))
    domicilio_depto = db.Column(db.String(10))
    domicilio_localidad = db.Column(db.String(100))
    telefono_fijo = db.Column(db.String(20))
    telefono_celular = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    telefono_referencia = db.Column(db.String(20))
    nombre_referencia = db.Column(db.String(100))
    parentesco_referencia = db.Column(db.String(50))
    fecha_ingreso = db.Column(db.String(20))
    categoria = db.Column(db.String(20))
    antiguedad = db.Column(db.String(20))
    planta_permanente = db.Column(db.Integer, default=0)
    planta_temporaria = db.Column(db.Integer, default=0)
    lugar_desempeno = db.Column(db.String(100))
    actividad = db.Column(db.String(100))
    enfermedad_preexistente = db.Column(db.Text)
    vacuna_covid_dosis = db.Column(db.String(20))
    vacuna_gripe = db.Column(db.String(10))
    vacuna_neumonia = db.Column(db.String(10))
    percibe_asig_fliares_hcd = db.Column(db.Integer, default=0)
    servicios_anteriores = db.Column(db.Text)
    antiguedad_servicios = db.Column(db.String(50))
    trabaja_otra_reparticion = db.Column(db.Integer, default=0)
    otra_reparticion_donde = db.Column(db.String(200))
    percibe_asig_fliares_otro = db.Column(db.Integer, default=0)
    lugar = db.Column(db.String(100))
    fecha_declaracion = db.Column(db.String(20))
    firma_agente = db.Column(db.Text)
    
    # Relación
    declaracion = db.relationship('DeclaracionJurada', backref='datos_personales')
    
    def __repr__(self):
        return f'<DDJJDatos DDJJ:{self.ddjj_id}>'


class DDJJFamiliaresCargo(db.Model):
    """Familiares a cargo en la declaración jurada"""
    __tablename__ = 'ddjj_familiares_cargo'
    
    id = db.Column(db.Integer, primary_key=True)
    ddjj_id = db.Column(db.Integer, db.ForeignKey('declaraciones_juradas.id'), nullable=False)
    orden = db.Column(db.Integer)
    apellido_nombre = db.Column(db.String(200))
    parentesco = db.Column(db.String(50))
    convive = db.Column(db.Integer, default=0)
    fecha_nacimiento = db.Column(db.String(20))
    edad = db.Column(db.Integer)
    dni = db.Column(db.String(20))
    ni = db.Column(db.String(10))  # Nivel Inicial
    pri = db.Column(db.String(10))  # Primaria
    sec = db.Column(db.String(10))  # Secundaria
    ter_univ = db.Column(db.String(10))  # Terciario/Universitario
    
    # Relación
    declaracion = db.relationship('DeclaracionJurada', backref='familiares_cargo')


class DDJJPadresHermanos(db.Model):
    """Padres y hermanos en la declaración jurada"""
    __tablename__ = 'ddjj_padres_hermanos'
    
    id = db.Column(db.Integer, primary_key=True)
    ddjj_id = db.Column(db.Integer, db.ForeignKey('declaraciones_juradas.id'), nullable=False)
    orden = db.Column(db.Integer)
    apellido_nombre = db.Column(db.String(200))
    parentesco = db.Column(db.String(50))
    convive = db.Column(db.Integer, default=0)
    fecha_nacimiento = db.Column(db.String(20))
    dni = db.Column(db.String(20))
    observacion = db.Column(db.Text)
    
    # Relación
    declaracion = db.relationship('DeclaracionJurada', backref='padres_hermanos')


class DDJJConyuge(db.Model):
    """Cónyuge en la declaración jurada"""
    __tablename__ = 'ddjj_conyuge'
    
    id = db.Column(db.Integer, primary_key=True)
    ddjj_id = db.Column(db.Integer, db.ForeignKey('declaraciones_juradas.id'), nullable=False)
    apellido_nombre = db.Column(db.String(200))
    dni = db.Column(db.String(20))
    fecha_enlace = db.Column(db.String(20))
    lugar_enlace = db.Column(db.String(100))
    trabaja = db.Column(db.Integer, default=0)
    razon_social = db.Column(db.String(200))
    percibe_asignaciones = db.Column(db.Integer, default=0)
    observaciones = db.Column(db.Text)
    
    # Relación
    declaracion = db.relationship('DeclaracionJurada', backref='conyuge')


class Auditoria(db.Model):
    """Modelo de auditoría del sistema"""
    __tablename__ = 'auditoria'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50))
    rol = db.Column(db.String(20))
    accion = db.Column(db.String(50), nullable=False)
    legajo_id = db.Column(db.String(20))
    documento_id = db.Column(db.Integer)
    ddjj_id = db.Column(db.Integer)
    detalle = db.Column(db.Text)
    ip = db.Column(db.String(50))
    user_agent = db.Column(db.Text)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    hash_previo = db.Column(db.String(256))
    hash_nuevo = db.Column(db.String(256))
    
    def __repr__(self):
        return f'<Auditoria {self.usuario} - {self.accion} - {self.fecha}>'


class Alerta(db.Model):
    """Modelo de alertas del sistema"""
    __tablename__ = 'alertas'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # INFO, WARNING, ERROR
    mensaje = db.Column(db.Text, nullable=False)
    usuario = db.Column(db.String(50))
    legajo_id = db.Column(db.String(20))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    leida = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Alerta {self.tipo} - {self.mensaje[:50]}>'


class Backup(db.Model):
    """Modelo de respaldos del sistema"""
    __tablename__ = 'backups'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_archivo = db.Column(db.String(255), nullable=False)
    ruta_archivo = db.Column(db.String(500), nullable=False)
    tamaño = db.Column(db.Integer)  # en bytes
    fecha_backup = db.Column(db.DateTime, default=datetime.utcnow)
    usuario = db.Column(db.String(50))
    descripcion = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Backup {self.nombre_archivo} - {self.fecha_backup}>'
