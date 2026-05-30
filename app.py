"""
Sistema de Gestión de Mantenimiento de Equipos — Aplicación Web (Flask).

Servidor web que expone la funcionalidad del sistema de mantenimiento
a través de una interfaz web moderna y visualmente atractiva.
"""

import sys
import os

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import date
from database import Database
from models import equipo, tecnico, orden_trabajo
from reports import historial, reportes

app = Flask(__name__)
app.secret_key = "mantenimiento_secret_key_2026"

# Inicializar base de datos al arrancar
db = Database()
db.inicializar()


# ════════════════════════════════════════════════════════════════
# PÁGINA PRINCIPAL (DASHBOARD)
# ════════════════════════════════════════════════════════════════

@app.route("/")
def dashboard():
    """Dashboard principal con estadísticas y resumen."""
    # Contar registros
    total_equipos = db.fetchone("SELECT COUNT(*) as c FROM equipos")["c"]
    total_tecnicos = db.fetchone("SELECT COUNT(*) as c FROM tecnicos")["c"]
    total_ots = db.fetchone("SELECT COUNT(*) as c FROM ordenes_trabajo")["c"]
    ots_pendientes = db.fetchone(
        "SELECT COUNT(*) as c FROM ordenes_trabajo WHERE estado IN ('pendiente', 'en proceso')"
    )["c"]
    ots_completadas = db.fetchone(
        "SELECT COUNT(*) as c FROM ordenes_trabajo WHERE estado = 'completada'"
    )["c"]

    # Órdenes atrasadas
    atrasadas = reportes.ordenes_atrasadas()

    # Últimas OTs
    ultimas_ots = db.fetchall(
        """SELECT ot.id, ot.fecha_solicitud, ot.prioridad, ot.estado,
                  e.nombre as equipo_nombre, t.nombre as tecnico_nombre
           FROM ordenes_trabajo ot
           JOIN equipos e ON ot.equipo_codigo = e.codigo
           JOIN tecnicos t ON ot.tecnico_documento = t.documento
           ORDER BY ot.id DESC LIMIT 5"""
    )

    return render_template("dashboard.html",
                           total_equipos=total_equipos,
                           total_tecnicos=total_tecnicos,
                           total_ots=total_ots,
                           ots_pendientes=ots_pendientes,
                           ots_completadas=ots_completadas,
                           atrasadas=atrasadas,
                           ultimas_ots=ultimas_ots)


# ════════════════════════════════════════════════════════════════
# EQUIPOS
# ════════════════════════════════════════════════════════════════

@app.route("/equipos")
def lista_equipos():
    """Lista todos los equipos."""
    equipos = equipo.obtener_equipos()
    return render_template("equipos/lista.html", equipos=equipos)


@app.route("/equipos/crear", methods=["GET", "POST"])
def crear_equipo_view():
    """Formulario para crear un nuevo equipo."""
    if request.method == "POST":
        codigo = request.form.get("codigo", "").strip().upper()
        nombre = request.form.get("nombre", "").strip()
        tipo = request.form.get("tipo", "").strip()
        ubicacion = request.form.get("ubicacion", "").strip()
        fecha_instalacion = request.form.get("fecha_instalacion", "").strip()
        estado = request.form.get("estado", "operativo").strip()

        if not all([codigo, nombre, tipo, ubicacion, fecha_instalacion]):
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("crear_equipo_view"))

        try:
            if equipo.crear_equipo(codigo, nombre, tipo, ubicacion, fecha_instalacion, estado):
                flash(f"Equipo '{codigo}' creado exitosamente.", "success")
                return redirect(url_for("lista_equipos"))
            else:
                flash(f"Error: Ya existe un equipo con el código '{codigo}'.", "error")
        except ValueError as e:
            flash(str(e), "error")

    return render_template("equipos/crear.html")


