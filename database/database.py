"""
Gestor de Base de Datos SQLite
Maneja todas las operaciones CRUD del sistema
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Clase para gestionar todas las operaciones de base de datos"""
    
    def __init__(self, db_path: Path):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_path:  Ruta al archivo de base de datos SQLite
        """
        self. db_path = db_path
        self.connection = None
        self.create_tables()
    
    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
            logger.info(f"Conexión exitosa a la base de datos: {self.db_path}")
            return self.connection
        except sqlite3.Error as e:
            logger. error(f"Error al conectar a la base de datos: {e}")
            raise
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            logger.info("Conexión cerrada correctamente")
    
    def create_tables(self):
        """Crea todas las tablas necesarias del sistema"""
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Tabla de Socios
            cursor. execute('''
                CREATE TABLE IF NOT EXISTS socios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    fecha_nacimiento DATE,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    categoria TEXT NOT NULL,
                    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
                    estado_pago TEXT DEFAULT 'al_dia',
                    fecha_ultimo_pago DATE,
                    observaciones TEXT,
                    activo INTEGER DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de Cuotas (Registro histórico de pagos)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cuotas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    socio_id INTEGER NOT NULL,
                    mes INTEGER NOT NULL,
                    anio INTEGER NOT NULL,
                    monto REAL NOT NULL,
                    fecha_pago DATE DEFAULT CURRENT_DATE,
                    metodo_pago TEXT,
                    recibo_numero TEXT,
                    observaciones TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (socio_id) REFERENCES socios (id) ON DELETE CASCADE,
                    UNIQUE(socio_id, mes, anio)
                )
            ''')
            
            # Tabla de Transacciones Financieras
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transacciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo TEXT NOT NULL CHECK(tipo IN ('ingreso', 'egreso')),
                    categoria TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    monto REAL NOT NULL,
                    fecha DATE DEFAULT CURRENT_DATE,
                    metodo_pago TEXT,
                    comprobante TEXT,
                    responsable TEXT,
                    observaciones TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de Sponsors
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sponsors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_empresa TEXT NOT NULL,
                    nombre_contacto TEXT,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT,
                    monto_contrato REAL NOT NULL,
                    fecha_inicio DATE NOT NULL,
                    fecha_vencimiento DATE NOT NULL,
                    estado TEXT DEFAULT 'activo',
                    tipo_patrocinio TEXT,
                    observaciones TEXT,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de Usuarios del Sistema (para control de acceso futuro)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    contrasena TEXT NOT NULL,
                    nombre_completo TEXT NOT NULL,
                    rol TEXT DEFAULT 'operador',
                    activo INTEGER DEFAULT 1,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Índices para mejorar rendimiento
            cursor. execute('CREATE INDEX IF NOT EXISTS idx_socios_dni ON socios(dni)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_cuotas_socio ON cuotas(socio_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transacciones_fecha ON transacciones(fecha)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_transacciones_tipo ON transacciones(tipo)')
            
            conn.commit()
            logger.info("Todas las tablas creadas exitosamente")
            
        except sqlite3.Error as e:
            logger.error(f"Error al crear tablas: {e}")
            conn.rollback()
            raise
        finally:
            self.disconnect()
    
    # ==================== OPERACIONES SOCIOS ====================
    
    def agregar_socio(self, datos: Dict) -> int:
        """
        Agrega un nuevo socio a la base de datos
        
        Args:
            datos: Diccionario con los datos del socio
        
        Returns:
            ID del socio creado
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO socios (nombre, apellido, dni, fecha_nacimiento, 
                                   telefono, email, direccion, categoria, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['nombre'],
                datos['apellido'],
                datos['dni'],
                datos. get('fecha_nacimiento'),
                datos.get('telefono'),
                datos.get('email'),
                datos.get('direccion'),
                datos['categoria'],
                datos.get('observaciones')
            ))
            
            conn.commit()
            socio_id = cursor.lastrowid
            logger.info(f"Socio creado exitosamente - ID: {socio_id}")
            return socio_id
            
        except sqlite3.IntegrityError:
            logger. error(f"DNI duplicado:  {datos['dni']}")
            raise ValueError("Ya existe un socio con ese DNI")
        except sqlite3.Error as e:
            logger.error(f"Error al agregar socio: {e}")
            conn.rollback()
            raise
        finally:
            self.disconnect()
    
    def obtener_todos_socios(self, solo_activos: bool = True) -> List[Dict]:
        """
        Obtiene todos los socios de la base de datos
        
        Args:
            solo_activos: Si True, solo retorna socios activos
        
        Returns:
            Lista de diccionarios con datos de socios
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            query = 'SELECT * FROM socios'
            if solo_activos: 
                query += ' WHERE activo = 1'
            query += ' ORDER BY apellido, nombre'
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            socios = [dict(row) for row in rows]
            return socios
            
        except sqlite3.Error as e:
            logger.error(f"Error al obtener socios: {e}")
            raise
        finally: 
            self.disconnect()
    
    def buscar_socio_por_dni(self, dni:  str) -> Optional[Dict]:
        """
        Busca un socio por su DNI
        
        Args:
            dni:  Número de DNI del socio
        
        Returns:
            Diccionario con datos del socio o None si no existe
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM socios WHERE dni = ?', (dni,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
            
        except sqlite3.Error as e:
            logger.error(f"Error al buscar socio: {e}")
            raise
        finally:
            self.disconnect()
    
    def actualizar_socio(self, socio_id: int, datos: Dict):
        """
        Actualiza los datos de un socio
        
        Args:
            socio_id: ID del socio a actualizar
            datos: Diccionario con los nuevos datos
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor. execute('''
                UPDATE socios 
                SET nombre = ?, apellido = ?, telefono = ?, email = ?,
                    direccion = ?, categoria = ?, observaciones = ?,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                datos['nombre'],
                datos['apellido'],
                datos. get('telefono'),
                datos.get('email'),
                datos.get('direccion'),
                datos['categoria'],
                datos. get('observaciones'),
                socio_id
            ))
            
            conn.commit()
            logger.info(f"Socio {socio_id} actualizado exitosamente")
            
        except sqlite3.Error as e:
            logger.error(f"Error al actualizar socio: {e}")
            conn.rollback()
            raise
        finally: 
            self.disconnect()
    
    def actualizar_estado_pago_socio(self, socio_id: int, estado: str, fecha_pago: str = None):
        """
        Actualiza el estado de pago de un socio
        
        Args:
            socio_id:  ID del socio
            estado:  Nuevo estado ('al_dia', 'moroso', 'exento')
            fecha_pago: Fecha del último pago
        """
        conn = self. connect()
        cursor = conn. cursor()
        
        try: 
            if fecha_pago:
                cursor.execute('''
                    UPDATE socios 
                    SET estado_pago = ?, fecha_ultimo_pago = ? 
                    WHERE id = ? 
                ''', (estado, fecha_pago, socio_id))
            else:
                cursor. execute('''
                    UPDATE socios 
                    SET estado_pago = ? 
                    WHERE id = ? 
                ''', (estado, socio_id))
            
            conn.commit()
            logger.info(f"Estado de pago actualizado - Socio ID: {socio_id}")
            
        except sqlite3.Error as e:
            logger.error(f"Error al actualizar estado de pago: {e}")
            conn.rollback()
            raise
        finally:
            self.disconnect()
    
    # ==================== OPERACIONES CUOTAS ====================
    
    def registrar_cuota(self, datos: Dict) -> int:
        """
        Registra el pago de una cuota mensual
        
        Args: 
            datos: Diccionario con datos del pago
        
        Returns: 
            ID de la cuota registrada
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO cuotas (socio_id, mes, anio, monto, fecha_pago,
                                   metodo_pago, recibo_numero, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['socio_id'],
                datos['mes'],
                datos['anio'],
                datos['monto'],
                datos. get('fecha_pago', datetime.now().date()),
                datos.get('metodo_pago'),
                datos.get('recibo_numero'),
                datos.get('observaciones')
            ))
            
            # Actualizar estado del socio
            self.actualizar_estado_pago_socio(
                datos['socio_id'],
                'al_dia',
                datos.get('fecha_pago', datetime.now().date())
            )
            
            conn.commit()
            cuota_id = cursor.lastrowid
            logger.info(f"Cuota registrada exitosamente - ID: {cuota_id}")
            return cuota_id
            
        except sqlite3.IntegrityError:
            logger. error(f"Cuota duplicada para socio {datos['socio_id']} - {datos['mes']}/{datos['anio']}")
            raise ValueError("Ya existe una cuota registrada para este mes")
        except sqlite3.Error as e:
            logger.error(f"Error al registrar cuota: {e}")
            conn.rollback()
            raise
        finally:
            self.disconnect()
    
    def obtener_cuotas_socio(self, socio_id: int) -> List[Dict]:
        """
        Obtiene todas las cuotas pagadas por un socio
        
        Args:
            socio_id: ID del socio
        
        Returns:
            Lista de cuotas
        """
        conn = self. connect()
        cursor = conn. cursor()
        
        try: 
            cursor.execute('''
                SELECT * FROM cuotas 
                WHERE socio_id = ? 
                ORDER BY anio DESC, mes DESC
            ''', (socio_id,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Error al obtener cuotas: {e}")
            raise
        finally: 
            self.disconnect()
    
    # ==================== OPERACIONES FINANZAS ====================
    
    def registrar_transaccion(self, datos: Dict) -> int:
        """
        Registra una transacción financiera (ingreso o egreso)
        
        Args:
            datos:  Diccionario con datos de la transacción
        
        Returns:
            ID de la transacción
        """
        conn = self. connect()
        cursor = conn. cursor()
        
        try: 
            cursor.execute('''
                INSERT INTO transacciones (tipo, categoria, descripcion, monto,
                                          fecha, metodo_pago, comprobante, 
                                          responsable, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['tipo'],
                datos['categoria'],
                datos['descripcion'],
                datos['monto'],
                datos.get('fecha', datetime.now().date()),
                datos.get('metodo_pago'),
                datos.get('comprobante'),
                datos. get('responsable'),
                datos.get('observaciones')
            ))
            
            conn.commit()
            transaccion_id = cursor.lastrowid
            logger.info(f"Transacción registrada - ID: {transaccion_id}")
            return transaccion_id
            
        except sqlite3.Error as e:
            logger.error(f"Error al registrar transacción: {e}")
            conn.rollback()
            raise
        finally:
            self. disconnect()
    
    def obtener_balance_general(self) -> Dict:
        """
        Calcula el balance general (ingresos totales - egresos totales)
        
        Returns:
            Diccionario con totales de ingresos, egresos y balance
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Total ingresos
            cursor.execute('''
                SELECT COALESCE(SUM(monto), 0) as total
                FROM transacciones
                WHERE tipo = 'ingreso'
            ''')
            total_ingresos = cursor.fetchone()['total']
            
            # Total egresos
            cursor.execute('''
                SELECT COALESCE(SUM(monto), 0) as total
                FROM transacciones
                WHERE tipo = 'egreso'
            ''')
            total_egresos = cursor.fetchone()['total']
            
            balance = total_ingresos - total_egresos
            
            return {
                'ingresos': float(total_ingresos),
                'egresos': float(total_egresos),
                'balance': float(balance)
            }
            
        except sqlite3.Error as e:
            logger.error(f"Error al calcular balance:  {e}")
            raise
        finally:
            self.disconnect()
    
    def obtener_transacciones_periodo(self, fecha_inicio: str, fecha_fin: str) -> List[Dict]:
        """
        Obtiene todas las transacciones en un período de tiempo
        
        Args: 
            fecha_inicio: Fecha de inicio (YYYY-MM-DD)
            fecha_fin: Fecha de fin (YYYY-MM-DD)
        
        Returns: 
            Lista de transacciones
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try: 
            cursor.execute('''
                SELECT * FROM transacciones
                WHERE fecha BETWEEN ? AND ?
                ORDER BY fecha DESC
            ''', (fecha_inicio, fecha_fin))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Error al obtener transacciones: {e}")
            raise
        finally:
            self.disconnect()
    
    # ==================== OPERACIONES SPONSORS ====================
    
    def agregar_sponsor(self, datos:  Dict) -> int:
        """
        Agrega un nuevo sponsor
        
        Args:
            datos: Diccionario con datos del sponsor
        
        Returns: 
            ID del sponsor creado
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try: 
            cursor.execute('''
                INSERT INTO sponsors (nombre_empresa, nombre_contacto, telefono,
                                     email, direccion, monto_contrato, fecha_inicio,
                                     fecha_vencimiento, tipo_patrocinio, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['nombre_empresa'],
                datos. get('nombre_contacto'),
                datos.get('telefono'),
                datos.get('email'),
                datos.get('direccion'),
                datos['monto_contrato'],
                datos['fecha_inicio'],
                datos['fecha_vencimiento'],
                datos. get('tipo_patrocinio'),
                datos.get('observaciones')
            ))
            
            conn.commit()
            sponsor_id = cursor.lastrowid
            logger.info(f"Sponsor creado - ID: {sponsor_id}")
            return sponsor_id
            
        except sqlite3.Error as e:
            logger.error(f"Error al agregar sponsor: {e}")
            conn.rollback()
            raise
        finally: 
            self.disconnect()
    
    def obtener_sponsors_activos(self) -> List[Dict]:
        """
        Obtiene todos los sponsors activos
        
        Returns:
            Lista de sponsors activos
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM sponsors
                WHERE estado = 'activo'
                ORDER BY nombre_empresa
            ''')
            
            rows = cursor. fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger. error(f"Error al obtener sponsors:  {e}")
            raise
        finally:
            self.disconnect()
    
    def obtener_sponsors_proximos_vencer(self, dias:  int = 30) -> List[Dict]:
        """
        Obtiene sponsors cuyos contratos vencen próximamente
        
        Args: 
            dias: Cantidad de días hacia adelante para buscar
        
        Returns: 
            Lista de sponsors próximos a vencer
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT * FROM sponsors
                WHERE estado = 'activo'
                AND fecha_vencimiento BETWEEN DATE('now') AND DATE('now', '+' || ?  || ' days')
                ORDER BY fecha_vencimiento
            ''', (dias,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
            
        except sqlite3.Error as e:
            logger.error(f"Error al obtener sponsors próximos a vencer: {e}")
            raise
        finally: 
            self.disconnect()