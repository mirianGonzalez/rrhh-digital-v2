# ======================================
# MÓDULO PARA GENERAR QR
# ======================================
import qrcode

def generar_qr(texto: str, salida_png: str):
    """
    Genera un código QR a partir de un texto y lo guarda en salida_png
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(salida_png)