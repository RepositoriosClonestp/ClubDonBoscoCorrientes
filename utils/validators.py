"""
Validadores de datos
Funciones para validar entradas de usuario
"""

import re
from datetime import datetime


def validar_dni(dni:  str) -> bool:
    """
    Valida que el DNI sea numérico y tenga entre 7 y 8 dígitos
    
    Args:
        dni: String con el DNI
    
    Returns:
        True si es válido, False si no
    """
    if not dni:
        return False
    
    dni_limpio = dni.strip().replace('. ', '').replace(',', '')
    
    if not dni_limpio.isdigit():
        return False
    
    if len(dni_limpio) < 7 or len(dni_limpio) > 8:
        return False
    
    return True


def validar_email(email: str) -> bool:
    """
    Valida formato de email
    
    Args: 
        email: String con el email
    
    Returns:
        True si es válido, False si no
    """
    if not email:
        return True  # Email es opcional
    
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


def validar_telefono(telefono: str) -> bool:
    """
    Valida formato de teléfono argentino
    
    Args: 
        telefono: String con el teléfono
    
    Returns:
        True si es válido, False si no
    """
    if not telefono:
        return True  # Teléfono es opcional
    
    telefono_limpio = telefono. strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Debe tener entre 10 y 13 dígitos (con código de país opcional)
    if not telefono_limpio.isdigit():
        return False
    
    if len(telefono_limpio) < 10 or len(telefono_limpio) > 13:
        return False
    
    return True


def validar_monto(monto: float) -> bool:
    """
    Valida que el monto sea positivo
    
    Args: 
        monto: Valor numérico
    
    Returns: 
        True si es válido, False si no
    """
    return monto > 0


def validar_fecha(fecha_str: str, formato: str = '%Y-%m-%d') -> bool:
    """
    Valida formato de fecha
    
    Args: 
        fecha_str: String con la fecha
        formato: Formato esperado
    
    Returns: 
        True si es válido, False si no
    """
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except:
        return False


def limpiar_texto(texto: str) -> str:
    """
    Limpia un texto eliminando espacios extras y caracteres especiales
    
    Args:
        texto:  Texto a limpiar
    
    Returns:
        Texto limpio
    """
    if not texto:
        return ""
    
    # Eliminar espacios al inicio y final
    texto = texto.strip()
    
    # Reemplazar múltiples espacios por uno solo
    texto = re.sub(r'\s+', ' ', texto)
    
    return texto


def formatear_dni(dni: str) -> str:
    """
    Formatea un DNI con puntos (XX.XXX.XXX)
    
    Args:
        dni: DNI sin formato
    
    Returns:
        DNI formateado
    """
    dni_limpio = dni.strip().replace('.', '').replace(',', '')
    
    if len(dni_limpio) == 7:
        return f"{dni_limpio[0]}.{dni_limpio[1: 4]}.{dni_limpio[4:]}"
    elif len(dni_limpio) == 8:
        return f"{dni_limpio[0:2]}.{dni_limpio[2:5]}.{dni_limpio[5:]}"
    else:
        return dni_limpio


def formatear_monto(monto: float) -> str:
    """
    Formatea un monto con separadores de miles y dos decimales
    
    Args: 
        monto: Valor numérico
    
    Returns:
        String formateado
    """
    return f"${monto:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')