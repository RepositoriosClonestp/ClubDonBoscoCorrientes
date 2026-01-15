# 🏀 Sistema de Gestión Integral - Club Don Bosco

Sistema de escritorio profesional para la gestión administrativa, financiera y de socios del **Club Don Bosco de Básquet** en Corrientes, Argentina.

## 🎯 Características Principales

### 📊 Dashboard Interactivo
- Resumen financiero en tiempo real (Ingresos, Egresos, Balance)
- Estadísticas de socios (Totales, Al día, Morosos)
- Alertas automáticas de vencimientos y deudas
- Información de sponsors activos

### 👥 Gestión de Socios
- Registro completo de socios con datos personales
- Categorías de básquet (Mini, U11, U13, U15, U17, U19, Mayores, etc.)
- Control de estado de pagos (Al día / Moroso / Exento)
- Búsqueda rápida por DNI, nombre o apellido
- Historial completo de cuotas pagadas

### 💵 Gestión de Cuotas
- Registro de pagos mensuales
- Múltiples métodos de pago (Efectivo, Transferencia, Débito, Crédito)
- Generación automática de recibos en PDF
- Actualización automática del estado del socio

### 💰 Gestión Financiera
- Registro de ingresos y egresos categorizados
- Balance general en tiempo real
- Filtros por período de tiempo (Hoy, Semana, Mes, Personalizado)
- Exportación a Excel de transacciones
- Categorías predefinidas para mejor organización

### 🤝 Gestión de Sponsors
- Registro de empresas patrocinadoras
- Control de contratos y montos
- Alertas de vencimientos próximos (30 días)
- Tipos de patrocinio (Indumentaria, Monetario, Equipamiento, etc.)
- Historial de renovaciones

## 🛠️ Stack Tecnológico

- **Lenguaje:** Python 3.10+
- **GUI Framework:** PyQt6
- **Base de Datos:** SQLite
- **Generación PDF:** ReportLab
- **Exportación Excel:** OpenPyXL
- **Análisis de Datos:** Pandas

## 📋 Requisitos del Sistema

- Windows 10/11
- Python 3.10 o superior
- 4 GB RAM mínimo
- 500 MB espacio en disco

## 🚀 Instalación

### 1. Clonar o descargar el proyecto

```bash
git clone https://github.com/RepositoriosClonestp/ClubDonBoscoCorrientes. git
cd ClubDonBoscoCorrientes
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Colocar el logo

Copiar el archivo `logo.png` del club en la carpeta `assets/`

### 6. Ejecutar la aplicación

```bash
python main.py
```

## 📁 Estructura del Proyecto

```
club_donbosco/
│
├── main.py                          # Punto de entrada
├── requirements.txt                 # Dependencias
├── README.md                        # Documentación
│
├── config/
│   ├── __init__.py
│   └── settings.py                  # Configuraciones globales
│
├── database/
│   ├── __init__.py
│   └── database.py                  # Gestor de base de datos
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py               # Ventana principal
│   ├── styles.py                    # Estilos CSS
│   │
│   └── views/
│       ├── __init__.py
│       ├── dashboard_view.py        # Vista Dashboard
│       ├── socios_view.py           # Vista Socios
│       ├── finanzas_view.py         # Vista Finanzas
│       └── sponsors_view.py         # Vista Sponsors
│
├── utils/
│   ├── __init__.py
│   ├── pdf_generator.py             # Generador de PDFs
│   ├── excel_exporter.py            # Exportador Excel
│   └── validators.py                # Validadores
│
├── assets/
│   └── logo.png                     # Logo del club
│
├── data/
│   └── club_donbosco.db            # Base de datos (se crea automáticamente)
│
└── exports/
    ├── recibos/                     # Recibos generados
    └── reportes/                    # Reportes exportados
```

## 🎨 Colores Institucionales

- **Azul Principal:** `#1D71B8`
- **Naranja:** `#F7941D`
- **Azul Oscuro:** `#214068`
- **Blanco:** `#FFFFFF`

## 📖 Manual de Uso

### Agregar un Nuevo Socio

1. Ir a la sección **"Socios"**
2. Hacer clic en **"➕ Nuevo Socio"**
3. Completar los datos obligatorios (Nombre, Apellido, DNI, Categoría)
4. Guardar

### Registrar una Cuota

1. Ir a la sección **"Socios"**
2. Hacer clic en **"💵 Registrar Cuota"**
3. Ingresar el DNI del socio y buscar
4. Seleccionar mes/año y monto
5. Guardar
6. Opcionalmente generar recibo en PDF

### Registrar una Transacción Financiera

1. Ir a la sección **"Finanzas"**
2. Hacer clic en **"➕ Registrar Ingreso"** o **"➖ Registrar Egreso"**
3. Completar categoría, descripción y monto
4. Guardar

### Agregar un Sponsor

1. Ir a la sección **"Sponsors"**
2. Hacer clic en **"➕ Nuevo Sponsor"**
3. Completar datos de la empresa y contrato
4. Guardar

### Exportar Datos

- **Transacciones:** Ir a Finanzas → "📄 Exportar a Excel"
- Los archivos se guardan en la carpeta `exports/`

## 🔒 Seguridad

- Base de datos local (SQLite) - sin conexión a internet requerida
- Datos almacenados localmente en el equipo
- Se recomienda realizar backups periódicos de la carpeta `data/`

## 🆘 Soporte y Contacto

Para reportar problemas o solicitar nuevas funcionalidades: 
- Email: agustinmaximilianostoppello@outlook.com.ar
- Teléfono: +54 379 4141551

## 📝 Licencia

© 2026 Agustin Stoppello - Corrientes, Argentina
Todos los derechos reservados.
