"""
Vista del Dashboard principal
Muestra resumen financiero y estadísticas del club
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config.settings import COLORS


class DashboardView(QWidget):
    """Vista principal del dashboard"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del dashboard"""
        # Layout principal con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape. NoFrame)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("📊 Dashboard - Panel de Control")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Subtítulo con fecha actual
        from datetime import datetime
        subtitle = QLabel(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        subtitle.setStyleSheet(f"color: {COLORS['text']}; font-size: 11pt;")
        layout.addWidget(subtitle)
        
        # Tarjetas de resumen financiero
        financial_cards = self.create_financial_cards()
        layout.addLayout(financial_cards)
        
        # Tarjetas de estadísticas
        stats_cards = self.create_stats_cards()
        layout.addLayout(stats_cards)
        
        # Alertas y notificaciones
        alerts_section = self.create_alerts_section()
        layout.addWidget(alerts_section)
        
        # Espaciador
        layout.addStretch()
        
        scroll.setWidget(container)
        
        main_layout = QVBoxLayout(self)
        main_layout. setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(scroll)
    
    def create_financial_cards(self) -> QHBoxLayout:
        """
        Crea las tarjetas de resumen financiero
        
        Returns:
            Layout con las tarjetas
        """
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Tarjeta de Ingresos
        self.card_ingresos = self.create_metric_card(
            "💵 Total Ingresos",
            "$0. 00",
            COLORS['success'],
            "card_primary"
        )
        layout.addWidget(self.card_ingresos)
        
        # Tarjeta de Egresos
        self.card_egresos = self.create_metric_card(
            "📤 Total Egresos",
            "$0.00",
            COLORS['danger'],
            "card_secondary"
        )
        layout.addWidget(self.card_egresos)
        
        # Tarjeta de Balance
        self.card_balance = self.create_metric_card(
            "💰 Balance Total",
            "$0.00",
            COLORS['primary'],
            "card_primary"
        )
        layout.addWidget(self.card_balance)
        
        return layout
    
    def create_stats_cards(self) -> QGridLayout:
        """
        Crea las tarjetas de estadísticas
        
        Returns: 
            Grid layout con las tarjetas
        """
        layout = QGridLayout()
        layout.setSpacing(20)
        
        # Tarjeta de Socios Totales
        self.card_socios_total = self.create_info_card(
            "👥 Socios Activos",
            "0",
            "Total de socios registrados"
        )
        layout.addWidget(self.card_socios_total, 0, 0)
        
        # Tarjeta de Socios al Día
        self.card_socios_al_dia = self.create_info_card(
            "✅ Socios al Día",
            "0",
            "Socios sin deudas"
        )
        layout.addWidget(self.card_socios_al_dia, 0, 1)
        
        # Tarjeta de Morosos
        self.card_socios_morosos = self.create_info_card(
            "⚠️ Socios Morosos",
            "0",
            "Socios con cuotas pendientes"
        )
        layout.addWidget(self.card_socios_morosos, 1, 0)
        
        # Tarjeta de Sponsors Activos
        self.card_sponsors = self.create_info_card(
            "🤝 Sponsors Activos",
            "0",
            "Empresas patrocinadoras"
        )
        layout.addWidget(self.card_sponsors, 1, 1)
        
        return layout
    
    def create_metric_card(self, title: str, value: str, color: str, style: str) -> QFrame:
        """
        Crea una tarjeta de métrica financiera
        
        Args: 
            title: Título de la tarjeta
            value: Valor a mostrar
            color: Color de fondo
            style: Nombre del estilo
        
        Returns:
            QFrame con la tarjeta
        """
        card = QFrame()
        card.setObjectName(style)
        card.setStyleSheet(f"""
            QFrame#{style} {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {COLORS['white']};
            font-size:  14pt;
            font-weight:  600;
        """)
        layout.addWidget(title_label)
        
        # Valor
        value_label = QLabel(value)
        value_label. setObjectName("metric_value")
        value_label.setStyleSheet(f"""
            color: {COLORS['white']};
            font-size:  36pt;
            font-weight:  bold;
        """)
        layout.addWidget(value_label)
        
        # Guardar referencia al label de valor para actualización
        card.value_label = value_label
        
        return card
    
    def create_info_card(self, title: str, value: str, description: str) -> QFrame:
        """
        Crea una tarjeta de información
        
        Args:
            title: Título de la tarjeta
            value: Valor a mostrar
            description: Descripción adicional
        
        Returns: 
            QFrame con la tarjeta
        """
        card = QFrame()
        card.setObjectName("card")
        card.setMinimumHeight(120)
        
        layout = QVBoxLayout(card)
        
        # Título
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color:  {COLORS['primary']};
            font-size:  12pt;
            font-weight:  600;
        """)
        layout.addWidget(title_label)
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("info_value")
        value_label.setStyleSheet(f"""
            color: {COLORS['dark']};
            font-size:  32pt;
            font-weight:  bold;
        """)
        layout.addWidget(value_label)
        
        # Descripción
        desc_label = QLabel(description)
        desc_label.setStyleSheet(f"color: {COLORS['text']}; font-size: 9pt;")
        layout.addWidget(desc_label)
        
        # Guardar referencia al label de valor
        card.value_label = value_label
        
        return card
    
    def create_alerts_section(self) -> QFrame:
        """
        Crea la sección de alertas y notificaciones
        
        Returns:
            QFrame con las alertas
        """
        section = QFrame()
        section.setObjectName("card")
        
        layout = QVBoxLayout(section)
        
        # Título
        title = QLabel("🔔 Notificaciones y Alertas")
        title.setStyleSheet(f"""
            color: {COLORS['primary']};
            font-size: 14pt;
            font-weight:  600;
        """)
        layout.addWidget(title)
        
        # Contenedor de alertas
        self.alerts_container = QVBoxLayout()
        layout.addLayout(self.alerts_container)
        
        # Mensaje por defecto
        self.no_alerts_label = QLabel("✓ No hay alertas pendientes")
        self.no_alerts_label.setStyleSheet(f"color: {COLORS['success']}; font-size: 11pt; padding: 10px;")
        self.alerts_container.addWidget(self.no_alerts_label)
        
        return section
    
    def refresh_data(self):
        """Actualiza todos los datos del dashboard"""
        try:
            # Obtener balance general
            balance = self.db_manager.obtener_balance_general()
            
            # Actualizar tarjetas financieras
            self.card_ingresos.value_label.setText(f"${balance['ingresos']: ,.2f}")
            self.card_egresos.value_label.setText(f"${balance['egresos']:,.2f}")
            self.card_balance.value_label.setText(f"${balance['balance']:,.2f}")
            
            # Obtener estadísticas de socios
            socios = self.db_manager.obtener_todos_socios()
            socios_al_dia = [s for s in socios if s['estado_pago'] == 'al_dia']
            socios_morosos = [s for s in socios if s['estado_pago'] == 'moroso']
            
            self.card_socios_total.value_label.setText(str(len(socios)))
            self.card_socios_al_dia.value_label.setText(str(len(socios_al_dia)))
            self.card_socios_morosos. value_label.setText(str(len(socios_morosos)))
            
            # Obtener sponsors activos
            sponsors = self. db_manager.obtener_sponsors_activos()
            self.card_sponsors.value_label. setText(str(len(sponsors)))
            
            # Actualizar alertas
            self.update_alerts(socios_morosos, sponsors)
            
        except Exception as e:
            print(f"Error al actualizar dashboard: {e}")
    
    def update_alerts(self, socios_morosos: list, sponsors: list):
        """
        Actualiza la sección de alertas
        
        Args:
            socios_morosos: Lista de socios con deudas
            sponsors: Lista de sponsors activos
        """
        # Limpiar alertas anteriores
        while self.alerts_container.count():
            child = self.alerts_container.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        has_alerts = False
        
        # Alerta de socios morosos
        if len(socios_morosos) > 0:
            has_alerts = True
            alert = QLabel(f"⚠️ Hay {len(socios_morosos)} socios con cuotas pendientes")
            alert.setStyleSheet(f"color: {COLORS['warning']}; font-size: 11pt; padding: 10px;")
            self.alerts_container.addWidget(alert)
        
        # Alerta de sponsors próximos a vencer
        sponsors_vencer = self.db_manager.obtener_sponsors_proximos_vencer(30)
        if len(sponsors_vencer) > 0:
            has_alerts = True
            alert = QLabel(f"📅 Hay {len(sponsors_vencer)} contratos de sponsors por vencer en 30 días")
            alert.setStyleSheet(f"color:  {COLORS['warning']}; font-size: 11pt; padding: 10px;")
            self.alerts_container.addWidget(alert)
        
        # Si no hay alertas, mostrar mensaje
        if not has_alerts: 
            no_alerts = QLabel("✓ No hay alertas pendientes")
            no_alerts.setStyleSheet(f"color: {COLORS['success']}; font-size: 11pt; padding: 10px;")
            self.alerts_container.addWidget(no_alerts)