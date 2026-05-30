"""
Historial de mantenimiento (solo lectura con filtros).

Muestra las órdenes de trabajo completadas con detalles
del equipo y técnico asociados, con capacidad de filtrado.
"""

from database import Database

db = Database()


def ver_historial(filtro_equipo=None, filtro_tecnico=None,
                  filtro_fecha_inicio=None, filtro_fecha_fin=None):
    """
    Consulta el historial de mantenimiento (OTs completadas).

    Args:
        filtro_equipo: Código del equipo para filtrar (opcional).
        filtro_tecnico: Documento del técnico para filtrar (opcional).
        filtro_fecha_inicio: Fecha mínima de ejecución YYYY-MM-DD (opcional).
        filtro_fecha_fin: Fecha máxima de ejecución YYYY-MM-DD (opcional).

    Returns:
        Lista de registros del historial con JOIN a equipos y técnicos.
    """
    query = """
        SELECT ot.id,
               ot.fecha_solicitud,
               ot.fecha_ejecucion,
               ot.descripcion_falla,
               ot.prioridad,
               ot.solucion_aplicada,
               ot.costo_repuestos,
               e.codigo as equipo_codigo,
               e.nombre as equipo_nombre,
               e.tipo as equipo_tipo,
               e.ubicacion as equipo_ubicacion,
               t.documento as tecnico_documento,
               t.nombre as tecnico_nombre,
               t.especialidad as tecnico_especialidad
        FROM ordenes_trabajo ot
        JOIN equipos e ON ot.equipo_codigo = e.codigo
        JOIN tecnicos t ON ot.tecnico_documento = t.documento
        WHERE ot.estado = 'completada'
    """
    params = []

    if filtro_equipo:
        query += " AND ot.equipo_codigo = ?"
        params.append(filtro_equipo)

    if filtro_tecnico:
        query += " AND ot.tecnico_documento = ?"
        params.append(filtro_tecnico)

    if filtro_fecha_inicio:
        query += " AND ot.fecha_ejecucion >= ?"
        params.append(filtro_fecha_inicio)

    if filtro_fecha_fin:
        query += " AND ot.fecha_ejecucion <= ?"
        params.append(filtro_fecha_fin)

    query += " ORDER BY ot.fecha_ejecucion DESC"

    return db.fetchall(query, tuple(params) if params else None)
