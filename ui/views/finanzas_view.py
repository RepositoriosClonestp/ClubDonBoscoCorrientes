"""
Vista de Gestión Financiera
Permite registrar ingresos, egresos y visualizar el balance
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QFrame,
    QDialog, QFormLayout, QComboBox, QDateEdit, QTextEdit,
    QMessageBox, QHeaderView, QAbstractItemView, QDialogButtonBox,
    QDoubleSpinBox, QTabWidget, QGridLayout
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime, timedelta

from config.settings import COLORS, CATEGORIAS_INGRESOS, CATEGORIAS_EGRESOS


class FinanzasView(QWidget):
    """Vista principal de finanzas"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("💰 Gestión Financiera")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Cards de resumen
        summary_cards = self.create_summary_cards()
        layout.addLayout(summary_cards)
        
        # Barra de herramientas
        toolbar = self. create_toolbar()
        layout.addLayout(toolbar)
        
        # Filtros
        filters = self.create_filters()
        layout.addLayout(filters)
        
        # Tabs para ingresos y egresos
        self.tabs = QTabWidget()
        
        # Tab de ingresos
        self.table_ingresos = self.create_transacciones_table()
        self.tabs.addTab(self.table_ingresos, "💵 Ingresos")
        
        # Tab de egresos
        self.table_egresos = self.create_transacciones_table()
        self.tabs.addTab(self.table_egresos, "📤 Egresos")
        
        # Tab de todas las transacciones
        self. table_todas = self.create_transacciones_table()
        self.tabs.addTab(self.table_todas, "📊 Todas")
        
        layout.addWidget(self. tabs)
        
        # Cargar datos iniciales
        self. load_transacciones()
    
    def create_summary_cards(self) -> QHBoxLayout:
        """Crea las tarjetas de resumen financiero"""
        layout = QHBoxLayout()
        layout.setSpacing(20)
        
        # Card de ingresos
        self.card_ingresos = self. create_metric_card(
            "💵 Total Ingresos",
            "$0.00",
            COLORS['success']
        )
        layout.addWidget(self.card_ingresos)
        
        # Card de egresos
        self.card_egresos = self.create_metric_card(
            "📤 Total Egresos",
            "$0.00",
            COLORS['danger']
        )
        layout.addWidget(self.card_egresos)
        
        # Card de balance
        self. card_balance = self.create_metric_card(
            "💰 Balance",
            "$0.00",
            COLORS['primary']
        )
        layout.addWidget(self.card_balance)
        
        return layout
    
    def create_metric_card(self, title: str, value: str, color: str) -> QFrame:
        """Crea una tarjeta de métrica"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius:  10px;
                padding:  20px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['white']}; font-size: 14pt; font-weight: 600;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {COLORS['white']}; font-size: 32pt; font-weight: bold;")
        layout.addWidget(value_label)
        
        card.value_label = value_label
        return card
    
    def create_toolbar(self) -> QHBoxLayout:
        """Crea la barra de herramientas"""
        layout = QHBoxLayout()
        
        btn_ingreso = QPushButton("➕ Registrar Ingreso")
        btn_ingreso.clicked.connect(lambda: self.show_add_transaccion_dialog('ingreso'))
        btn_ingreso.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn_ingreso)
        
        btn_egreso = QPushButton("➖ Registrar Egreso")
        btn_egreso.setObjectName("secondary")
        btn_egreso. clicked.connect(lambda: self. show_add_transaccion_dialog('egreso'))
        btn_egreso.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn_egreso)
        
        btn_exportar = QPushButton("📄 Exportar a Excel")
        btn_exportar.clicked. connect(self.exportar_excel)
        btn_exportar. setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn_exportar)
        
        layout.addStretch()
        
        return layout
    
    def create_filters(self) -> QHBoxLayout:
        """Crea los filtros de fecha"""
        layout = QHBoxLayout()
        
        lbl_desde = QLabel("Desde:")
        lbl_desde.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl_desde)
        
        self.filter_desde = QDateEdit()
        self.filter_desde.setCalendarPopup(True)
        self.filter_desde.setDate(QDate.currentDate().addMonths(-1))
        self.filter_desde.dateChanged.connect(self.load_transacciones)
        layout.addWidget(self.filter_desde)
        
        lbl_hasta = QLabel("Hasta:")
        lbl_hasta.setStyleSheet("font-weight:  bold;")
        layout.addWidget(lbl_hasta)
        
        self.filter_hasta = QDateEdit()
        self.filter_hasta.setCalendarPopup(True)
        self.filter_hasta.setDate(QDate.currentDate())
        self.filter_hasta.dateChanged.connect(self.load_transacciones)
        layout.addWidget(self.filter_hasta)
        
        btn_hoy = QPushButton("Hoy")
        btn_hoy.clicked.connect(self. filtrar_hoy)
        layout.addWidget(btn_hoy)
        
        btn_semana = QPushButton("Esta Semana")
        btn_semana.clicked.connect(self. filtrar_semana)
        layout.addWidget(btn_semana)
        
        btn_mes = QPushButton("Este Mes")
        btn_mes.clicked.connect(self.filtrar_mes)
        layout.addWidget(btn_mes)
        
        layout.addStretch()
        
        return layout
    
    def create_transacciones_table(self) -> QTableWidget:
        """Crea una tabla de transacciones"""
        table = QTableWidget()
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "ID", "Fecha", "Tipo", "Categoría", "Descripción", "Monto", "Método", "Acciones"
        ])
        
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setAlternatingRowColors(True)
        
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode. Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode. ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(7, 100)
        
        table.setColumnHidden(0, True)
        
        return table
    
    def filtrar_hoy(self):
        """Filtra transacciones de hoy"""
        self.filter_desde.setDate(QDate.currentDate())
        self.filter_hasta. setDate(QDate.currentDate())
    
    def filtrar_semana(self):
        """Filtra transacciones de esta semana"""
        hoy = QDate.currentDate()
        inicio_semana = hoy. addDays(-hoy.dayOfWeek() + 1)
        self.filter_desde.setDate(inicio_semana)
        self.filter_hasta.setDate(hoy)
    
    def filtrar_mes(self):
        """Filtra transacciones de este mes"""
        hoy = QDate.currentDate()
        inicio_mes = QDate(hoy.year(), hoy.month(), 1)
        self.filter_desde.setDate(inicio_mes)
        self.filter_hasta.setDate(hoy)
    
    def load_transacciones(self):
        """Carga las transacciones según los filtros"""
        try: 
            fecha_desde = self.filter_desde.date().toString('yyyy-MM-dd')
            fecha_hasta = self.filter_hasta.date().toString('yyyy-MM-dd')
            
            transacciones = self.db_manager.obtener_transacciones_periodo(fecha_desde, fecha_hasta)
            
            # Filtrar por tipo
            ingresos = [t for t in transacciones if t['tipo'] == 'ingreso']
            egresos = [t for t in transacciones if t['tipo'] == 'egreso']
            
            # Poblar tablas
            self.populate_table(self.table_ingresos, ingresos)
            self.populate_table(self.table_egresos, egresos)
            self.populate_table(self.table_todas, transacciones)
            
            # Actualizar totales
            self.update_totals(ingresos, egresos)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar transacciones:  {str(e)}")
    
    def populate_table(self, table: QTableWidget, transacciones: list):
        """Puebla una tabla con transacciones"""
        table.setRowCount(0)
        
        for trans in transacciones:
            row = table.rowCount()
            table.insertRow(row)
            
            table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            
            fecha = datetime.strptime(trans['fecha'], '%Y-%m-%d').strftime('%d/%m/%Y')
            table.setItem(row, 1, QTableWidgetItem(fecha))
            
            tipo_item = QTableWidgetItem(trans['tipo']. capitalize())
            if trans['tipo'] == 'ingreso':
                tipo_item. setForeground(Qt.GlobalColor.darkGreen)
            else:
                tipo_item.setForeground(Qt.GlobalColor.red)
            tipo_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            table.setItem(row, 2, tipo_item)
            
            table.setItem(row, 3, QTableWidgetItem(trans['categoria']))
            table.setItem(row, 4, QTableWidgetItem(trans['descripcion']))
            
            monto_item = QTableWidgetItem(f"${trans['monto']: ,.2f}")
            monto_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            table.setItem(row, 5, monto_item)
            
            metodo = trans. get('metodo_pago', '-') or '-'
            table.setItem(row, 6, QTableWidgetItem(metodo))
            
            actions_widget = self.create_action_buttons(trans['id'])
            table.setCellWidget(row, 7, actions_widget)
    
    def create_action_buttons(self, transaccion_id: int) -> QWidget:
        """Crea botones de acción para cada transacción"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(40, 30)
        btn_delete.setObjectName("danger")
        btn_delete.setToolTip("Eliminar")
        btn_delete.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_delete.clicked. connect(lambda: self.delete_transaccion(transaccion_id))
        layout.addWidget(btn_delete)
        
        return widget
    
    def update_totals(self, ingresos: list, egresos:  list):
        """Actualiza los totales en las cards"""
        total_ingresos = sum(t['monto'] for t in ingresos)
        total_egresos = sum(t['monto'] for t in egresos)
        balance = total_ingresos - total_egresos
        
        self.card_ingresos. value_label.setText(f"${total_ingresos:,.2f}")
        self.card_egresos.value_label. setText(f"${total_egresos:,.2f}")
        self.card_balance.value_label.setText(f"${balance:,.2f}")
        
        # Cambiar color del balance según sea positivo o negativo
        if balance >= 0:
            color = COLORS['success']
        else:
            color = COLORS['danger']
        
        self.card_balance.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 20px;
            }}
        """)
    
    def show_add_transaccion_dialog(self, tipo: str):
        """Muestra el diálogo para agregar transacción"""
        dialog = AddTransaccionDialog(self. db_manager, tipo, self)
        if dialog.exec() == QDialog.DialogCode. Accepted:
            self.refresh_data()
    
    def delete_transaccion(self, transaccion_id: int):
        """Elimina una transacción"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro que desea eliminar esta transacción?",
            QMessageBox. StandardButton.Yes | QMessageBox.StandardButton. No
        )
        
        if reply == QMessageBox. StandardButton.Yes:
            try:
                conn = self.db_manager.connect()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transacciones WHERE id = ? ", (transaccion_id,))
                conn.commit()
                self.db_manager.disconnect()
                
                QMessageBox.information(self, "Éxito", "Transacción eliminada correctamente")
                self.refresh_data()
            except Exception as e:
                QMessageBox. critical(self, "Error", f"Error al eliminar:  {str(e)}")
    
    def exportar_excel(self):
        """Exporta las transacciones a Excel"""
        try:
            from utils.excel_exporter import ExcelExporter
            exporter = ExcelExporter()
            
            fecha_desde = self.filter_desde.date().toString('yyyy-MM-dd')
            fecha_hasta = self.filter_hasta.date().toString('yyyy-MM-dd')
            
            transacciones = self.db_manager.obtener_transacciones_periodo(fecha_desde, fecha_hasta)
            
            filename = exporter.exportar_transacciones(transacciones, fecha_desde, fecha_hasta)
            QMessageBox.information(self, "Éxito", f"Archivo exportado: {filename}")
            
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"Error al exportar:  {str(e)}")
    
    def refresh_data(self):
        """Recarga los datos"""
        self.load_transacciones()


