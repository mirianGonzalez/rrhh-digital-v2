# ======================================
# MÓDULO PARA GENERAR HASH DE DOCUMENTOS
# ======================================
import hashlib

def generar_hash(texto: str) -> str:
    """
    Genera un hash SHA256 de cualquier texto
    """
    sha = hashlib.sha256()
    sha.update(texto.encode("utf-8"))
    return sha.hexdigest()