"""
Menús interactivos de consola para el sistema de gestión de mantenimiento.

Contiene todos los submenús para gestionar equipos, técnicos,
órdenes de trabajo, historial y reportes.
"""

import sys
import os

# Agregar el directorio raíz al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import date
from models import equipo, tecnico, orden_trabajo
from reports import historial, reportes
from views.tabla import (
    imprimir_tabla, imprimir_detalle, imprimir_titulo,
    limpiar_pantalla, pausar, confirmar
)


# ════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ════════════════════════════════════════════════════════════════

def menu_principal():
    """Muestra el menú principal del sistema y gestiona la navegación."""
    while True:
        limpiar_pantalla()
        imprimir_titulo("SISTEMA DE GESTIÓN DE MANTENIMIENTO")
        print("  1. Gestión de Equipos")
        print("  2. Gestión de Técnicos")
        print("  3. Gestión de Órdenes de Trabajo")
        print("  4. Historial de Mantenimiento")
        print("  5. Reportes y Consultas Especiales")
        print("  0. Salir")
        print()

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_tecnicos()
        elif opcion == "3":
            menu_ordenes()
        elif opcion == "4":
            menu_historial()
        elif opcion == "5":
            menu_reportes()
        elif opcion == "0":
            print("\n  ¡Hasta luego! Sistema cerrado.\n")
            break
        else:
            print("  ✗ Opción inválida.")
            pausar()


# ════════════════════════════════════════════════════════════════
# MENÚ DE EQUIPOS
# ════════════════════════════════════════════════════════════════

def menu_equipos():
    """Submenú de gestión de equipos (CRUD)."""
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE EQUIPOS")
        print("  1. Listar todos los equipos")
        print("  2. Buscar equipo por código")
        print("  3. Crear nuevo equipo")
        print("  4. Actualizar equipo")
        print("  5. Eliminar equipo")
        print("  0. Volver al menú principal")
        print()

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            listar_equipos()
        elif opcion == "2":
            buscar_equipo()
        elif opcion == "3":
            crear_equipo()
        elif opcion == "4":
            actualizar_equipo()
        elif opcion == "5":
            eliminar_equipo()
        elif opcion == "0":
            break
        else:
            print("  ✗ Opción inválida.")
            pausar()


def listar_equipos():
    """Muestra todos los equipos en formato de tabla."""
    limpiar_pantalla()
    imprimir_titulo("LISTADO DE EQUIPOS")
    equipos = equipo.obtener_equipos()
    headers = ["Código", "Nombre", "Tipo", "Ubicación", "F. Instalación", "Estado"]
    rows = [[e["codigo"], e["nombre"], e["tipo"], e["ubicacion"],
             e["fecha_instalacion"], e["estado"]] for e in equipos]
    imprimir_tabla(headers, rows)
    pausar()


def buscar_equipo():
    """Busca y muestra los detalles de un equipo por código."""
    limpiar_pantalla()
    imprimir_titulo("BUSCAR EQUIPO")
    codigo = input("  Ingrese el código del equipo: ").strip().upper()
    e = equipo.obtener_equipo(codigo)
    if e:
        imprimir_detalle([
            ("Código", e["codigo"]),
            ("Nombre", e["nombre"]),
            ("Tipo", e["tipo"]),
            ("Ubicación", e["ubicacion"]),
            ("Fecha Instalación", e["fecha_instalacion"]),
            ("Estado", e["estado"]),
        ])
    else:
        print(f"\n  ✗ No se encontró el equipo con código '{codigo}'.")
    pausar()


def crear_equipo():
    """Formulario para crear un nuevo equipo."""
    limpiar_pantalla()
    imprimir_titulo("CREAR NUEVO EQUIPO")
    print()
    codigo = input("  Código (ej: EQ-016): ").strip().upper()
    nombre = input("  Nombre: ").strip()
    tipo = input("  Tipo: ").strip()
    ubicacion = input("  Ubicación: ").strip()
    fecha = input("  Fecha de instalación (YYYY-MM-DD): ").strip()
    print("  Estados: operativo | en mantenimiento | fuera de servicio")
    estado = input("  Estado [operativo]: ").strip().lower() or "operativo"

    if not all([codigo, nombre, tipo, ubicacion, fecha]):
        print("\n  ✗ Todos los campos son obligatorios.")
        pausar()
        return

    try:
        if equipo.crear_equipo(codigo, nombre, tipo, ubicacion, fecha, estado):
            print("\n  ✓ Equipo creado exitosamente.")
    except ValueError as e:
        print(f"\n  ✗ Error: {e}")
    pausar()


