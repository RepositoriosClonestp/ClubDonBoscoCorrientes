"""
Vista de Gestión de Socios
Permite agregar, editar, buscar y gestionar cuotas de socios
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QFrame,
    QDialog, QFormLayout, QComboBox, QDateEdit, QTextEdit,
    QMessageBox, QHeaderView, QAbstractItemView, QDialogButtonBox,
    QDoubleSpinBox, QSpinBox, QScrollArea
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from datetime import datetime

from config.settings import COLORS, CATEGORIAS_BASQUET, ESTADOS_PAGO
from utils.pdf_generator import PDFGenerator


class SociosView(QWidget):
    """Vista principal de gestión de socios"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.pdf_generator = PDFGenerator()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("👥 Gestión de Socios")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Barra de herramientas
        toolbar = self.create_toolbar()
        layout.addLayout(toolbar)
        
        # Buscador
        search_bar = self.create_search_bar()
        layout.addLayout(search_bar)
        
        # Tabla de socios
        self.table = self.create_socios_table()
        layout.addWidget(self.table)
        
        # Cargar datos iniciales
        self.load_socios()
    
    def create_toolbar(self) -> QHBoxLayout:
        """Crea la barra de herramientas"""
        layout = QHBoxLayout()
        
        # Botón agregar socio
        btn_add = QPushButton("➕ Nuevo Socio")
        btn_add.clicked.connect(self.show_add_socio_dialog)
        btn_add.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn_add)
        
        # Botón registrar cuota
        btn_cuota = QPushButton("💵 Registrar Cuota")
        btn_cuota.setObjectName("secondary")
        btn_cuota.clicked.connect(self.show_registrar_cuota_dialog)
        btn_cuota.setCursor(Qt.CursorShape. PointingHandCursor)
        layout.addWidget(btn_cuota)
        
        # Botón ver historial
        btn_historial = QPushButton("📋 Ver Historial")
        btn_historial.clicked.connect(self.show_historial_cuotas)
        btn_historial.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(btn_historial)
        
        layout.addStretch()
        
        # Estadísticas rápidas
        self.lbl_total = QLabel("Total: 0")
        self.lbl_total.setStyleSheet(f"color: {COLORS['primary']}; font-weight: bold; font-size: 11pt;")
        layout.addWidget(self.lbl_total)
        
        self.lbl_al_dia = QLabel("Al día: 0")
        self.lbl_al_dia.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold; font-size: 11pt;")
        layout.addWidget(self.lbl_al_dia)
        
        self. lbl_morosos = QLabel("Morosos: 0")
        self.lbl_morosos.setStyleSheet(f"color: {COLORS['danger']}; font-weight: bold; font-size: 11pt;")
        layout.addWidget(self.lbl_morosos)
        
        return layout
    
    def create_search_bar(self) -> QHBoxLayout:
        """Crea la barra de búsqueda"""
        layout = QHBoxLayout()
        
        lbl_search = QLabel("🔍 Buscar:")
        lbl_search.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl_search)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre, apellido o DNI...")
        self.search_input. textChanged.connect(self.filter_socios)
        layout.addWidget(self.search_input)
        
        return layout
    
    def create_socios_table(self) -> QTableWidget:
        """Crea la tabla de socios"""
        table = QTableWidget()
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels([
            "ID", "DNI", "Apellido", "Nombre", "Categoría", 
            "Teléfono", "Estado Pago", "Último Pago", "Acciones"
        ])
        
        # Configurar tabla
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setAlternatingRowColors(True)
        
        # Ajustar columnas
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode. Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode. Stretch)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.Fixed)
        table.setColumnWidth(8, 180)
        
        # Ocultar columna ID
        table.setColumnHidden(0, True)
        
        return table
    
    def load_socios(self):
        """Carga todos los socios en la tabla"""
        try:
            socios = self.db_manager. obtener_todos_socios()
            self.populate_table(socios)
            self.update_statistics(socios)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar socios: {str(e)}")
    
    def populate_table(self, socios: list):
        """
        Puebla la tabla con los datos de socios
        
        Args: 
            socios: Lista de diccionarios con datos de socios
        """
        self. table.setRowCount(0)
        
        for socio in socios:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # ID (oculto)
            self.table.setItem(row, 0, QTableWidgetItem(str(socio['id'])))
            
            # DNI
            self.table.setItem(row, 1, QTableWidgetItem(socio['dni']))
            
            # Apellido
            self.table.setItem(row, 2, QTableWidgetItem(socio['apellido']))
            
            # Nombre
            self.table. setItem(row, 3, QTableWidgetItem(socio['nombre']))
            
            # Categoría
            self.table.setItem(row, 4, QTableWidgetItem(socio['categoria']))
            
            # Teléfono
            telefono = socio. get('telefono', '') or '-'
            self.table.setItem(row, 5, QTableWidgetItem(telefono))
            
            # Estado de pago
            estado_item = QTableWidgetItem(ESTADOS_PAGO.get(socio['estado_pago'], 'Desconocido'))
            if socio['estado_pago'] == 'al_dia': 
                estado_item.setForeground(Qt.GlobalColor. darkGreen)
            elif socio['estado_pago'] == 'moroso':
                estado_item.setForeground(Qt.GlobalColor.red)
            estado_item.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.table.setItem(row, 6, estado_item)
            
            # Último pago
            ultimo_pago = socio.get('fecha_ultimo_pago', '') or '-'
            if ultimo_pago != '-':
                try:
                    fecha = datetime.strptime(ultimo_pago, '%Y-%m-%d')
                    ultimo_pago = fecha.strftime('%d/%m/%Y')
                except: 
                    pass
            self.table.setItem(row, 7, QTableWidgetItem(ultimo_pago))
            
            # Botones de acción
            actions_widget = self.create_action_buttons(socio['id'])
            self.table. setCellWidget(row, 8, actions_widget)
    
    def create_action_buttons(self, socio_id: int) -> QWidget:
        """
        Crea los botones de acción para cada fila
        
        Args: 
            socio_id: ID del socio
        
        Returns:
            Widget con los botones
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        layout.setSpacing(5)
        
        # Botón editar
        btn_edit = QPushButton("✏️")
        btn_edit.setFixedSize(35, 30)
        btn_edit.setToolTip("Editar socio")
        btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_edit.clicked. connect(lambda: self.edit_socio(socio_id))
        layout.addWidget(btn_edit)
        
        # Botón ver detalles
        btn_view = QPushButton("👁️")
        btn_view.setFixedSize(35, 30)
        btn_view.setToolTip("Ver detalles")
        btn_view.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_view.clicked. connect(lambda: self.view_socio_details(socio_id))
        layout.addWidget(btn_view)
        
        # Botón eliminar
        btn_delete = QPushButton("🗑️")
        btn_delete.setFixedSize(35, 30)
        btn_delete.setObjectName("danger")
        btn_delete.setToolTip("Eliminar socio")
        btn_delete.setCursor(Qt. CursorShape.PointingHandCursor)
        btn_delete.clicked.connect(lambda: self.delete_socio(socio_id))
        layout.addWidget(btn_delete)
        
        return widget
    
    def update_statistics(self, socios:  list):
        """
        Actualiza las estadísticas mostradas
        
        Args: 
            socios: Lista de socios
        """
        total = len(socios)
        al_dia = len([s for s in socios if s['estado_pago'] == 'al_dia'])
        morosos = len([s for s in socios if s['estado_pago'] == 'moroso'])
        
        self.lbl_total.setText(f"Total: {total}")
        self.lbl_al_dia. setText(f"Al día: {al_dia}")
        self.lbl_morosos.setText(f"Morosos: {morosos}")
    
    def filter_socios(self):
        """Filtra los socios según el texto de búsqueda"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table. rowCount()):
            show_row = False
            
            # Buscar en DNI, Apellido y Nombre
            for col in [1, 2, 3]: 
                item = self.table. item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            
            self.table.setRowHidden(row, not show_row)
    
    def show_add_socio_dialog(self):
        """Muestra el diálogo para agregar un nuevo socio"""
        dialog = AddSocioDialog(self.db_manager, self)
        if dialog.exec() == QDialog.DialogCode. Accepted:
            self.refresh_data()
    
    def show_registrar_cuota_dialog(self):
        """Muestra el diálogo para registrar una cuota"""
        dialog = RegistrarCuotaDialog(self.db_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
    
    def show_historial_cuotas(self):
        """Muestra el historial de cuotas de un socio"""
        # Obtener socio seleccionado
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor, seleccione un socio")
            return
        
        socio_id = int(self.table.item(current_row, 0).text())
        dialog = HistorialCuotasDialog(self.db_manager, socio_id, self)
        dialog.exec()
    
    def edit_socio(self, socio_id: int):
        """
        Edita un socio
        
        Args:
            socio_id: ID del socio a editar
        """
        dialog = EditSocioDialog(self.db_manager, socio_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
    
    def view_socio_details(self, socio_id:  int):
        """
        Muestra los detalles completos de un socio
        
        Args:
            socio_id:  ID del socio
        """
        dialog = SocioDetailsDialog(self.db_manager, socio_id, self)
        dialog.exec()
    
    def delete_socio(self, socio_id: int):
        """
        Elimina un socio (lo marca como inactivo)
        
        Args:
            socio_id:  ID del socio
        """
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Está seguro que desea eliminar este socio?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox. StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = self.db_manager.connect()
                cursor = conn.cursor()
                cursor.execute("UPDATE socios SET activo = 0 WHERE id = ?", (socio_id,))
                conn.commit()
                self.db_manager.disconnect()
                
                QMessageBox.information(self, "Éxito", "Socio eliminado correctamente")
                self.refresh_data()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar socio: {str(e)}")
    
    def refresh_data(self):
        """Recarga los datos de la tabla"""
        self.load_socios()


class AddSocioDialog(QDialog):
    """Diálogo para agregar un nuevo socio"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Agregar Nuevo Socio")
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("➕ Nuevo Socio")
        title.setStyleSheet(f"color: {COLORS['primary']}; font-size: 16pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Formulario
        form = QFormLayout()
        form.setSpacing(15)
        
        # Campos
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre")
        form.addRow("Nombre *:", self.input_nombre)
        
        self.input_apellido = QLineEdit()
        self.input_apellido.setPlaceholderText("Ingrese el apellido")
        form.addRow("Apellido *:", self.input_apellido)
        
        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("Ingrese el DNI")
        form.addRow("DNI *:", self.input_dni)
        
        self.input_fecha_nac = QDateEdit()
        self.input_fecha_nac.setCalendarPopup(True)
        self.input_fecha_nac.setDate(QDate.currentDate().addYears(-10))
        form.addRow("Fecha de Nacimiento:", self.input_fecha_nac)
        
        self.input_categoria = QComboBox()
        self.input_categoria.addItems(CATEGORIAS_BASQUET)
        form.addRow("Categoría *:", self.input_categoria)
        
        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Ej: 3794123456")
        form.addRow("Teléfono:", self.input_telefono)
        
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("ejemplo@mail.com")
        form.addRow("Email:", self.input_email)
        
        self. input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Calle y número")
        form.addRow("Dirección:", self.input_direccion)
        
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
        buttons.accepted.connect(self.save_socio)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def save_socio(self):
        """Guarda el nuevo socio"""
        # Validar campos obligatorios
        if not self. input_nombre.text().strip():
            QMessageBox.warning(self, "Advertencia", "El nombre es obligatorio")
            return
        
        if not self.input_apellido.text().strip():
            QMessageBox.warning(self, "Advertencia", "El apellido es obligatorio")
            return
        
        if not self. input_dni.text().strip():
            QMessageBox.warning(self, "Advertencia", "El DNI es obligatorio")
            return
        
        # Preparar datos
        datos = {
            'nombre': self.input_nombre.text().strip(),
            'apellido': self.input_apellido. text().strip(),
            'dni': self.input_dni.text().strip(),
            'fecha_nacimiento': self.input_fecha_nac.date().toString('yyyy-MM-dd'),
            'categoria': self.input_categoria.currentText(),
            'telefono': self.input_telefono.text().strip(),
            'email': self.input_email.text().strip(),
            'direccion': self.input_direccion.text().strip(),
            'observaciones': self.input_observaciones.toPlainText().strip()
        }
        
        try:
            socio_id = self.db_manager.agregar_socio(datos)
            QMessageBox. information(self, "Éxito", f"Socio agregado correctamente\nID: {socio_id}")
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar socio: {str(e)}")


class EditSocioDialog(QDialog):
    """Diálogo para editar un socio existente"""
    
    def __init__(self, db_manager, socio_id:  int, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.socio_id = socio_id
        self.setWindowTitle("Editar Socio")
        self.setMinimumWidth(500)
        self.init_ui()
        self.load_socio_data()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("✏️ Editar Socio")
        title.setStyleSheet(f"color:  {COLORS['primary']}; font-size: 16pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Formulario
        form = QFormLayout()
        form.setSpacing(15)
        
        self.input_nombre = QLineEdit()
        form.addRow("Nombre *:", self.input_nombre)
        
        self.input_apellido = QLineEdit()
        form.addRow("Apellido *:", self.input_apellido)
        
        self.input_categoria = QComboBox()
        self.input_categoria.addItems(CATEGORIAS_BASQUET)
        form.addRow("Categoría *:", self.input_categoria)
        
        self.input_telefono = QLineEdit()
        form.addRow("Teléfono:", self.input_telefono)
        
        self.input_email = QLineEdit()
        form.addRow("Email:", self.input_email)
        
        self.input_direccion = QLineEdit()
        form.addRow("Dirección:", self.input_direccion)
        
        self.input_observaciones = QTextEdit()
        self.input_observaciones.setMaximumHeight(80)
        form.addRow("Observaciones:", self.input_observaciones)
        
        layout.addLayout(form)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.save_changes)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def load_socio_data(self):
        """Carga los datos del socio"""
        try:
            conn = self.db_manager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM socios WHERE id = ?", (self. socio_id,))
            socio = dict(cursor.fetchone())
            self.db_manager.disconnect()
            
            self.input_nombre.setText(socio['nombre'])
            self.input_apellido.setText(socio['apellido'])
            self.input_categoria.setCurrentText(socio['categoria'])
            self.input_telefono.setText(socio. get('telefono', '') or '')
            self.input_email.setText(socio.get('email', '') or '')
            self.input_direccion.setText(socio.get('direccion', '') or '')
            self.input_observaciones.setPlainText(socio.get('observaciones', '') or '')
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")
    
    def save_changes(self):
        """Guarda los cambios"""
        if not self.input_nombre.text().strip() or not self.input_apellido.text().strip():
            QMessageBox.warning(self, "Advertencia", "Nombre y apellido son obligatorios")
            return
        
        datos = {
            'nombre': self.input_nombre.text().strip(),
            'apellido': self.input_apellido.text().strip(),
            'categoria': self.input_categoria.currentText(),
            'telefono': self. input_telefono.text().strip(),
            'email': self. input_email.text().strip(),
            'direccion': self. input_direccion.text().strip(),
            'observaciones': self.input_observaciones.toPlainText().strip()
        }
        
        try:
            self.db_manager.actualizar_socio(self.socio_id, datos)
            QMessageBox.information(self, "Éxito", "Socio actualizado correctamente")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al actualizar:  {str(e)}")


class RegistrarCuotaDialog(QDialog):
    """Diálogo para registrar el pago de una cuota"""
    
    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.setWindowTitle("Registrar Pago de Cuota")
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("💵 Registrar Pago de Cuota")
        title.setStyleSheet(f"color:  {COLORS['primary']}; font-size: 16pt; font-weight: bold;")
        layout.addWidget(title)
        
        # Formulario
        form = QFormLayout()
        form.setSpacing(15)
        
        # DNI del socio
        dni_layout = QHBoxLayout()
        self.input_dni = QLineEdit()
        self.input_dni.setPlaceholderText("Ingrese DNI del socio")
        dni_layout.addWidget(self. input_dni)
        
        btn_buscar = QPushButton("🔍 Buscar")
        btn_buscar.clicked. connect(self.buscar_socio)
        dni_layout. addWidget(btn_buscar)
        
        form.addRow("DNI Socio *:", dni_layout)
        
        # Información del socio
        self.lbl_socio_info = QLabel("Seleccione un socio")
        self.lbl_socio_info.setStyleSheet(f"color: {COLORS['text']}; padding: 10px; background-color: {COLORS['background']}; border-radius: 5px;")
        self.lbl_socio_info.setWordWrap(True)
        form.addRow("", self.lbl_socio_info)
        
        # Mes y año
        mes_anio_layout = QHBoxLayout()
        
        self.input_mes = QComboBox()
        self.input_mes. addItems([
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ])
        self.input_mes.setCurrentIndex(datetime.now().month - 1)
        mes_anio_layout.addWidget(self.input_mes)
        
        self.input_anio = QSpinBox()
        self.input_anio.setRange(2020, 2030)
        self.input_anio.setValue(datetime.now().year)
        mes_anio_layout.addWidget(self.input_anio)
        
        form.addRow("Mes/Año *:", mes_anio_layout)
        
        # Monto
        self.input_monto = QDoubleSpinBox()
        self.input_monto.setPrefix("$ ")
        self.input_monto.setRange(0, 999999)
        self.input_monto.setValue(5000)  # Valor por defecto
        self.input_monto.setDecimals(2)
        form.addRow("Monto *:", self.input_monto)
        
        # Fecha de pago
        self.input_fecha = QDateEdit()
        self.input_fecha.setCalendarPopup(True)
        self.input_fecha.setDate(QDate.currentDate())
        form.addRow("Fecha de Pago:", self.input_fecha)
        
        # Método de pago
        self.input_metodo = QComboBox()
        self.input_metodo.addItems(["Efectivo", "Transferencia", "Débito", "Crédito"])
        form.addRow("Método de Pago:", self.input_metodo)
        
        # Número de recibo
        self.input_recibo = QLineEdit()
        self.input_recibo.setPlaceholderText("Número de recibo (opcional)")
        form.addRow("N° Recibo:", self.input_recibo)
        
        layout.addLayout(form)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox. StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self. save_cuota)
        buttons.rejected. connect(self.reject)
        layout.addWidget(buttons)
        
        self.socio_actual = None
    
    def buscar_socio(self):
        """Busca un socio por DNI"""
        dni = self.input_dni.text().strip()
        
        if not dni:
            QMessageBox.warning(self, "Advertencia", "Ingrese un DNI")
            return
        
        try:
            socio = self.db_manager. buscar_socio_por_dni(dni)
            
            if socio:
                self.socio_actual = socio
                info = f"✓ {socio['apellido']}, {socio['nombre']}\n"
                info += f"Categoría: {socio['categoria']}\n"
                info += f"Estado: {ESTADOS_PAGO. get(socio['estado_pago'], 'Desconocido')}"
                
                self.lbl_socio_info.setText(info)
                self.lbl_socio_info.setStyleSheet(f"color: {COLORS['success']}; font-weight: bold; padding: 10px; background-color: #E8F5E9; border-radius: 5px;")
            else:
                self.socio_actual = None
                self.lbl_socio_info.setText("❌ No se encontró ningún socio con ese DNI")
                self. lbl_socio_info. setStyleSheet(f"color:  {COLORS['danger']}; font-weight: bold; padding:  10px; background-color:  #FFEBEE; border-radius:  5px;")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al buscar socio: {str(e)}")
    
    def save_cuota(self):
        """Guarda el pago de la cuota"""
        if not self.socio_actual:
            QMessageBox. warning(self, "Advertencia", "Primero debe buscar y seleccionar un socio")
            return
        
        datos = {
            'socio_id': self.socio_actual['id'],
            'mes': self.input_mes.currentIndex() + 1,
            'anio': self.input_anio.value(),
            'monto': self.input_monto.value(),
            'fecha_pago': self.input_fecha.date().toString('yyyy-MM-dd'),
            'metodo_pago': self.input_metodo.currentText(),
            'recibo_numero': self.input_recibo. text().strip()
        }
        
        try:
            cuota_id = self.db_manager.registrar_cuota(datos)
            
            # También registrar como ingreso en finanzas
            self.db_manager.registrar_transaccion({
                'tipo': 'ingreso',
                'categoria': 'Cuotas Socios',
                'descripcion': f"Cuota {self.input_mes.currentText()} {self.input_anio.value()} - {self.socio_actual['apellido']}, {self.socio_actual['nombre']}",
                'monto': self.input_monto.value(),
                'fecha': self.input_fecha.date().toString('yyyy-MM-dd'),
                'metodo_pago': self.input_metodo.currentText()
            })
            
            # Preguntar si desea generar recibo
            reply = QMessageBox.question(
                self,
                "Cuota Registrada",
                "Cuota registrada exitosamente.\n¿Desea generar el recibo en PDF?",
                QMessageBox. StandardButton.Yes | QMessageBox. StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self. generar_recibo(datos, cuota_id)
            
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(self, "Advertencia", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al registrar cuota: {str(e)}")
    
    def generar_recibo(self, datos:  dict, cuota_id: int):
        """Genera el recibo en PDF"""
        try:
            from utils.pdf_generator import PDFGenerator
            pdf_gen = PDFGenerator()
            
            datos_recibo = {
                'socio': f"{self.socio_actual['apellido']}, {self.socio_actual['nombre']}",
                'dni': self.socio_actual['dni'],
                'categoria': self.socio_actual['categoria'],
                'periodo': f"{self.input_mes.currentText()} {self.input_anio.value()}",
                'monto': datos['monto'],
                'metodo_pago': datos['metodo_pago'],
                'fecha':  datetime.strptime(datos['fecha_pago'], '%Y-%m-%d').strftime('%d/%m/%Y'),
                'recibo_numero': datos. get('recibo_numero', f"REC-{cuota_id: 06d}")
            }
            
            filename = pdf_gen.generar_recibo_cuota(datos_recibo)
            QMessageBox.information(self, "Éxito", f"Recibo generado:  {filename}")
            
        except Exception as e:
            QMessageBox.warning(self, "Advertencia", f"Error al generar PDF: {str(e)}")


class HistorialCuotasDialog(QDialog):
    """Diálogo para ver el historial de cuotas de un socio"""
    
    def __init__(self, db_manager, socio_id: int, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.socio_id = socio_id
        self.setWindowTitle("Historial de Cuotas")
        self.setMinimumSize(700, 500)
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Información del socio
        self.lbl_socio = QLabel()
        self.lbl_socio.setStyleSheet(f"color: {COLORS['primary']}; font-size: 14pt; font-weight: bold;")
        layout.addWidget(self.lbl_socio)
        
        # Tabla de cuotas
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Mes", "Año", "Monto", "Fecha Pago", "Método", "Recibo"
        ])
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table. setAlternatingRowColors(True)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.table)
        
        # Botón cerrar
        btn_close = QPushButton("Cerrar")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
    
    def load_data(self):
        """Carga los datos del socio y sus cuotas"""
        try: 
            # Obtener datos del socio
            conn = self.db_manager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM socios WHERE id = ?", (self.socio_id,))
            socio = dict(cursor.fetchone())
            self.db_manager.disconnect()
            
            self.lbl_socio.setText(f"📋 Historial de:  {socio['apellido']}, {socio['nombre']} (DNI: {socio['dni']})")
            
            # Obtener cuotas
            cuotas = self.db_manager.obtener_cuotas_socio(self.socio_id)
            
            self.table.setRowCount(0)
            for cuota in cuotas: 
                row = self.table.rowCount()
                self.table. insertRow(row)
                
                meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
                mes_nombre = meses[cuota['mes'] - 1]
                
                self.table.setItem(row, 0, QTableWidgetItem(mes_nombre))
                self.table.setItem(row, 1, QTableWidgetItem(str(cuota['anio'])))
                self.table. setItem(row, 2, QTableWidgetItem(f"${cuota['monto']:,.2f}"))
                
                fecha = datetime.strptime(cuota['fecha_pago'], '%Y-%m-%d').strftime('%d/%m/%Y')
                self.table.setItem(row, 3, QTableWidgetItem(fecha))
                
                self.table.setItem(row, 4, QTableWidgetItem(cuota. get('metodo_pago', '-')))
                self.table. setItem(row, 5, QTableWidgetItem(cuota.get('recibo_numero', '-') or '-'))
            
            if not cuotas:
                self. table.setRowCount(1)
                item = QTableWidgetItem("No hay cuotas registradas")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(0, 0, item)
                self.table.setSpan(0, 0, 1, 6)
        
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"Error al cargar historial: {str(e)}")


class SocioDetailsDialog(QDialog):
    """Diálogo para mostrar todos los detalles de un socio"""
    
    def __init__(self, db_manager, socio_id: int, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.socio_id = socio_id
        self.setWindowTitle("Detalles del Socio")
        self.setMinimumWidth(600)
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        
        # Título
        self.lbl_title = QLabel()
        self.lbl_title.setStyleSheet(f"color: {COLORS['primary']}; font-size: 16pt; font-weight: bold;")
        container_layout.addWidget(self.lbl_title)
        
        # Card con información
        card = QFrame()
        card.setObjectName("card")
        card_layout = QFormLayout(card)
        card_layout.setSpacing(10)
        
        self.lbl_dni = QLabel()
        card_layout.addRow("DNI:", self.lbl_dni)
        
        self.lbl_fecha_nac = QLabel()
        card_layout.addRow("Fecha de Nacimiento:", self. lbl_fecha_nac)
        
        self.lbl_categoria = QLabel()
        card_layout.addRow("Categoría:", self.lbl_categoria)
        
        self.lbl_telefono = QLabel()
        card_layout.addRow("Teléfono:", self.lbl_telefono)
        
        self.lbl_email = QLabel()
        card_layout. addRow("Email:", self.lbl_email)
        
        self.lbl_direccion = QLabel()
        card_layout.addRow("Dirección:", self.lbl_direccion)
        
        self. lbl_fecha_inscripcion = QLabel()
        card_layout.addRow("Fecha de Inscripción:", self.lbl_fecha_inscripcion)
        
        self. lbl_estado = QLabel()
        card_layout.addRow("Estado de Pago:", self.lbl_estado)
        
        self.lbl_ultimo_pago = QLabel()
        card_layout.addRow("Último Pago:", self. lbl_ultimo_pago)
        
        self.lbl_observaciones = QLabel()
        self.lbl_observaciones.setWordWrap(True)
        card_layout.addRow("Observaciones:", self.lbl_observaciones)
        
        container_layout.addWidget(card)
        
        scroll.setWidget(container)
        layout.addWidget(scroll)
        
        # Botón cerrar
        btn_close = QPushButton("Cerrar")
        btn_close.clicked. connect(self.accept)
        layout.addWidget(btn_close)
    
    def load_data(self):
        """Carga los datos del socio"""
        try:
            conn = self.db_manager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM socios WHERE id = ?", (self.socio_id,))
            socio = dict(cursor.fetchone())
            self.db_manager.disconnect()
            
            self.lbl_title.setText(f"👤 {socio['apellido']}, {socio['nombre']}")
            self.lbl_dni.setText(socio['dni'])
            
            if socio. get('fecha_nacimiento'):
                fecha_nac = datetime.strptime(socio['fecha_nacimiento'], '%Y-%m-%d')
                edad = datetime.now().year - fecha_nac.year
                self.lbl_fecha_nac.setText(f"{fecha_nac.strftime('%d/%m/%Y')} ({edad} años)")
            else:
                self.lbl_fecha_nac.setText("-")
            
            self.lbl_categoria.setText(socio['categoria'])
            self.lbl_telefono.setText(socio. get('telefono', '-') or '-')
            self.lbl_email.setText(socio.get('email', '-') or '-')
            self.lbl_direccion.setText(socio.get('direccion', '-') or '-')
            
            if socio.get('fecha_inscripcion'):
                fecha_insc = datetime.strptime(socio['fecha_inscripcion'], '%Y-%m-%d')
                self.lbl_fecha_inscripcion.setText(fecha_insc.strftime('%d/%m/%Y'))
            else:
                self.lbl_fecha_inscripcion.setText("-")
            
            estado_text = ESTADOS_PAGO.get(socio['estado_pago'], 'Desconocido')
            color = COLORS['success'] if socio['estado_pago'] == 'al_dia' else COLORS['danger']
            self.lbl_estado.setText(f"<b style='color:  {color};'>{estado_text}</b>")
            
            if socio.get('fecha_ultimo_pago'):
                fecha_pago = datetime.strptime(socio['fecha_ultimo_pago'], '%Y-%m-%d')
                self.lbl_ultimo_pago.setText(fecha_pago.strftime('%d/%m/%Y'))
            else:
                self.lbl_ultimo_pago.setText("-")
            
            self.lbl_observaciones.setText(socio.get('observaciones', '-') or '-')
        
        except Exception as e: 
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")