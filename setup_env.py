# =====================================================
# setup_env.py
# Script para preparar el entorno Python para DDJJ
# =====================================================

import sys
import os
import subprocess

print("=== INICIANDO CONFIGURACIÓN DEL ENTORNO DDJJ ===")

# -----------------------------
# 1️⃣ Instalar librerías externas
# -----------------------------
librerias = ["docxtpl", "python-docx", "docx2pdf", "qrcode[pil]"]

for lib in librerias:
    print(f"Instalando {lib}...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", lib])

print("Librerías externas instaladas ✅\n")

# -----------------------------
# 2️⃣ Revisar hash_documentos.py
# -----------------------------
# Ruta donde se espera hash_documentos.py
ruta_hash = r"G:\Mi unidad\RRHH_DIGITAL\pdf\hash_documentos.py"

if os.path.exists(ruta_hash):
    print(f"hash_documentos.py encontrado ✅ ({ruta_hash})")
else:
    print(f"hash_documentos.py NO encontrado ❌, se creará automáticamente en {ruta_hash}")
    os.makedirs(os.path.dirname(ruta_hash), exist_ok=True)
    with open(ruta_hash, "w", encoding="utf-8") as f:
        f.write("""import hashlib

def generar_hash(texto: str) -> str:
    h = hashlib.sha256()
    h.update(texto.encode("utf-8"))
    return h.hexdigest()
""")
    print("hash_documentos.py creado ✅")

# -----------------------------
# 3️⃣ Agregar ruta para Python
# -----------------------------
ruta_modulo = os.path.dirname(ruta_hash)
if ruta_modulo not in sys.path:
    sys.path.append(ruta_modulo)
    print(f"Ruta añadida a sys.path ✅ ({ruta_modulo})")

# -----------------------------
# 4️⃣ Probar imports
# -----------------------------
try:
    from docxtpl import DocxTemplate, InlineImage # pyright: ignore[reportMissingImports]
    from docx.shared import Mm # pyright: ignore[reportMissingImports]
    from docx2pdf import convert # pyright: ignore[reportMissingImports]
    import qrcode # pyright: ignore[reportMissingModuleSource]
    print("Librerías externas importadas correctamente ✅")
except ModuleNotFoundError as e:
    print(f"ERROR importando librerías externas: {e}")

try:
    from hash_documentos import generar_hash # pyright: ignore[reportMissingImports]
    # probar hash rápido
    h = generar_hash("test")
    print(f"hash_documentos importado correctamente ✅ Hash ejemplo: {h}")
except ModuleNotFoundError as e:
    print(f"ERROR importando hash_documentos: {e}")

print("\n=== ENTORNO DDJJ CONFIGURADO COMPLETAMENTE ✅ ===")
