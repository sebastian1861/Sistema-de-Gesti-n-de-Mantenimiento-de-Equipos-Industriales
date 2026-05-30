"""
Modelo CRUD avanzado para la gestión de órdenes de trabajo.

Implementa las operaciones CRUD con reglas de negocio:
- Validar que el técnico asignado esté registrado.
- Al completar una OT, cambiar estado del equipo a 'operativo'.
- Control de transiciones de estado válidas.
"""

import sqlite3
from datetime import date
from database import Database

db = Database()


def crear_orden(fecha_solicitud, descripcion_falla, prioridad, equipo_codigo, tecnico_documento):
    """
    Crea una nueva orden de trabajo.

    Reglas de negocio:
    - El técnico debe estar registrado en el sistema.
    - El equipo debe existir.
    - Al crear la OT, el equipo cambia a estado 'en mantenimiento'.

    Args:
        fecha_solicitud: Fecha de solicitud (YYYY-MM-DD).
        descripcion_falla: Descripción de la falla reportada.
        prioridad: Prioridad de la OT ('alta', 'media', 'baja').
        equipo_codigo: Código del equipo asociado.
        tecnico_documento: Documento del técnico asignado.

    Returns:
        ID de la orden creada o None si hubo error.
    """
    # Validar prioridad
    prioridades_validas = ("alta", "media", "baja")
    if prioridad not in prioridades_validas:
        print(f"  ✗ Prioridad inválida. Debe ser una de: {', '.join(prioridades_validas)}")
        return None

    # Validar que el equipo exista
    equipo = db.fetchone("SELECT * FROM equipos WHERE codigo = ?", (equipo_codigo,))
    if not equipo:
        print(f"  ✗ No existe el equipo con código '{equipo_codigo}'.")
        return None

    # Regla de negocio: Validar que el técnico esté registrado
    tecnico = db.fetchone("SELECT * FROM tecnicos WHERE documento = ?", (tecnico_documento,))
    if not tecnico:
        print(f"  ✗ No se puede asignar: El técnico con documento '{tecnico_documento}' no está registrado.")
        return None

    try:
        cursor = db.ejecutar(
            """INSERT INTO ordenes_trabajo
               (fecha_solicitud, descripcion_falla, prioridad, equipo_codigo, tecnico_documento, estado)
               VALUES (?, ?, ?, ?, ?, 'pendiente')""",
            (fecha_solicitud, descripcion_falla, prioridad, equipo_codigo, tecnico_documento)
        )

        # Cambiar estado del equipo a 'en mantenimiento'
        db.ejecutar(
            "UPDATE equipos SET estado = 'en mantenimiento' WHERE codigo = ?",
            (equipo_codigo,)
        )

        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        print(f"  ✗ Error de integridad: {e}")
        return None


def obtener_ordenes():
    """
    Retorna todas las órdenes de trabajo con información del equipo y técnico.

    Returns:
        Lista de registros con JOIN a equipos y técnicos.
    """
    return db.fetchall(
        """SELECT ot.*, e.nombre as equipo_nombre, t.nombre as tecnico_nombre
           FROM ordenes_trabajo ot
           JOIN equipos e ON ot.equipo_codigo = e.codigo
           JOIN tecnicos t ON ot.tecnico_documento = t.documento
           ORDER BY ot.id DESC"""
    )


def obtener_orden(id_orden):
    """
    Busca una orden de trabajo por su ID con detalles completos.

    Args:
        id_orden: ID de la orden de trabajo.

    Returns:
        Registro de la orden (sqlite3.Row) o None si no existe.
    """
    return db.fetchone(
        """SELECT ot.*, e.nombre as equipo_nombre, e.tipo as equipo_tipo,
                  e.ubicacion as equipo_ubicacion,
                  t.nombre as tecnico_nombre, t.especialidad as tecnico_especialidad
           FROM ordenes_trabajo ot
           JOIN equipos e ON ot.equipo_codigo = e.codigo
           JOIN tecnicos t ON ot.tecnico_documento = t.documento
           WHERE ot.id = ?""",
        (id_orden,)
    )


def actualizar_orden(id_orden, **campos):
    """
    Actualiza campos de una orden de trabajo existente.

    Args:
        id_orden: ID de la orden a actualizar.
        **campos: Campos a actualizar.

    Returns:
        True si se actualizó, False en caso contrario.
    """
    campos_permitidos = {
        "descripcion_falla", "prioridad", "tecnico_documento",
        "fecha_ejecucion", "costo_repuestos", "solucion_aplicada"
    }
    campos_filtrados = {k: v for k, v in campos.items() if k in campos_permitidos and v is not None}

    if not campos_filtrados:
        print("  ✗ No se proporcionaron campos válidos para actualizar.")
        return False

    # Validar prioridad si se incluye
    if "prioridad" in campos_filtrados:
        prioridades_validas = ("alta", "media", "baja")
        if campos_filtrados["prioridad"] not in prioridades_validas:
            print(f"  ✗ Prioridad inválida. Debe ser una de: {', '.join(prioridades_validas)}")
            return False

    # Validar técnico si se incluye
    if "tecnico_documento" in campos_filtrados:
        tecnico = db.fetchone(
            "SELECT * FROM tecnicos WHERE documento = ?",
            (campos_filtrados["tecnico_documento"],)
        )
        if not tecnico:
            print("  ✗ El técnico especificado no está registrado.")
            return False

    set_clause = ", ".join(f"{k} = ?" for k in campos_filtrados)
    valores = list(campos_filtrados.values()) + [id_orden]

    cursor = db.ejecutar(f"UPDATE ordenes_trabajo SET {set_clause} WHERE id = ?", tuple(valores))
    if cursor.rowcount == 0:
        print(f"  ✗ No se encontró la orden de trabajo con ID {id_orden}.")
        return False
    return True


