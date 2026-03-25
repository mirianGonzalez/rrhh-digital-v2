"""
Firma Digital de PDF - Superpone la firma en los campos correctos
"""

import os
import io
import hashlib
import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter

def firmar_pdf_digitalmente(pdf_path, nombre_firmante, cargo, 
                            tipo_firma="AGENTE", hash_anterior=None):
    """
    Agrega sello de firma digital SUPERPONIÉNDOLO sobre la página existente
    """
    
     # Coordenadas ajustadas - Tamaño de página A4: 595 x 842 puntos
    # Los valores Y más bajos = más cerca del borde inferior
    
    if tipo_firma == "AGENTE":
        # FIRMA DEL AGENTE - debe ir en el campo de la derecha
        coordenadas = {
            0: {'x': 400, 'y': 180},    # Página 1
            1: {'x': 400, 'y': 260}    # Página 2
        }
    else:  # DIRECTOR
        # SELLO Y FIRMA DEL ORGANISMO - debe ir en el campo de la izquierda
        coordenadas = {
            0: {'x': 70, 'y': 180},     # Página 1
            1: {'x': 70, 'y': 260}     # Página 2
        }
    
    # Calcular hash del PDF
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    hash_documento = hashlib.sha256(pdf_data).hexdigest()
    
    # Leer el PDF original
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    # Texto de la firma digital (MÁS PEQUEÑO)
    fecha_hora = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    # Texto más compacto para que quepa dentro de los márgenes
    firma_texto = [
        "=" * 35,
        "FIRMA DIGITAL - Ley 25.506",
        f"Firmante: {nombre_firmante[:35]}",  # Limitar longitud
        f"Cargo: {cargo[:25]}",               # Limitar longitud
        f"Fecha: {fecha_hora}",
        "=" * 35
    ]
    
    # Procesar cada página
    for i, page in enumerate(reader.pages):
        if i in coordenadas:
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=A4)
            # Fuente más pequeña
            c.setFont("Helvetica", 6)
            
            x = coordenadas[i]['x']
            y = coordenadas[i]['y']
            
            # Opcional: dibujar un rectángulo muy pequeño (o eliminarlo)
            # c.rect(x - 2, y - 2, 220, 45, stroke=1, fill=0)
            
            # Dibujar el texto de la firma
            for j, linea in enumerate(firma_texto):
                c.drawString(x, y - (j * 8), linea)
            
            c.save()
            packet.seek(0)
            
            overlay = PdfReader(packet)
            page.merge_page(overlay.pages[0])
        
        writer.add_page(page)
    
    # Guardar el PDF
    output_path = pdf_path.replace('.pdf', f'_firmado_{tipo_firma.lower()}.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    
    return output_path, hash_documento, f"FIRMA_SIMULADA_{hash_documento[:16]}"


def agregar_sello_institucion(pdf_path, sello_path, coordenadas=None):
    """Agrega el sello de la institución al PDF"""
    if coordenadas is None:
        coordenadas = {
            0: {'x': 250, 'y': 85, 'ancho': 80, 'alto': 80},
            1: {'x': 250, 'y': 110, 'ancho': 80, 'alto': 80}
        }
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for i, page in enumerate(reader.pages):
        if i in coordenadas:
            packet = io.BytesIO()
            c = canvas.Canvas(packet, pagesize=A4)
            
            # Cargar y dibujar la imagen del sello
            if os.path.exists(sello_path):
                img = ImageReader(sello_path)
                x = coordenadas[i]['x']
                y = coordenadas[i]['y']
                ancho = coordenadas[i]['ancho']
                alto = coordenadas[i]['alto']
                c.drawImage(img, x, y, width=ancho, height=alto, mask='auto')
            
            c.save()
            packet.seek(0)
            overlay = PdfReader(packet)
            page.merge_page(overlay.pages[0])
        
        writer.add_page(page)
    
    output_path = pdf_path.replace('.pdf', '_con_sello.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    
    return output_path