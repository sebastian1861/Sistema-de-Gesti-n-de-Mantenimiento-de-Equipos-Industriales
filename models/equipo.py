"""
Modelo CRUD para la gestión de equipos.

Implementa las operaciones de crear, leer, actualizar y eliminar equipos,
incluyendo la regla de negocio de no eliminar equipos con OTs asociadas.
"""

import sqlite3
from database import Database

db = Database()


def crear_equipo(codigo, nombre, tipo, ubicacion, fecha_instalacion, estado="operativo"):
    """
    Crea un nuevo equipo en la base de datos.

    Args:
        codigo: Código único del equipo (ej: 'EQ-016').
        nombre: Nombre descriptivo del equipo.
        tipo: Tipo de equipo (ej: 'Compresor', 'Motor').
        ubicacion: Ubicación física del equipo.
        fecha_instalacion: Fecha de instalación (formato YYYY-MM-DD).
        estado: Estado del equipo ('operativo', 'en mantenimiento', 'fuera de servicio').

    Returns:
        True si se creó correctamente, False en caso de error.

    Raises:
        ValueError: Si el estado no es válido.
    """
    estados_validos = ("operativo", "en mantenimiento", "fuera de servicio")
    if estado not in estados_validos:
        raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")

    try:
        db.ejecutar(
            """INSERT INTO equipos (codigo, nombre, tipo, ubicacion, fecha_instalacion, estado)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (codigo, nombre, tipo, ubicacion, fecha_instalacion, estado)
        )
        return True
    except sqlite3.IntegrityError:
        print(f"  ✗ Error: Ya existe un equipo con el código '{codigo}'.")
        return False


def obtener_equipos():
    """
    Retorna todos los equipos registrados.

    Returns:
        Lista de registros de equipos (sqlite3.Row).
    """
    return db.fetchall("SELECT * FROM equipos ORDER BY codigo")


def obtener_equipo(codigo):
    """
    Busca un equipo por su código.

    Args:
        codigo: Código del equipo a buscar.

    Returns:
        Registro del equipo (sqlite3.Row) o None si no existe.
    """
    return db.fetchone("SELECT * FROM equipos WHERE codigo = ?", (codigo,))


def actualizar_equipo(codigo, **campos):
    """
    Actualiza los campos de un equipo existente.

    Args:
        codigo: Código del equipo a actualizar.
        **campos: Campos a actualizar (nombre, tipo, ubicacion, fecha_instalacion, estado).

    Returns:
        True si se actualizó, False si no se encontró el equipo.

    Raises:
        ValueError: Si el estado proporcionado no es válido.
    """
    if "estado" in campos:
        estados_validos = ("operativo", "en mantenimiento", "fuera de servicio")
        if campos["estado"] not in estados_validos:
            raise ValueError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")

    campos_permitidos = {"nombre", "tipo", "ubicacion", "fecha_instalacion", "estado"}
    campos_filtrados = {k: v for k, v in campos.items() if k in campos_permitidos and v is not None}

    if not campos_filtrados:
        print("  ✗ No se proporcionaron campos válidos para actualizar.")
        return False

    set_clause = ", ".join(f"{k} = ?" for k in campos_filtrados)
    valores = list(campos_filtrados.values()) + [codigo]

    cursor = db.ejecutar(f"UPDATE equipos SET {set_clause} WHERE codigo = ?", tuple(valores))
    if cursor.rowcount == 0:
        print(f"  ✗ No se encontró el equipo con código '{codigo}'.")
        return False
    return True


def eliminar_equipo(codigo):
    """
    Elimina un equipo de la base de datos.

    Regla de negocio: No se puede eliminar un equipo que tenga
    órdenes de trabajo asociadas.

    Args:
        codigo: Código del equipo a eliminar.

    Returns:
        True si se eliminó, False si no se puede eliminar o no existe.
    """
    # Verificar que no tenga órdenes de trabajo asociadas
    ots = db.fetchone(
        "SELECT COUNT(*) as total FROM ordenes_trabajo WHERE equipo_codigo = ?",
        (codigo,)
    )
    if ots and ots["total"] > 0:
        print(f"  ✗ No se puede eliminar: El equipo '{codigo}' tiene {ots['total']} orden(es) de trabajo asociada(s).")
        return False

    cursor = db.ejecutar("DELETE FROM equipos WHERE codigo = ?", (codigo,))
    if cursor.rowcount == 0:
        print(f"  ✗ No se encontró el equipo con código '{codigo}'.")
        return False
    return True