class AddTransaccionDialog(QDialog):
    """Diálogo para agregar una transacción"""
    
    def __init__(self, db_manager, tipo: str, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.tipo = tipo
        self. setWindowTitle(f"Registrar {tipo.capitalize()}")
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Título
        icono = "💵" if self.tipo == 'ingreso' else "📤"
        title = QLabel(f"{icono} Registrar {self.tipo.capitalize()}")
        title.setStyleSheet(f"color: {COLORS['primary']}; font-size: 16pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Formulario
        form = QFormLayout()
        form.setSpacing(15)
        
        # Categoría
        self.input_categoria = QComboBox()
        if self.tipo == 'ingreso':
            self.input_categoria.addItems(CATEGORIAS_INGRESOS)
        else:
            self.input_categoria.addItems(CATEGORIAS_EGRESOS)
        form.addRow("Categoría *:", self.input_categoria)
        
        # Descripción
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setPlaceholderText("Descripción de la transacción")
        form.addRow("Descripción *:", self.input_descripcion)
        
        # Monto
        self.input_monto = QDoubleSpinBox()
        self.input_monto.setPrefix("$ ")
        self.input_monto.setRange(0, 9999999)
        self.input_monto.setDecimals(2)
        form.addRow("Monto *:", self.input_monto)
        
        # Fecha
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        form.addRow("Fecha:", self.input_fecha)
        
        # Método de pago
        self.input_metodo = QComboBox()
        self.input_metodo.addItems(["Efectivo", "Transferencia", "Débito", "Crédito", "Cheque"])
        form.addRow("Método de Pago:", self.input_metodo)
        
        # Comprobante
        self.input_comprobante = QLineEdit()
        self.input_comprobante.setPlaceholderText("Número de comprobante (opcional)")
        form.addRow("Comprobante:", self. input_comprobante)
        
        # Responsable
        self.input_responsable = QLineEdit()
        self.input_responsable.setPlaceholderText("Persona responsable")
        form.addRow("Responsable:", self.input_responsable)
        
        # Observaciones
        self.input_observaciones = QTextEdit()
        self.input_observaciones.setMaximumHeight(80)
        self.input_observaciones.setPlaceholderText("Observaciones adicionales...")
        form.addRow("Observaciones:", self.input_observaciones)
        
        layout.addLayout(form)
        
        # Nota
        note = QLabel("* Campos obligatorios")
        note.setStyleSheet(f"color: {COLORS['danger']}; font-size: 9pt; font-style: italic;")
        layout.addWidget(note)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_transaccion)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def save_transaccion(self):
        """Guarda la transacción"""
        if not self.input_descripcion.text().strip():
            QMessageBox. warning(self, "Advertencia", "La descripción es obligatoria")
            return
        
        if self.input_monto.value() <= 0:
            QMessageBox.warning(self, "Advertencia", "El monto debe ser mayor a cero")
            return
        
        datos = {
            'tipo': self.tipo,
            'categoria': self.input_categoria. currentText(),
            'descripcion': self.input_descripcion. text().strip(),
            'monto': self.input_monto.value(),
            'fecha': self.input_fecha.date().toString('yyyy-MM-dd'),
            'metodo_pago': self.input_metodo.currentText(),
            'comprobante': self.input_comprobante.text().strip(),
            'responsable': self.input_responsable.text().strip(),
            'observaciones': self. input_observaciones.toPlainText().strip()
        }
        
        try:
            transaccion_id = self.db_manager.registrar_transaccion(datos)
            QMessageBox.information(self, "Éxito", f"Transacción registrada correctamente\nID: {transaccion_id}")
            self.accept()
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")