def actualizar_equipo():
    """Formulario para actualizar un equipo existente."""
    limpiar_pantalla()
    imprimir_titulo("ACTUALIZAR EQUIPO")
    codigo = input("  Ingrese el código del equipo a actualizar: ").strip().upper()

    e = equipo.obtener_equipo(codigo)
    if not e:
        print(f"\n  ✗ No se encontró el equipo con código '{codigo}'.")
        pausar()
        return

    print(f"\n  Equipo actual: {e['nombre']} ({e['codigo']})")
    print("  (Deje en blanco para mantener el valor actual)\n")

    nombre = input(f"  Nombre [{e['nombre']}]: ").strip() or None
    tipo = input(f"  Tipo [{e['tipo']}]: ").strip() or None
    ubicacion = input(f"  Ubicación [{e['ubicacion']}]: ").strip() or None
    fecha = input(f"  Fecha instalación [{e['fecha_instalacion']}]: ").strip() or None
    print(f"  Estados: operativo | en mantenimiento | fuera de servicio")
    estado = input(f"  Estado [{e['estado']}]: ").strip().lower() or None

    try:
        if equipo.actualizar_equipo(codigo, nombre=nombre, tipo=tipo,
                                     ubicacion=ubicacion, fecha_instalacion=fecha,
                                     estado=estado):
            print("\n  ✓ Equipo actualizado exitosamente.")
    except ValueError as err:
        print(f"\n  ✗ Error: {err}")
    pausar()


def eliminar_equipo():
    """Formulario para eliminar un equipo."""
    limpiar_pantalla()
    imprimir_titulo("ELIMINAR EQUIPO")
    codigo = input("  Ingrese el código del equipo a eliminar: ").strip().upper()

    e = equipo.obtener_equipo(codigo)
    if not e:
        print(f"\n  ✗ No se encontró el equipo con código '{codigo}'.")
        pausar()
        return

    print(f"\n  Equipo: {e['nombre']} ({e['codigo']}) - Estado: {e['estado']}")
    if confirmar("¿Está seguro de que desea eliminar este equipo?"):
        if equipo.eliminar_equipo(codigo):
            print("\n  ✓ Equipo eliminado exitosamente.")
    else:
        print("\n  Operación cancelada.")
    pausar()


# ════════════════════════════════════════════════════════════════
# MENÚ DE TÉCNICOS
# ════════════════════════════════════════════════════════════════

def menu_tecnicos():
    """Submenú de gestión de técnicos (CRUD)."""
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE TÉCNICOS")
        print("  1. Listar todos los técnicos")
        print("  2. Buscar técnico por documento")
        print("  3. Crear nuevo técnico")
        print("  4. Actualizar técnico")
        print("  5. Eliminar técnico")
        print("  0. Volver al menú principal")
        print()

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            listar_tecnicos()
        elif opcion == "2":
            buscar_tecnico()
        elif opcion == "3":
            crear_tecnico()
        elif opcion == "4":
            actualizar_tecnico()
        elif opcion == "5":
            eliminar_tecnico()
        elif opcion == "0":
            break
        else:
            print("  ✗ Opción inválida.")
            pausar()


def listar_tecnicos():
    """Muestra todos los técnicos en formato de tabla."""
    limpiar_pantalla()
    imprimir_titulo("LISTADO DE TÉCNICOS")
    tecnicos = tecnico.obtener_tecnicos()
    headers = ["Documento", "Nombre", "Especialidad", "Teléfono", "Email"]
    rows = [[t["documento"], t["nombre"], t["especialidad"],
             t["telefono"], t["email"]] for t in tecnicos]
    imprimir_tabla(headers, rows)
    pausar()


def buscar_tecnico():
    """Busca y muestra los detalles de un técnico por documento."""
    limpiar_pantalla()
    imprimir_titulo("BUSCAR TÉCNICO")
    documento = input("  Ingrese el documento del técnico: ").strip()
    t = tecnico.obtener_tecnico(documento)
    if t:
        imprimir_detalle([
            ("Documento", t["documento"]),
            ("Nombre", t["nombre"]),
            ("Especialidad", t["especialidad"]),
            ("Teléfono", t["telefono"]),
            ("Email", t["email"]),
        ])
    else:
        print(f"\n  ✗ No se encontró el técnico con documento '{documento}'.")
    pausar()


