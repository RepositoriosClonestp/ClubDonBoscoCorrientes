"""
Vista de Gestión de Sponsors
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class SponsorsView(QWidget):
    """Vista de sponsors"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        
        label = QLabel("🤝 Gestión de Sponsors\n\nEn construcción")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 24pt; color: #1D71B8; font-weight: bold;")
        layout.addWidget(label)
    
    def refresh_data(self):
        """Recarga los datos"""
        pass