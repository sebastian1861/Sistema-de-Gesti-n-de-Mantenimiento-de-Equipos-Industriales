"""
Reportes y consultas especiales.

Implementa los reportes avanzados del sistema:
- Equipos sin mantenimiento
- Top 2 equipos con más intervenciones
- Técnico con mayor costo acumulado en repuestos
- Órdenes atrasadas (más de 7 días sin completar)
"""

from database import Database

db = Database()


def equipos_sin_mantenimiento():
    """
    Consulta los equipos que nunca han recibido mantenimiento.

    Utiliza un LEFT JOIN para encontrar equipos sin OTs completadas.

    Returns:
        Lista de equipos sin mantenimiento registrado.
    """
    return db.fetchall(
        """SELECT e.codigo, e.nombre, e.tipo, e.ubicacion,
                  e.fecha_instalacion, e.estado
           FROM equipos e
           LEFT JOIN ordenes_trabajo ot
               ON e.codigo = ot.equipo_codigo AND ot.estado = 'completada'
           WHERE ot.id IS NULL
           ORDER BY e.codigo"""
    )


def top_equipos_intervenidos(n=2):
    """
    Consulta los N equipos con más intervenciones (OTs completadas).

    Args:
        n: Número de equipos a retornar (por defecto 2).

    Returns:
        Lista de equipos con su conteo de intervenciones.
    """
    return db.fetchall(
        """SELECT e.codigo, e.nombre, e.tipo, e.ubicacion,
                  COUNT(ot.id) as total_intervenciones
           FROM equipos e
           JOIN ordenes_trabajo ot ON e.codigo = ot.equipo_codigo
           WHERE ot.estado = 'completada'
           GROUP BY e.codigo, e.nombre, e.tipo, e.ubicacion
           ORDER BY total_intervenciones DESC
           LIMIT ?""",
        (n,)
    )


def tecnico_mayor_costo():
    """
    Consulta el técnico con mayor costo acumulado en repuestos.

    Suma el costo de repuestos de todas las OTs completadas
    agrupadas por técnico.

    Returns:
        Registro del técnico con mayor costo acumulado, o None.
    """
    return db.fetchone(
        """SELECT t.documento, t.nombre, t.especialidad,
                  SUM(ot.costo_repuestos) as costo_total,
                  COUNT(ot.id) as total_ordenes
           FROM tecnicos t
           JOIN ordenes_trabajo ot ON t.documento = ot.tecnico_documento
           WHERE ot.estado = 'completada'
           GROUP BY t.documento, t.nombre, t.especialidad
           ORDER BY costo_total DESC
           LIMIT 1"""
    )


def ordenes_atrasadas():
    """
    Consulta las órdenes de trabajo atrasadas.

    Una OT se considera atrasada si lleva más de 7 días desde
    su fecha de solicitud sin haber sido completada (estado
    'pendiente' o 'en proceso').

    Returns:
        Lista de OTs atrasadas con detalles del equipo y técnico.
    """
    return db.fetchall(
        """SELECT ot.id, ot.fecha_solicitud, ot.descripcion_falla,
                  ot.prioridad, ot.estado,
                  CAST(julianday('now') - julianday(ot.fecha_solicitud) AS INTEGER) as dias_transcurridos,
                  e.codigo as equipo_codigo, e.nombre as equipo_nombre,
                  t.nombre as tecnico_nombre
           FROM ordenes_trabajo ot
           JOIN equipos e ON ot.equipo_codigo = e.codigo
           JOIN tecnicos t ON ot.tecnico_documento = t.documento
           WHERE ot.estado IN ('pendiente', 'en proceso')
             AND julianday('now') - julianday(ot.fecha_solicitud) > 7
           ORDER BY dias_transcurridos DESC"""
    )
