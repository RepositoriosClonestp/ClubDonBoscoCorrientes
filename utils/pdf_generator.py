"""
Generador de PDFs
Crea recibos de cuotas y reportes financieros
"""

from reportlab.lib import colors
from reportlab.lib. pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfgen import canvas
from datetime import datetime
from pathlib import Path

from config.settings import CLUB_INFO, COLORS, EXPORTS_PATH, ASSETS_PATH


class PDFGenerator:
    """Clase para generar documentos PDF"""
    
    def __init__(self):
        self.exports_path = EXPORTS_PATH
        self. logo_path = ASSETS_PATH / "logo.png"
    
    def generar_recibo_cuota(self, datos:  dict) -> str:
        """
        Genera un recibo de pago de cuota en PDF
        
        Args: 
            datos: Diccionario con los datos del recibo
        
        Returns:
            Nombre del archivo generado
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"recibo_{datos['recibo_numero']}_{timestamp}. pdf"
        filepath = self. exports_path / filename
        
        c = canvas.Canvas(str(filepath), pagesize=letter)
        width, height = letter
        
        # Logo (si existe)
        if self.logo_path. exists():
            try:
                c.drawImage(str(self.logo_path), 50, height - 120, width=100, height=100, preserveAspectRatio=True)
            except:
                pass
        
        # Encabezado del club
        c.setFont("Helvetica-Bold", 18)
        c.drawString(170, height - 60, CLUB_INFO['nombre'])
        
        c.setFont("Helvetica", 11)
        c.drawString(170, height - 80, f"{CLUB_INFO['ciudad']} - {CLUB_INFO['deporte']}")
        c.drawString(170, height - 95, f"Tel: {CLUB_INFO['telefono']}")
        
        # Línea separadora
        c.setStrokeColorRGB(0.11, 0.44, 0.72)
        c.setLineWidth(2)
        c.line(50, height - 130, width - 50, height - 130)
        
        # Título del recibo
        c.setFillColorRGB(0.97, 0.58, 0.11)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 165, "RECIBO DE PAGO - CUOTA MENSUAL")
        
        # Número de recibo y fecha
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(width - 200, height - 165, f"N° {datos['recibo_numero']}")
        c.setFont("Helvetica", 10)
        c.drawString(width - 200, height - 180, f"Fecha: {datos['fecha']}")
        
        # Datos del socio
        y_position = height - 220
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, "DATOS DEL SOCIO")
        
        y_position -= 25
        c.setFont("Helvetica", 11)
        c.drawString(70, y_position, f"Nombre: {datos['socio']}")
        
        y_position -= 20
        c.drawString(70, y_position, f"DNI: {datos['dni']}")
        
        y_position -= 20
        c.drawString(70, y_position, f"Categoría: {datos['categoria']}")
        
        # Detalles del pago
        y_position -= 40
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_position, "DETALLES DEL PAGO")
        
        y_position -= 25
        c.setFont("Helvetica", 11)
        c.drawString(70, y_position, f"Período: {datos['periodo']}")
        
        y_position -= 20
        c.drawString(70, y_position, f"Método de Pago: {datos['metodo_pago']}")
        
        # Monto (destacado)
        y_position -= 40
        c.setFillColorRGB(0.11, 0.44, 0.72)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(70, y_position, f"MONTO TOTAL: ${datos['monto']:,. 2f}")
        
        # Pie de página
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica-Italic", 9)
        footer_text = f"Recibo generado electrónicamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        c.drawString(50, 50, footer_text)
        c.drawString(50, 35, f"{CLUB_INFO['nombre']} - {CLUB_INFO['direccion']}")
        
        c.save()
        return filename