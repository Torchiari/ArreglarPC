from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

ANCHO = 420
ALTO = 472

def generar_pdf_boleta(nombre_cliente, fecha, detalle, valor, id_cliente, id_artefacto):
    carpeta_salida = "boletas"
    os.makedirs(carpeta_salida, exist_ok=True)

    nombre_pdf = f"boleta_{id_cliente}_{id_artefacto}.pdf"
    ruta_salida = os.path.join(carpeta_salida, nombre_pdf)

    ruta_template = os.path.join("assets", "boleta_plantilla.jpg")

    c = canvas.Canvas(ruta_salida, pagesize=(ANCHO, ALTO))

    template = ImageReader(ruta_template)
    c.drawImage(template, 0, 0, width=ANCHO, height=ALTO)

    c.setFont("Helvetica-Bold", 12)

    # --- NOMBRE DEL CLIENTE ---
    c.drawString(60, 295, nombre_cliente.upper())

    # --- FECHA ---
    c.drawString(130, 233, fecha)

    # --- DESCRIPCIÓN ---
    c.drawString(25, 180, detalle)

    # --- PRECIO ---
    texto_valor = f"${valor}"
    c.drawString(350, 180, texto_valor)

    # --- SUBTOTAL ---
    c.drawString(350, 35, texto_valor)

    # --- TOTAL ---
    c.drawString(350, 20, texto_valor)

    c.save()
    return ruta_salida