def crear_tecnico():
    """Formulario para crear un nuevo técnico."""
    limpiar_pantalla()
    imprimir_titulo("CREAR NUEVO TÉCNICO")
    print()
    documento = input("  Documento de identidad: ").strip()
    nombre = input("  Nombre completo: ").strip()
    especialidad = input("  Especialidad: ").strip()
    telefono = input("  Teléfono: ").strip()
    email = input("  Email: ").strip()

    if not all([documento, nombre, especialidad, telefono, email]):
        print("\n  ✗ Todos los campos son obligatorios.")
        pausar()
        return

    if tecnico.crear_tecnico(documento, nombre, especialidad, telefono, email):
        print("\n  ✓ Técnico creado exitosamente.")
    pausar()


def actualizar_tecnico():
    """Formulario para actualizar un técnico existente."""
    limpiar_pantalla()
    imprimir_titulo("ACTUALIZAR TÉCNICO")
    documento = input("  Ingrese el documento del técnico a actualizar: ").strip()

    t = tecnico.obtener_tecnico(documento)
    if not t:
        print(f"\n  ✗ No se encontró el técnico con documento '{documento}'.")
        pausar()
        return

    print(f"\n  Técnico actual: {t['nombre']}")
    print("  (Deje en blanco para mantener el valor actual)\n")

    nombre = input(f"  Nombre [{t['nombre']}]: ").strip() or None
    especialidad = input(f"  Especialidad [{t['especialidad']}]: ").strip() or None
    telefono = input(f"  Teléfono [{t['telefono']}]: ").strip() or None
    email = input(f"  Email [{t['email']}]: ").strip() or None

    if tecnico.actualizar_tecnico(documento, nombre=nombre, especialidad=especialidad,
                                   telefono=telefono, email=email):
        print("\n  ✓ Técnico actualizado exitosamente.")
    pausar()


def eliminar_tecnico():
    """Formulario para eliminar un técnico."""
    limpiar_pantalla()
    imprimir_titulo("ELIMINAR TÉCNICO")
    documento = input("  Ingrese el documento del técnico a eliminar: ").strip()

    t = tecnico.obtener_tecnico(documento)
    if not t:
        print(f"\n  ✗ No se encontró el técnico con documento '{documento}'.")
        pausar()
        return

    print(f"\n  Técnico: {t['nombre']} - Especialidad: {t['especialidad']}")
    if confirmar("¿Está seguro de que desea eliminar este técnico?"):
        if tecnico.eliminar_tecnico(documento):
            print("\n  ✓ Técnico eliminado exitosamente.")
    else:
        print("\n  Operación cancelada.")
    pausar()


# ════════════════════════════════════════════════════════════════
# MENÚ DE ÓRDENES DE TRABAJO
# ════════════════════════════════════════════════════════════════

def menu_ordenes():
    """Submenú de gestión de órdenes de trabajo (CRUD avanzado)."""
    while True:
        limpiar_pantalla()
        imprimir_titulo("GESTIÓN DE ÓRDENES DE TRABAJO")
        print("  1. Listar todas las órdenes")
        print("  2. Ver detalle de una orden")
        print("  3. Crear nueva orden de trabajo")
        print("  4. Actualizar orden de trabajo")
        print("  5. Completar orden de trabajo")
        print("  6. Cancelar orden de trabajo")
        print("  7. Cambiar estado de una orden")
        print("  8. Eliminar orden de trabajo")
        print("  0. Volver al menú principal")
        print()

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            listar_ordenes()
        elif opcion == "2":
            ver_detalle_orden()
        elif opcion == "3":
            crear_orden()
        elif opcion == "4":
            actualizar_orden()
        elif opcion == "5":
            completar_orden()
        elif opcion == "6":
            cancelar_orden()
        elif opcion == "7":
            cambiar_estado_orden()
        elif opcion == "8":
            eliminar_orden()
        elif opcion == "0":
            break
        else:
            print("  ✗ Opción inválida.")
            pausar()


