"""
Modelo CRUD para la gestión de técnicos.

Implementa las operaciones de crear, leer, actualizar y eliminar técnicos,
incluyendo validaciones de integridad referencial.
"""

import sqlite3
from database import Database

db = Database()


def crear_tecnico(documento, nombre, especialidad, telefono, email):
    """
    Crea un nuevo técnico en la base de datos.

    Args:
        documento: Documento de identidad del técnico (PK).
        nombre: Nombre completo del técnico.
        especialidad: Área de especialización.
        telefono: Número de teléfono.
        email: Correo electrónico (debe ser único).

    Returns:
        True si se creó correctamente, False en caso de error.
    """
    try:
        db.ejecutar(
            """INSERT INTO tecnicos (documento, nombre, especialidad, telefono, email)
               VALUES (?, ?, ?, ?, ?)""",
            (documento, nombre, especialidad, telefono, email)
        )
        return True
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e).upper():
            print(f"  ✗ Error: Ya existe un técnico con el email '{email}'.")
        else:
            print(f"  ✗ Error: Ya existe un técnico con el documento '{documento}'.")
        return False


def obtener_tecnicos():
    """
    Retorna todos los técnicos registrados.

    Returns:
        Lista de registros de técnicos (sqlite3.Row).
    """
    return db.fetchall("SELECT * FROM tecnicos ORDER BY nombre")


def obtener_tecnico(documento):
    """
    Busca un técnico por su documento.

    Args:
        documento: Documento de identidad del técnico.

    Returns:
        Registro del técnico (sqlite3.Row) o None si no existe.
    """
    return db.fetchone("SELECT * FROM tecnicos WHERE documento = ?", (documento,))


def actualizar_tecnico(documento, **campos):
    """
    Actualiza los campos de un técnico existente.

    Args:
        documento: Documento del técnico a actualizar.
        **campos: Campos a actualizar (nombre, especialidad, telefono, email).

    Returns:
        True si se actualizó, False si no se encontró el técnico.
    """
    campos_permitidos = {"nombre", "especialidad", "telefono", "email"}
    campos_filtrados = {k: v for k, v in campos.items() if k in campos_permitidos and v is not None}

    if not campos_filtrados:
        print("  ✗ No se proporcionaron campos válidos para actualizar.")
        return False

    set_clause = ", ".join(f"{k} = ?" for k in campos_filtrados)
    valores = list(campos_filtrados.values()) + [documento]

    try:
        cursor = db.ejecutar(f"UPDATE tecnicos SET {set_clause} WHERE documento = ?", tuple(valores))
        if cursor.rowcount == 0:
            print(f"  ✗ No se encontró el técnico con documento '{documento}'.")
            return False
        return True
    except sqlite3.IntegrityError:
        print("  ✗ Error: El email proporcionado ya está en uso por otro técnico.")
        return False


def eliminar_tecnico(documento):
    """
    Elimina un técnico de la base de datos.

    Verifica que el técnico no tenga órdenes de trabajo activas
    (pendientes o en proceso) antes de eliminar.

    Args:
        documento: Documento del técnico a eliminar.

    Returns:
        True si se eliminó, False si no se puede eliminar o no existe.
    """
    # Verificar que no tenga OTs activas
    ots = db.fetchone(
        """SELECT COUNT(*) as total FROM ordenes_trabajo
           WHERE tecnico_documento = ? AND estado IN ('pendiente', 'en proceso')""",
        (documento,)
    )
    if ots and ots["total"] > 0:
        print(f"  ✗ No se puede eliminar: El técnico tiene {ots['total']} orden(es) de trabajo activa(s).")
        return False

    try:
        cursor = db.ejecutar("DELETE FROM tecnicos WHERE documento = ?", (documento,))
        if cursor.rowcount == 0:
            print(f"  ✗ No se encontró el técnico con documento '{documento}'.")
            return False
        return True
    except sqlite3.IntegrityError:
        print("  ✗ No se puede eliminar: El técnico tiene órdenes de trabajo asociadas.")
        return False