def completar_orden(id_orden, solucion_aplicada, costo_repuestos):
    """
    Completa una orden de trabajo.

    Regla de negocio:
    - Cambia el estado de la OT a 'completada'.
    - Establece la fecha de ejecución al día actual.
    - Cambia el estado del equipo asociado a 'operativo'.

    Args:
        id_orden: ID de la orden a completar.
        solucion_aplicada: Descripción de la solución aplicada.
        costo_repuestos: Costo de los repuestos utilizados.

    Returns:
        True si se completó correctamente, False en caso contrario.
    """
    # Obtener la orden actual
    orden = db.fetchone("SELECT * FROM ordenes_trabajo WHERE id = ?", (id_orden,))
    if not orden:
        print(f"  ✗ No se encontró la orden de trabajo con ID {id_orden}.")
        return False

    if orden["estado"] == "completada":
        print("  ✗ La orden ya está completada.")
        return False

    if orden["estado"] == "cancelada":
        print("  ✗ No se puede completar una orden cancelada.")
        return False

    fecha_hoy = date.today().isoformat()

    # Actualizar la orden de trabajo
    db.ejecutar(
        """UPDATE ordenes_trabajo
           SET estado = 'completada',
               fecha_ejecucion = ?,
               solucion_aplicada = ?,
               costo_repuestos = ?
           WHERE id = ?""",
        (fecha_hoy, solucion_aplicada, costo_repuestos, id_orden)
    )

    # Regla de negocio: Cambiar estado del equipo a 'operativo'
    db.ejecutar(
        "UPDATE equipos SET estado = 'operativo' WHERE codigo = ?",
        (orden["equipo_codigo"],)
    )

    return True


def cambiar_estado_orden(id_orden, nuevo_estado):
    """
    Cambia el estado de una orden de trabajo.

    Args:
        id_orden: ID de la orden.
        nuevo_estado: Nuevo estado ('pendiente', 'en proceso', 'completada', 'cancelada').

    Returns:
        True si se cambió el estado, False en caso contrario.
    """
    estados_validos = ("pendiente", "en proceso", "completada", "cancelada")
    if nuevo_estado not in estados_validos:
        print(f"  ✗ Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
        return False

    orden = db.fetchone("SELECT * FROM ordenes_trabajo WHERE id = ?", (id_orden,))
    if not orden:
        print(f"  ✗ No se encontró la orden de trabajo con ID {id_orden}.")
        return False

    if orden["estado"] == "completada" and nuevo_estado != "completada":
        print("  ✗ No se puede cambiar el estado de una orden completada.")
        return False

    db.ejecutar(
        "UPDATE ordenes_trabajo SET estado = ? WHERE id = ?",
        (nuevo_estado, id_orden)
    )
    return True


def cancelar_orden(id_orden):
    """
    Cancela una orden de trabajo.

    Args:
        id_orden: ID de la orden a cancelar.

    Returns:
        True si se canceló, False en caso contrario.
    """
    orden = db.fetchone("SELECT * FROM ordenes_trabajo WHERE id = ?", (id_orden,))
    if not orden:
        print(f"  ✗ No se encontró la orden de trabajo con ID {id_orden}.")
        return False

    if orden["estado"] == "completada":
        print("  ✗ No se puede cancelar una orden completada.")
        return False

    if orden["estado"] == "cancelada":
        print("  ✗ La orden ya está cancelada.")
        return False

    db.ejecutar(
        "UPDATE ordenes_trabajo SET estado = 'cancelada' WHERE id = ?",
        (id_orden,)
    )
    return True


def eliminar_orden(id_orden):
    """
    Elimina una orden de trabajo.
    Solo se permite eliminar OTs con estado 'pendiente' o 'cancelada'.

    Args:
        id_orden: ID de la orden a eliminar.

    Returns:
        True si se eliminó, False en caso contrario.
    """
    orden = db.fetchone("SELECT * FROM ordenes_trabajo WHERE id = ?", (id_orden,))
    if not orden:
        print(f"  ✗ No se encontró la orden de trabajo con ID {id_orden}.")
        return False

    if orden["estado"] not in ("pendiente", "cancelada"):
        print(f"  ✗ Solo se pueden eliminar órdenes con estado 'pendiente' o 'cancelada'. Estado actual: '{orden['estado']}'.")
        return False

    db.ejecutar("DELETE FROM ordenes_trabajo WHERE id = ?", (id_orden,))
    return True
