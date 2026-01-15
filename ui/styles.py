"""
Hojas de estilo (QSS) para la interfaz gráfica
Estilos personalizados con los colores del Club Don Bosco
"""

from config. settings import COLORS

# Estilo global de la aplicación
GLOBAL_STYLE = f"""
    QMainWindow {{
        background-color:  {COLORS['background']};
    }}
    
    QWidget {{
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
        color: {COLORS['text']};
    }}
    
    /* Títulos */
    QLabel#title {{
        font-size: 24pt;
        font-weight:  bold;
        color: {COLORS['primary']};
        padding: 10px;
    }}
    
    QLabel#subtitle {{
        font-size: 14pt;
        font-weight: 600;
        color: {COLORS['dark']};
        padding: 5px;
    }}
    
    /* Botones principales */
    QPushButton {{
        background-color: {COLORS['primary']};
        color: {COLORS['white']};
        border: none;
        border-radius: 6px;
        padding: 10px 20px;
        font-weight: 600;
        font-size:  10pt;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['dark']};
    }}
    
    QPushButton:pressed {{
        background-color: #163451;
    }}
    
    QPushButton:disabled {{
        background-color: #CCCCCC;
        color: #666666;
    }}
    
    /* Botón secundario */
    QPushButton#secondary {{
        background-color:  {COLORS['secondary']};
    }}
    
    QPushButton#secondary:hover {{
        background-color: #E07A0D;
    }}
    
    /* Botón de peligro */
    QPushButton#danger {{
        background-color:  {COLORS['danger']};
    }}
    
    QPushButton#danger:hover {{
        background-color: #C82333;
    }}
    
    /* Campos de entrada */
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QDateEdit, QComboBox {{
        border: 2px solid {COLORS['border']};
        border-radius:  6px;
        padding:  8px;
        background-color: {COLORS['white']};
        selection-background-color: {COLORS['primary']};
    }}
    
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
        border: 2px solid {COLORS['primary']};
    }}
    
    /* Tablas */
    QTableWidget {{
        border: 1px solid {COLORS['border']};
        border-radius: 8px;
        background-color:  {COLORS['white']};
        gridline-color: {COLORS['border']};
        selection-background-color: {COLORS['primary']};
    }}
    
    QTableWidget::item {{
        padding: 8px;
    }}
    
    QHeaderView::section {{
        background-color: {COLORS['dark']};
        color: {COLORS['white']};
        padding: 10px;
        border: none;
        font-weight: bold;
    }}
    
    /* Menú lateral */
    QFrame#sidebar {{
        background-color: {COLORS['dark']};
        border-right: 3px solid {COLORS['primary']};
    }}
    
    QPushButton#menu_button {{
        background-color: transparent;
        color: {COLORS['white']};
        text-align: left;
        padding: 15px 20px;
        border: none;
        border-left: 4px solid transparent;
        font-size: 11pt;
    }}
    
    QPushButton#menu_button:hover {{
        background-color: {COLORS['primary']};
        border-left:  4px solid {COLORS['secondary']};
    }}
    
    QPushButton#menu_button:checked {{
        background-color: {COLORS['primary']};
        border-left:  4px solid {COLORS['secondary']};
        font-weight: bold;
    }}
    
    /* Tarjetas de información */
    QFrame#card {{
        background-color: {COLORS['white']};
        border: 1px solid {COLORS['border']};
        border-radius: 10px;
        padding: 15px;
    }}
    
    QFrame#card_primary {{
        background-color: {COLORS['primary']};
        border:  none;
        border-radius: 10px;
        padding: 20px;
    }}
    
    QFrame#card_secondary {{
        background-color: {COLORS['secondary']};
        border: none;
        border-radius: 10px;
        padding: 20px;
    }}
    
    QLabel#card_title {{
        color: {COLORS['white']};
        font-size:  16pt;
        font-weight: bold;
    }}
    
    QLabel#card_value {{
        color: {COLORS['white']};
        font-size: 32pt;
        font-weight:  bold;
    }}
    
    /* Mensajes de estado */
    QLabel#success {{
        color: {COLORS['success']};
        font-weight: bold;
    }}
    
    QLabel#warning {{
        color: {COLORS['warning']};
        font-weight: bold;
    }}
    
    QLabel#danger {{
        color: {COLORS['danger']};
        font-weight: bold;
    }}
    
    /* Scrollbar personalizada */
    QScrollBar: vertical {{
        border: none;
        background: {COLORS['background']};
        width: 10px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background: {COLORS['primary']};
        border-radius: 5px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background: {COLORS['dark']};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line: vertical {{
        border: none;
        background: none;
    }}
    
    /* Diálogos */
    QDialog {{
        background-color: {COLORS['background']};
    }}
    
    QMessageBox {{
        background-color: {COLORS['white']};
    }}
"""

def get_style():
    """Retorna el estilo global de la aplicación"""
    return GLOBAL_STYLE