def listar_ordenes():
    """Muestra todas las órdenes de trabajo en formato de tabla."""
    limpiar_pantalla()
    imprimir_titulo("LISTADO DE ÓRDENES DE TRABAJO")
    ordenes = orden_trabajo.obtener_ordenes()
    headers = ["ID", "Fecha Sol.", "Equipo", "Técnico", "Prioridad", "Estado"]
    rows = [[o["id"], o["fecha_solicitud"], o["equipo_nombre"],
             o["tecnico_nombre"], o["prioridad"], o["estado"]] for o in ordenes]
    imprimir_tabla(headers, rows)
    pausar()


def ver_detalle_orden():
    """Muestra los detalles completos de una orden de trabajo."""
    limpiar_pantalla()
    imprimir_titulo("DETALLE DE ORDEN DE TRABAJO")
    try:
        id_orden = int(input("  Ingrese el ID de la orden: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        pausar()
        return

    o = orden_trabajo.obtener_orden(id_orden)
    if o:
        imprimir_detalle([
            ("ID", o["id"]),
            ("Fecha Solicitud", o["fecha_solicitud"]),
            ("Fecha Ejecución", o["fecha_ejecucion"]),
            ("Descripción Falla", o["descripcion_falla"]),
            ("Prioridad", o["prioridad"]),
            ("Estado", o["estado"]),
            ("─── Equipo ───", ""),
            ("Código Equipo", o["equipo_codigo"]),
            ("Nombre Equipo", o["equipo_nombre"]),
            ("Tipo Equipo", o["equipo_tipo"]),
            ("Ubicación", o["equipo_ubicacion"]),
            ("─── Técnico ───", ""),
            ("Técnico", o["tecnico_nombre"]),
            ("Especialidad", o["tecnico_especialidad"]),
            ("─── Resolución ───", ""),
            ("Solución Aplicada", o["solucion_aplicada"]),
            ("Costo Repuestos", f"${o['costo_repuestos']:,.2f}" if o["costo_repuestos"] else "$0.00"),
        ])
    else:
        print(f"\n  ✗ No se encontró la orden de trabajo con ID {id_orden}.")
    pausar()


def crear_orden():
    """Formulario para crear una nueva orden de trabajo."""
    limpiar_pantalla()
    imprimir_titulo("CREAR NUEVA ORDEN DE TRABAJO")

    # Mostrar equipos disponibles
    print("\n  ── Equipos disponibles ──")
    equipos = equipo.obtener_equipos()
    for e in equipos:
        print(f"    {e['codigo']} - {e['nombre']} [{e['estado']}]")

    print()
    equipo_codigo = input("  Código del equipo: ").strip().upper()

    # Mostrar técnicos disponibles
    print("\n  ── Técnicos disponibles ──")
    tecnicos = tecnico.obtener_tecnicos()
    for t in tecnicos:
        print(f"    {t['documento']} - {t['nombre']} ({t['especialidad']})")

    print()
    tecnico_doc = input("  Documento del técnico: ").strip()
    fecha = input(f"  Fecha de solicitud (YYYY-MM-DD) [{date.today().isoformat()}]: ").strip()
    if not fecha:
        fecha = date.today().isoformat()
    descripcion = input("  Descripción de la falla: ").strip()
    print("  Prioridades: alta | media | baja")
    prioridad = input("  Prioridad: ").strip().lower()

    if not all([equipo_codigo, tecnico_doc, descripcion, prioridad]):
        print("\n  ✗ Todos los campos son obligatorios.")
        pausar()
        return

    id_orden = orden_trabajo.crear_orden(fecha, descripcion, prioridad,
                                          equipo_codigo, tecnico_doc)
    if id_orden:
        print(f"\n  ✓ Orden de trabajo #{id_orden} creada exitosamente.")
    pausar()


def actualizar_orden():
    """Formulario para actualizar una orden de trabajo."""
    limpiar_pantalla()
    imprimir_titulo("ACTUALIZAR ORDEN DE TRABAJO")
    try:
        id_orden = int(input("  Ingrese el ID de la orden a actualizar: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        pausar()
        return

    o = orden_trabajo.obtener_orden(id_orden)
    if not o:
        print(f"\n  ✗ No se encontró la orden con ID {id_orden}.")
        pausar()
        return

    print(f"\n  Orden #{o['id']} - Estado: {o['estado']}")
    print("  (Deje en blanco para mantener el valor actual)\n")

    descripcion = input(f"  Descripción [{o['descripcion_falla'][:50]}...]: ").strip() or None
    print("  Prioridades: alta | media | baja")
    prioridad = input(f"  Prioridad [{o['prioridad']}]: ").strip().lower() or None

    if orden_trabajo.actualizar_orden(id_orden, descripcion_falla=descripcion,
                                       prioridad=prioridad):
        print("\n  ✓ Orden actualizada exitosamente.")
    pausar()


def completar_orden():
    """Formulario para completar una orden de trabajo."""
    limpiar_pantalla()
    imprimir_titulo("COMPLETAR ORDEN DE TRABAJO")
    try:
        id_orden = int(input("  Ingrese el ID de la orden a completar: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        pausar()
        return

    o = orden_trabajo.obtener_orden(id_orden)
    if not o:
        print(f"\n  ✗ No se encontró la orden con ID {id_orden}.")
        pausar()
        return

    print(f"\n  Orden #{o['id']} - Equipo: {o['equipo_nombre']} - Estado: {o['estado']}")
    print()

    solucion = input("  Solución aplicada: ").strip()
    try:
        costo = float(input("  Costo de repuestos: $").strip() or "0")
    except ValueError:
        print("  ✗ Valor de costo inválido.")
        pausar()
        return

    if not solucion:
        print("\n  ✗ La solución aplicada es obligatoria.")
        pausar()
        return

    if orden_trabajo.completar_orden(id_orden, solucion, costo):
        print(f"\n  ✓ Orden #{id_orden} completada exitosamente.")
        print(f"  ✓ El equipo '{o['equipo_nombre']}' ha sido marcado como 'operativo'.")
    pausar()


def cancelar_orden():
    """Formulario para cancelar una orden de trabajo."""
    limpiar_pantalla()
    imprimir_titulo("CANCELAR ORDEN DE TRABAJO")
    try:
        id_orden = int(input("  Ingrese el ID de la orden a cancelar: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        pausar()
        return

    o = orden_trabajo.obtener_orden(id_orden)
    if not o:
        print(f"\n  ✗ No se encontró la orden con ID {id_orden}.")
        pausar()
        return

    print(f"\n  Orden #{o['id']} - Equipo: {o['equipo_nombre']} - Estado: {o['estado']}")
    if confirmar("¿Está seguro de que desea cancelar esta orden?"):
        if orden_trabajo.cancelar_orden(id_orden):
            print(f"\n  ✓ Orden #{id_orden} cancelada exitosamente.")
    else:
        print("\n  Operación cancelada.")
    pausar()


def cambiar_estado_orden():
    """Formulario para cambiar el estado de una orden."""
    limpiar_pantalla()
    imprimir_titulo("CAMBIAR ESTADO DE ORDEN")
    try:
        id_orden = int(input("  Ingrese el ID de la orden: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        pausar()
        return

    o = orden_trabajo.obtener_orden(id_orden)
    if not o:
        print(f"\n  ✗ No se encontró la orden con ID {id_orden}.")
        pausar()
        return

    print(f"\n  Orden #{o['id']} - Estado actual: {o['estado']}")
    print("  Estados: pendiente | en proceso | completada | cancelada")
    nuevo_estado = input("  Nuevo estado: ").strip().lower()

    if nuevo_estado == "completada":
        print("\n  ✗ Para completar una orden, use la opción 'Completar orden de trabajo'.")
        pausar()
        return

    if orden_trabajo.cambiar_estado_orden(id_orden, nuevo_estado):
        print(f"\n  ✓ Estado cambiado a '{nuevo_estado}'.")
    pausar()


def eliminar_orden():
    """Formulario para eliminar una orden de trabajo."""
    limpiar_pantalla()
    imprimir_titulo("ELIMINAR ORDEN DE TRABAJO")
    try:
        id_orden = int(input("  Ingrese el ID de la orden a eliminar: ").strip())
    except ValueError:
        print("  ✗ ID inválido.")
        pausar()
        return

    o = orden_trabajo.obtener_orden(id_orden)
    if not o:
        print(f"\n  ✗ No se encontró la orden con ID {id_orden}.")
        pausar()
        return

    print(f"\n  Orden #{o['id']} - Equipo: {o['equipo_nombre']} - Estado: {o['estado']}")
    if confirmar("¿Está seguro de que desea eliminar esta orden?"):
        if orden_trabajo.eliminar_orden(id_orden):
            print(f"\n  ✓ Orden #{id_orden} eliminada exitosamente.")
    else:
        print("\n  Operación cancelada.")
    pausar()


# ════════════════════════════════════════════════════════════════
# MENÚ DE HISTORIAL
# ════════════════════════════════════════════════════════════════

def menu_historial():
    """Submenú del historial de mantenimiento (solo lectura + filtros)."""
    while True:
        limpiar_pantalla()
        imprimir_titulo("HISTORIAL DE MANTENIMIENTO")
        print("  1. Ver historial completo")
        print("  2. Filtrar por equipo")
        print("  3. Filtrar por técnico")
        print("  4. Filtrar por rango de fechas")
        print("  0. Volver al menú principal")
        print()

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_historial()
        elif opcion == "2":
            filtrar_historial_equipo()
        elif opcion == "3":
            filtrar_historial_tecnico()
        elif opcion == "4":
            filtrar_historial_fechas()
        elif opcion == "0":
            break
        else:
            print("  ✗ Opción inválida.")
            pausar()


def mostrar_historial(filtro_equipo=None, filtro_tecnico=None,
                       filtro_fecha_inicio=None, filtro_fecha_fin=None):
    """Muestra el historial de mantenimiento con filtros opcionales."""
    limpiar_pantalla()
    imprimir_titulo("HISTORIAL DE MANTENIMIENTO COMPLETADO")

    registros = historial.ver_historial(
        filtro_equipo=filtro_equipo,
        filtro_tecnico=filtro_tecnico,
        filtro_fecha_inicio=filtro_fecha_inicio,
        filtro_fecha_fin=filtro_fecha_fin
    )

    headers = ["ID", "F. Solicitud", "F. Ejecución", "Equipo", "Técnico",
               "Prioridad", "Costo Rep."]
    rows = [[r["id"], r["fecha_solicitud"], r["fecha_ejecucion"],
             r["equipo_nombre"], r["tecnico_nombre"], r["prioridad"],
             f"${r['costo_repuestos']:,.0f}"] for r in registros]
    imprimir_tabla(headers, rows)

    # Mostrar detalles de cada registro
    if registros and confirmar("¿Desea ver el detalle de alguna orden?"):
        try:
            id_orden = int(input("  ID de la orden: ").strip())
        except ValueError:
            print("  ✗ ID inválido.")
            pausar()
            return

        for r in registros:
            if r["id"] == id_orden:
                imprimir_detalle([
                    ("ID", r["id"]),
                    ("Fecha Solicitud", r["fecha_solicitud"]),
                    ("Fecha Ejecución", r["fecha_ejecucion"]),
                    ("Equipo", f"{r['equipo_nombre']} ({r['equipo_codigo']})"),
                    ("Tipo Equipo", r["equipo_tipo"]),
                    ("Ubicación", r["equipo_ubicacion"]),
                    ("Técnico", f"{r['tecnico_nombre']} ({r['tecnico_especialidad']})"),
                    ("Prioridad", r["prioridad"]),
                    ("Descripción Falla", r["descripcion_falla"]),
                    ("Solución Aplicada", r["solucion_aplicada"]),
                    ("Costo Repuestos", f"${r['costo_repuestos']:,.2f}"),
                ])
                break
        else:
            print(f"  ✗ No se encontró la orden {id_orden} en el historial.")

    pausar()


def filtrar_historial_equipo():
    """Filtra el historial por código de equipo."""
    limpiar_pantalla()
    imprimir_titulo("FILTRAR HISTORIAL POR EQUIPO")

    # Mostrar equipos disponibles
    equipos = equipo.obtener_equipos()
    for e in equipos:
        print(f"    {e['codigo']} - {e['nombre']}")

    print()
    codigo = input("  Código del equipo: ").strip().upper()
    mostrar_historial(filtro_equipo=codigo)


def filtrar_historial_tecnico():
    """Filtra el historial por documento de técnico."""
    limpiar_pantalla()
    imprimir_titulo("FILTRAR HISTORIAL POR TÉCNICO")

    # Mostrar técnicos disponibles
    tecnicos = tecnico.obtener_tecnicos()
    for t in tecnicos:
        print(f"    {t['documento']} - {t['nombre']}")

    print()
    documento = input("  Documento del técnico: ").strip()
    mostrar_historial(filtro_tecnico=documento)


def filtrar_historial_fechas():
    """Filtra el historial por rango de fechas."""
    limpiar_pantalla()
    imprimir_titulo("FILTRAR HISTORIAL POR FECHAS")
    print()
    fecha_inicio = input("  Fecha inicio (YYYY-MM-DD) [dejar vacío = sin límite]: ").strip() or None
    fecha_fin = input("  Fecha fin (YYYY-MM-DD) [dejar vacío = sin límite]: ").strip() or None
    mostrar_historial(filtro_fecha_inicio=fecha_inicio, filtro_fecha_fin=fecha_fin)


# ════════════════════════════════════════════════════════════════
# MENÚ DE REPORTES
# ════════════════════════════════════════════════════════════════

def menu_reportes():
    """Submenú de reportes y consultas especiales."""
    while True:
        limpiar_pantalla()
        imprimir_titulo("REPORTES Y CONSULTAS ESPECIALES")
        print("  1. Equipos que nunca recibieron mantenimiento")
        print("  2. Top 2 equipos con más intervenciones")
        print("  3. Técnico con mayor costo acumulado en repuestos")
        print("  4. Órdenes atrasadas (más de 7 días sin completar)")
        print("  0. Volver al menú principal")
        print()

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            reporte_sin_mantenimiento()
        elif opcion == "2":
            reporte_top_equipos()
        elif opcion == "3":
            reporte_tecnico_costo()
        elif opcion == "4":
            reporte_ordenes_atrasadas()
        elif opcion == "0":
            break
        else:
            print("  ✗ Opción inválida.")
            pausar()


def reporte_sin_mantenimiento():
    """Muestra equipos que nunca recibieron mantenimiento."""
    limpiar_pantalla()
    imprimir_titulo("EQUIPOS SIN MANTENIMIENTO")
    resultados = reportes.equipos_sin_mantenimiento()
    headers = ["Código", "Nombre", "Tipo", "Ubicación", "F. Instalación", "Estado"]
    rows = [[r["codigo"], r["nombre"], r["tipo"], r["ubicacion"],
             r["fecha_instalacion"], r["estado"]] for r in resultados]
    imprimir_tabla(headers, rows)
    pausar()


def reporte_top_equipos():
    """Muestra el top 2 de equipos con más intervenciones."""
    limpiar_pantalla()
    imprimir_titulo("TOP 2 EQUIPOS CON MÁS INTERVENCIONES")
    resultados = reportes.top_equipos_intervenidos(2)
    headers = ["Código", "Nombre", "Tipo", "Ubicación", "Total Intervenciones"]
    rows = [[r["codigo"], r["nombre"], r["tipo"], r["ubicacion"],
             r["total_intervenciones"]] for r in resultados]
    imprimir_tabla(headers, rows)
    pausar()


def reporte_tecnico_costo():
    """Muestra el técnico con mayor costo acumulado en repuestos."""
    limpiar_pantalla()
    imprimir_titulo("TÉCNICO CON MAYOR COSTO ACUMULADO")
    resultado = reportes.tecnico_mayor_costo()
    if resultado:
        imprimir_detalle([
            ("Documento", resultado["documento"]),
            ("Nombre", resultado["nombre"]),
            ("Especialidad", resultado["especialidad"]),
            ("Total Órdenes", resultado["total_ordenes"]),
            ("Costo Total Repuestos", f"${resultado['costo_total']:,.2f}"),
        ])
    else:
        print("\n  (No hay datos suficientes para generar este reporte)\n")
    pausar()


def reporte_ordenes_atrasadas():
    """Muestra las órdenes de trabajo atrasadas (más de 7 días)."""
    limpiar_pantalla()
    imprimir_titulo("ÓRDENES DE TRABAJO ATRASADAS (>7 DÍAS)")
    resultados = reportes.ordenes_atrasadas()
    headers = ["ID", "F. Solicitud", "Equipo", "Técnico", "Prioridad", "Estado", "Días"]
    rows = [[r["id"], r["fecha_solicitud"], r["equipo_nombre"],
             r["tecnico_nombre"], r["prioridad"], r["estado"],
             r["dias_transcurridos"]] for r in resultados]
    imprimir_tabla(headers, rows)
    pausar()
