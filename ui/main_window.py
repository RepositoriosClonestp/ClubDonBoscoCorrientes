"""
Ventana principal de la aplicación
Contiene el menú lateral y el área de contenido
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap

from config.settings import WINDOW_CONFIG, COLORS, CLUB_INFO, ASSETS_PATH
from ui.styles import get_style
from ui.views. dashboard_view import DashboardView
from ui.views.socios_view import SociosView
from ui.views. finanzas_view import FinanzasView
from ui.views. sponsors_view import SponsorsView


class MainWindow(QMainWindow):
    """Ventana principal del sistema"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self. init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Configurar ventana
        self.setWindowTitle(WINDOW_CONFIG['title'])
        self.setGeometry(100, 100, WINDOW_CONFIG['width'], WINDOW_CONFIG['height'])
        self.setMinimumSize(WINDOW_CONFIG['min_width'], WINDOW_CONFIG['min_height'])
        
        # Aplicar estilos globales
        self.setStyleSheet(get_style())
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal (horizontal:  sidebar + contenido)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Crear sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self. sidebar)
        
        # Crear área de contenido
        self.content_area = QStackedWidget()
        main_layout.addWidget(self. content_area)
        
        # Cargar vistas
        self.load_views()
        
        # Mostrar dashboard por defecto
        self.show_dashboard()
    
    def create_sidebar(self) -> QFrame:
        """
        Crea el menú lateral de navegación
        
        Returns: 
            QFrame con el menú lateral
        """
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header con logo
        header = self.create_sidebar_header()
        layout.addWidget(header)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {COLORS['primary']};")
        separator.setFixedHeight(3)
        layout.addWidget(separator)
        
        # Botones de menú
        self.btn_dashboard = self.create_menu_button("🏠  Inicio", self.show_dashboard)
        self.btn_socios = self. create_menu_button("👥  Socios", self.show_socios)
        self.btn_finanzas = self. create_menu_button("💰  Finanzas", self. show_finanzas)
        self.btn_sponsors = self. create_menu_button("🤝  Sponsors", self.show_sponsors)
        
        # Marcar botón de inicio como activo por defecto
        self.btn_dashboard.setCheckable(True)
        self.btn_socios.setCheckable(True)
        self.btn_finanzas.setCheckable(True)
        self.btn_sponsors. setCheckable(True)
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_socios)
        layout.addWidget(self.btn_finanzas)
        layout.addWidget(self. btn_sponsors)
        
        # Espaciador para empujar el footer hacia abajo
        layout.addStretch()
        
        # Footer con información
        footer = self.create_sidebar_footer()
        layout.addWidget(footer)
        
        return sidebar
    
    def create_sidebar_header(self) -> QWidget:
        """
        Crea el header del sidebar con logo y nombre del club
        
        Returns: 
            Widget con el header
        """
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLORS['dark']};")
        layout = QVBoxLayout(header)
        layout.setContentsMargins(10, 20, 10, 20)
        
        # Logo
        logo_label = QLabel()
        logo_path = ASSETS_PATH / "logo.png"
        
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            scaled_pixmap = pixmap.scaled(
                180, 180,
                Qt. AspectRatioMode. KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            logo_label.setPixmap(scaled_pixmap)
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            # Si no existe el logo, mostrar texto
            logo_label.setText(CLUB_INFO['nombre'])
            logo_label.setStyleSheet(f"""
                color: {COLORS['white']};
                font-size: 18pt;
                font-weight:  bold;
                padding: 20px;
            """)
            logo_label.setAlignment(Qt. AlignmentFlag.AlignCenter)
        
        layout.addWidget(logo_label)
        
        # Subtítulo
        subtitle = QLabel(CLUB_INFO['ciudad'])
        subtitle.setStyleSheet(f"""
            color: {COLORS['secondary']};
            font-size:  11pt;
            font-weight:  600;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag. AlignCenter)
        layout.addWidget(subtitle)
        
        return header
    
    def create_menu_button(self, text: str, callback) -> QPushButton:
        """
        Crea un botón para el menú lateral
        
        Args:
            text: Texto del botón
            callback: Función a ejecutar al hacer clic
        
        Returns:
            QPushButton configurado
        """
        button = QPushButton(text)
        button.setObjectName("menu_button")
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.clicked.connect(callback)
        
        return button
    
    def create_sidebar_footer(self) -> QWidget:
        """
        Crea el footer del sidebar con información del sistema
        
        Returns:
            Widget con el footer
        """
        footer = QWidget()
        footer.setStyleSheet(f"background-color: {COLORS['dark']}; padding: 10px;")
        layout = QVBoxLayout(footer)
        
        info_label = QLabel("Sistema de Gestión v1.0")
        info_label.setStyleSheet(f"color: {COLORS['white']}; font-size: 9pt;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info_label)
        
        year_label = QLabel("© 2026 Club Don Bosco")
        year_label.setStyleSheet(f"color: {COLORS['border']}; font-size: 8pt;")
        year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(year_label)
        
        return footer
    
    def load_views(self):
        """Carga todas las vistas de la aplicación"""
        # Dashboard
        self.dashboard_view = DashboardView(self.db_manager)
        self.content_area.addWidget(self.dashboard_view)
        
        # Socios
        self.socios_view = SociosView(self.db_manager)
        self.content_area.addWidget(self. socios_view)
        
        # Finanzas
        self.finanzas_view = FinanzasView(self. db_manager)
        self.content_area.addWidget(self.finanzas_view)
        
        # Sponsors
        self.sponsors_view = SponsorsView(self.db_manager)
        self.content_area.addWidget(self.sponsors_view)
    
    def update_menu_buttons(self, active_button: QPushButton):
        """
        Actualiza el estado visual de los botones del menú
        
        Args:
            active_button: Botón que debe quedar marcado como activo
        """
        buttons = [
            self.btn_dashboard,
            self.btn_socios,
            self.btn_finanzas,
            self.btn_sponsors
        ]
        
        for btn in buttons:
            btn.setChecked(btn == active_button)
    
    def show_dashboard(self):
        """Muestra la vista del Dashboard"""
        self.content_area.setCurrentWidget(self.dashboard_view)
        self.update_menu_buttons(self.btn_dashboard)
        self.dashboard_view.refresh_data()
    
    def show_socios(self):
        """Muestra la vista de Socios"""
        self.content_area.setCurrentWidget(self. socios_view)
        self.update_menu_buttons(self.btn_socios)
        self.socios_view.refresh_data()
    
    def show_finanzas(self):
        """Muestra la vista de Finanzas"""
        self.content_area.setCurrentWidget(self.finanzas_view)
        self.update_menu_buttons(self.btn_finanzas)
        self.finanzas_view.refresh_data()
    
    def show_sponsors(self):
        """Muestra la vista de Sponsors"""
        self.content_area.setCurrentWidget(self.sponsors_view)
        self.update_menu_buttons(self.btn_sponsors)
        self.sponsors_view.refresh_data()