@app.route("/equipos/editar/<codigo>", methods=["GET", "POST"])
def editar_equipo_view(codigo):
    """Formulario para editar un equipo existente."""
    eq = equipo.obtener_equipo(codigo)
    if not eq:
        flash(f"No se encontró el equipo '{codigo}'.", "error")
        return redirect(url_for("lista_equipos"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip() or None
        tipo = request.form.get("tipo", "").strip() or None
        ubicacion = request.form.get("ubicacion", "").strip() or None
        fecha_instalacion = request.form.get("fecha_instalacion", "").strip() or None
        estado = request.form.get("estado", "").strip() or None

        try:
            if equipo.actualizar_equipo(codigo, nombre=nombre, tipo=tipo,
                                         ubicacion=ubicacion, fecha_instalacion=fecha_instalacion,
                                         estado=estado):
                flash("Equipo actualizado exitosamente.", "success")
                return redirect(url_for("lista_equipos"))
        except ValueError as e:
            flash(str(e), "error")

    return render_template("equipos/editar.html", equipo=eq)


@app.route("/equipos/eliminar/<codigo>", methods=["POST"])
def eliminar_equipo_view(codigo):
    """Elimina un equipo."""
    if equipo.eliminar_equipo(codigo):
        flash(f"Equipo '{codigo}' eliminado exitosamente.", "success")
    return redirect(url_for("lista_equipos"))


# ════════════════════════════════════════════════════════════════
# TÉCNICOS
# ════════════════════════════════════════════════════════════════

@app.route("/tecnicos")
def lista_tecnicos():
    """Lista todos los técnicos."""
    tecnicos = tecnico.obtener_tecnicos()
    return render_template("tecnicos/lista.html", tecnicos=tecnicos)


@app.route("/tecnicos/crear", methods=["GET", "POST"])
def crear_tecnico_view():
    """Formulario para crear un nuevo técnico."""
    if request.method == "POST":
        documento = request.form.get("documento", "").strip()
        nombre = request.form.get("nombre", "").strip()
        especialidad = request.form.get("especialidad", "").strip()
        telefono = request.form.get("telefono", "").strip()
        email = request.form.get("email", "").strip()

        if not all([documento, nombre, especialidad, telefono, email]):
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("crear_tecnico_view"))

        if tecnico.crear_tecnico(documento, nombre, especialidad, telefono, email):
            flash(f"Técnico '{nombre}' creado exitosamente.", "success")
            return redirect(url_for("lista_tecnicos"))
        else:
            flash("Error al crear el técnico. Verifique que el documento y email sean únicos.", "error")

    return render_template("tecnicos/crear.html")


@app.route("/tecnicos/editar/<documento>", methods=["GET", "POST"])
def editar_tecnico_view(documento):
    """Formulario para editar un técnico existente."""
    tec = tecnico.obtener_tecnico(documento)
    if not tec:
        flash(f"No se encontró el técnico con documento '{documento}'.", "error")
        return redirect(url_for("lista_tecnicos"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip() or None
        especialidad = request.form.get("especialidad", "").strip() or None
        telefono = request.form.get("telefono", "").strip() or None
        email = request.form.get("email", "").strip() or None

        if tecnico.actualizar_tecnico(documento, nombre=nombre, especialidad=especialidad,
                                       telefono=telefono, email=email):
            flash("Técnico actualizado exitosamente.", "success")
            return redirect(url_for("lista_tecnicos"))
        else:
            flash("Error al actualizar. Verifique que el email no esté en uso.", "error")

    return render_template("tecnicos/editar.html", tecnico=tec)


@app.route("/tecnicos/eliminar/<documento>", methods=["POST"])
def eliminar_tecnico_view(documento):
    """Elimina un técnico."""
    if tecnico.eliminar_tecnico(documento):
        flash("Técnico eliminado exitosamente.", "success")
    return redirect(url_for("lista_tecnicos"))


# ════════════════════════════════════════════════════════════════
# ÓRDENES DE TRABAJO
# ════════════════════════════════════════════════════════════════

@app.route("/ordenes")
def lista_ordenes():
    """Lista todas las órdenes de trabajo."""
    ordenes = orden_trabajo.obtener_ordenes()
    return render_template("ordenes/lista.html", ordenes=ordenes)


@app.route("/ordenes/ver/<int:id_orden>")
def ver_orden_view(id_orden):
    """Muestra el detalle de una orden de trabajo."""
    orden = orden_trabajo.obtener_orden(id_orden)
    if not orden:
        flash(f"No se encontró la orden #{id_orden}.", "error")
        return redirect(url_for("lista_ordenes"))
    return render_template("ordenes/detalle.html", orden=orden)


@app.route("/ordenes/crear", methods=["GET", "POST"])
def crear_orden_view():
    """Formulario para crear una nueva orden de trabajo."""
    equipos = equipo.obtener_equipos()
    tecnicos = tecnico.obtener_tecnicos()

    if request.method == "POST":
        fecha_solicitud = request.form.get("fecha_solicitud", "").strip() or date.today().isoformat()
        descripcion = request.form.get("descripcion_falla", "").strip()
        prioridad = request.form.get("prioridad", "").strip()
        equipo_codigo = request.form.get("equipo_codigo", "").strip()
        tecnico_documento = request.form.get("tecnico_documento", "").strip()

        if not all([descripcion, prioridad, equipo_codigo, tecnico_documento]):
            flash("Todos los campos son obligatorios.", "error")
            return redirect(url_for("crear_orden_view"))

        id_nueva = orden_trabajo.crear_orden(fecha_solicitud, descripcion, prioridad,
                                              equipo_codigo, tecnico_documento)
        if id_nueva:
            flash(f"Orden de trabajo #{id_nueva} creada exitosamente.", "success")
            return redirect(url_for("lista_ordenes"))
        else:
            flash("Error al crear la orden. Verifique los datos.", "error")

    return render_template("ordenes/crear.html", equipos=equipos, tecnicos=tecnicos,
                           fecha_hoy=date.today().isoformat())


@app.route("/ordenes/editar/<int:id_orden>", methods=["GET", "POST"])
def editar_orden_view(id_orden):
    """Formulario para editar una orden de trabajo."""
    orden = orden_trabajo.obtener_orden(id_orden)
    if not orden:
        flash(f"No se encontró la orden #{id_orden}.", "error")
        return redirect(url_for("lista_ordenes"))

    tecnicos = tecnico.obtener_tecnicos()

    if request.method == "POST":
        descripcion = request.form.get("descripcion_falla", "").strip() or None
        prioridad = request.form.get("prioridad", "").strip() or None
        tecnico_doc = request.form.get("tecnico_documento", "").strip() or None

        if orden_trabajo.actualizar_orden(id_orden, descripcion_falla=descripcion,
                                           prioridad=prioridad, tecnico_documento=tecnico_doc):
            flash("Orden actualizada exitosamente.", "success")
            return redirect(url_for("ver_orden_view", id_orden=id_orden))
        else:
            flash("Error al actualizar la orden.", "error")

    return render_template("ordenes/editar.html", orden=orden, tecnicos=tecnicos)


@app.route("/ordenes/completar/<int:id_orden>", methods=["GET", "POST"])
def completar_orden_view(id_orden):
    """Formulario para completar una orden de trabajo."""
    orden = orden_trabajo.obtener_orden(id_orden)
    if not orden:
        flash(f"No se encontró la orden #{id_orden}.", "error")
        return redirect(url_for("lista_ordenes"))

    if request.method == "POST":
        solucion = request.form.get("solucion_aplicada", "").strip()
        try:
            costo = float(request.form.get("costo_repuestos", "0").strip() or "0")
        except ValueError:
            flash("El costo debe ser un número válido.", "error")
            return redirect(url_for("completar_orden_view", id_orden=id_orden))

        if not solucion:
            flash("La solución aplicada es obligatoria.", "error")
            return redirect(url_for("completar_orden_view", id_orden=id_orden))

        if orden_trabajo.completar_orden(id_orden, solucion, costo):
            flash(f"Orden #{id_orden} completada. Equipo marcado como 'operativo'.", "success")
            return redirect(url_for("ver_orden_view", id_orden=id_orden))
        else:
            flash("Error al completar la orden.", "error")

    return render_template("ordenes/completar.html", orden=orden)


@app.route("/ordenes/cancelar/<int:id_orden>", methods=["POST"])
def cancelar_orden_view(id_orden):
    """Cancela una orden de trabajo."""
    if orden_trabajo.cancelar_orden(id_orden):
        flash(f"Orden #{id_orden} cancelada.", "success")
    return redirect(url_for("lista_ordenes"))


@app.route("/ordenes/cambiar_estado/<int:id_orden>", methods=["POST"])
def cambiar_estado_view(id_orden):
    """Cambia el estado de una orden."""
    nuevo_estado = request.form.get("estado", "").strip()
    if orden_trabajo.cambiar_estado_orden(id_orden, nuevo_estado):
        flash(f"Estado cambiado a '{nuevo_estado}'.", "success")
    return redirect(url_for("ver_orden_view", id_orden=id_orden))


@app.route("/ordenes/eliminar/<int:id_orden>", methods=["POST"])
def eliminar_orden_view(id_orden):
    """Elimina una orden de trabajo."""
    if orden_trabajo.eliminar_orden(id_orden):
        flash(f"Orden #{id_orden} eliminada.", "success")
    return redirect(url_for("lista_ordenes"))


# ════════════════════════════════════════════════════════════════
# HISTORIAL
# ════════════════════════════════════════════════════════════════

@app.route("/historial")
def historial_view():
    """Historial de mantenimiento con filtros."""
    filtro_equipo = request.args.get("equipo", "").strip() or None
    filtro_tecnico = request.args.get("tecnico", "").strip() or None
    filtro_fecha_inicio = request.args.get("fecha_inicio", "").strip() or None
    filtro_fecha_fin = request.args.get("fecha_fin", "").strip() or None

    registros = historial.ver_historial(
        filtro_equipo=filtro_equipo,
        filtro_tecnico=filtro_tecnico,
        filtro_fecha_inicio=filtro_fecha_inicio,
        filtro_fecha_fin=filtro_fecha_fin
    )

    equipos = equipo.obtener_equipos()
    tecnicos = tecnico.obtener_tecnicos()

    return render_template("historial.html", registros=registros,
                           equipos=equipos, tecnicos=tecnicos,
                           filtro_equipo=filtro_equipo,
                           filtro_tecnico=filtro_tecnico,
                           filtro_fecha_inicio=filtro_fecha_inicio,
                           filtro_fecha_fin=filtro_fecha_fin)


# ════════════════════════════════════════════════════════════════
# REPORTES
# ════════════════════════════════════════════════════════════════

@app.route("/reportes")
def reportes_view():
    """Página de reportes especiales."""
    sin_mant = reportes.equipos_sin_mantenimiento()
    top = reportes.top_equipos_intervenidos(2)
    tec_costo = reportes.tecnico_mayor_costo()
    atrasadas = reportes.ordenes_atrasadas()

    return render_template("reportes.html",
                           sin_mantenimiento=sin_mant,
                           top_equipos=top,
                           tecnico_costo=tec_costo,
                           ordenes_atrasadas=atrasadas)


# ════════════════════════════════════════════════════════════════
# INICIAR SERVIDOR
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n  === SISTEMA DE GESTION DE MANTENIMIENTO ===")
    print("  Interfaz Web -> http://localhost:5000")
    print("  ==========================================\n")
    app.run(debug=True, host="0.0.0.0", port=5000)

