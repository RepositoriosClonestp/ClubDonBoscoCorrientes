"""
Punto de entrada de la aplicación
Sistema de Gestión Integral - Club Don Bosco
"""

import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from pathlib import Path

from config.settings import DATABASE_PATH, ASSETS_PATH
from database.database import DatabaseManager
from ui.main_window import MainWindow


def main():
    """Función principal de la aplicación"""
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Club Don Bosco - Sistema de Gestión")
    app.setOrganizationName("Club Don Bosco")
    
    # Configurar icono de la aplicación (si existe)
    icon_path = ASSETS_PATH / "logo.png"
    if icon_path. exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Inicializar base de datos
    db_manager = DatabaseManager(DATABASE_PATH)
    
    # Crear y mostrar ventana principal
    window = MainWindow(db_manager)
    window.show()
    
    # Ejecutar aplicación
    sys.exit(app.exec())


if __name__ == '__main__':
    main()