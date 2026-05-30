# Sistema de Gestión de Mantenimiento de Equipos

Aplicación de consola en Python con SQLite para gestionar el ciclo de vida del mantenimiento de equipos industriales.

## Requisitos

- **Python 3.8+** (no requiere librerías externas)
- **SQLite3** (incluido con Python)

## Estructura del Proyecto

```
proyecto final paradigmas/
├── schema.sql                  # Script DDL + datos de ejemplo
├── main.py                     # Punto de entrada de la aplicación
├── database.py                 # Conexión y gestión de la BD SQLite
├── models/
│   ├── __init__.py
│   ├── equipo.py               # CRUD de equipos
│   ├── tecnico.py              # CRUD de técnicos
│   └── orden_trabajo.py        # CRUD avanzado de órdenes de trabajo
├── views/
│   ├── __init__.py
│   ├── menu.py                 # Menús interactivos de consola
│   └── tabla.py                # Formateo de tablas y utilidades de consola
├── reports/
│   ├── __init__.py
│   ├── historial.py            # Historial de mantenimiento (solo lectura)
│   └── reportes.py             # Reportes y consultas especiales
└── README.md                   # Este archivo
```

## Cómo Ejecutar

Instalación y Ejecución
Requisitos
Python 3.10 o superior
pip (administrador de paquetes de Python)
Descargar el proyecto

Clonar o descargar este repositorio desde GitHub.

Instalar dependencias

Abrir una terminal en la carpeta del proyecto y ejecutar:

pip install flask

Si existe un archivo requirements.txt, ejecutar:

pip install -r requirements.txt
Ejecutar la aplicación

Desde la carpeta principal del proyecto ejecutar:

python app.py
Acceder al sistema

Una vez iniciada la aplicación, abrir el navegador y acceder a:

http://localhost:5000

o

http://127.0.0.1:5000
Base de datos

El sistema utiliza SQLite para almacenar la información.

Si es necesario crear las tablas manualmente, utilizar el archivo:

schema.sql
Estructura del Proyecto
app.py              -> Aplicación principal Flask
database.py         -> Conexión a la base de datos
models/             -> Modelos de datos
views/              -> Controladores y vistas
templates/          -> Plantillas HTML
static/             -> Archivos CSS, JS e imágenes
reports/            -> Reportes generados

Al ejecutar por primera vez, el sistema:
1. Crea la base de datos `mantenimiento.db`
2. Ejecuta `schema.sql` para crear tablas e insertar datos de ejemplo
3. Muestra el menú principal interactivo

## Funcionalidades

### 1. Gestión de Equipos (CRUD)
- Listar, buscar, crear, actualizar y eliminar equipos
- Estados: operativo, en mantenimiento, fuera de servicio

### 2. Gestión de Técnicos (CRUD)
- Listar, buscar, crear, actualizar y eliminar técnicos
- Validación de email único

### 3. Gestión de Órdenes de Trabajo (CRUD Avanzado)
- Crear, actualizar, completar, cancelar y eliminar OTs
- Asignación de equipo y técnico
- Gestión de prioridades y estados

### 4. Historial de Mantenimiento
- Visualización de OTs completadas
- Filtros por equipo, técnico y rango de fechas

### 5. Reportes Especiales
- Equipos que nunca recibieron mantenimiento
- Top 2 equipos con más intervenciones
- Técnico con mayor costo acumulado en repuestos
- Órdenes atrasadas (más de 7 días sin completar)

## Reglas de Negocio

| Regla | Descripción |
|-------|-------------|
| **RN-01** | No se puede eliminar un equipo que tenga órdenes de trabajo asociadas |
| **RN-02** | Solo se pueden asignar técnicos registrados en el sistema |
| **RN-03** | Al completar una OT, el equipo cambia automáticamente a estado "operativo" |

## Datos de Ejemplo

El archivo `schema.sql` incluye:
- **15 equipos** industriales con diferentes tipos y estados
- **12 técnicos** con diversas especialidades
- **15 órdenes de trabajo** con variedad de estados, prioridades y costos

## Base de Datos

La base de datos SQLite incluye:
- **3 tablas**: `equipos`, `tecnicos`, `ordenes_trabajo`
- **5 índices** para optimizar consultas frecuentes
- **Restricciones CHECK** para validar estados y prioridades
- **Claves foráneas** con `ON DELETE RESTRICT` para integridad referencial
