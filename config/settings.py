"""
Configuraciones globales del sistema
Club Don Bosco - Gestión Integral
"""

import os
from pathlib import Path

# Rutas del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "club_donbosco.db"
ASSETS_PATH = BASE_DIR / "assets"
EXPORTS_PATH = BASE_DIR / "exports"

# Crear directorios si no existen
os.makedirs(BASE_DIR / "data", exist_ok=True)
os.makedirs(EXPORTS_PATH, exist_ok=True)

# Colores institucionales del Club Don Bosco
COLORS = {
    'primary': '#1D71B8',      # Azul principal
    'secondary': '#F7941D',    # Naranja
    'dark': '#214068',         # Azul oscuro
    'white': '#FFFFFF',        # Blanco
    'success': '#28a745',      # Verde para estados positivos
    'danger': '#dc3545',       # Rojo para alertas
    'warning': '#ffc107',      # Amarillo para advertencias
    'background': '#F5F7FA',   # Fondo claro
    'text': '#2C3E50',         # Texto principal
    'border': '#E1E8ED'        # Bordes
}

# Información del Club
CLUB_INFO = {
    'nombre': 'Club Don Bosco',
    'ciudad': 'Corrientes',
    'deporte': 'Básquet',
    'telefono': '+54 379 4XXXXXX',
    'email': 'contacto@clubdonbosco.com. ar',
    'direccion': 'Calle Ejemplo 1234, Corrientes Capital'
}

# Categorías de Básquet
CATEGORIAS_BASQUET = [
    'Mini',
    'U11',
    'U13',
    'U15',
    'U17',
    'U19',
    'Mayores',
    'Femenino',
    'Escuelita'
]

# Categorías de Transacciones Financieras
CATEGORIAS_INGRESOS = [
    'Cuotas Socios',
    'Cantina',
    'Eventos',
    'Sponsors',
    'Donaciones',
    'Otros Ingresos'
]

CATEGORIAS_EGRESOS = [
    'Sueldos Personal',
    'Sueldos Entrenadores',
    'Mantenimiento',
    'Servicios (Luz, Agua, Gas)',
    'Material Deportivo',
    'Arbitros',
    'Transporte',
    'Otros Egresos'
]

# Estados de pago
ESTADOS_PAGO = {
    'al_dia': 'Al día',
    'moroso': 'Moroso',
    'exento': 'Exento'
}

# Configuración de la ventana principal
WINDOW_CONFIG = {
    'title': 'Club Don Bosco - Sistema de Gestión',
    'width': 1400,
    'height': 900,
    'min_width': 1200,
    'min_height':  700
}