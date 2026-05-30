"""
Utilidades de presentación para la interfaz de consola.

Proporciona funciones para formatear tablas, limpiar pantalla
y pausar la ejecución esperando interacción del usuario.
"""

import os


def limpiar_pantalla():
    """Limpia la pantalla de la consola (compatible Windows/Linux)."""
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\n  Presione Enter para continuar...")


def imprimir_tabla(headers, rows, anchos=None):
    """
    Imprime datos en formato de tabla ASCII con bordes.

    Args:
        headers: Lista de encabezados de columna.
        rows: Lista de listas con los datos de cada fila.
        anchos: Lista opcional de anchos para cada columna.
                Si no se proporciona, se calculan automáticamente.
    """
    if not rows:
        print("\n  (No se encontraron registros)\n")
        return

    # Convertir Row objects a listas si es necesario
    filas = []
    for row in rows:
        if hasattr(row, "keys"):
            filas.append([str(v) if v is not None else "" for v in row])
        else:
            filas.append([str(v) if v is not None else "" for v in row])

    # Calcular anchos de columna
    if anchos is None:
        anchos = []
        for i, h in enumerate(headers):
            ancho_header = len(str(h))
            ancho_datos = max((len(str(fila[i])) for fila in filas), default=0) if filas else 0
            anchos.append(max(ancho_header, ancho_datos, 5))

    # Limitar ancho máximo por columna
    max_ancho = 40
    anchos = [min(a, max_ancho) for a in anchos]

    # Construir líneas
    separador = "  +" + "+".join("-" * (a + 2) for a in anchos) + "+"

    # Encabezados
    print(f"\n{separador}")
    header_line = "  |" + "|".join(
        f" {str(h)[:a].center(a)} " for h, a in zip(headers, anchos)
    ) + "|"
    print(header_line)
    print(separador)

    # Filas de datos
    for fila in filas:
        linea = "  |" + "|".join(
            f" {str(fila[i])[:a].ljust(a)} " for i, a in enumerate(anchos)
        ) + "|"
        print(linea)

    print(separador)
    print(f"  Total: {len(filas)} registro(s)\n")


def imprimir_detalle(campos):
    """
    Imprime un registro en formato detallado (clave: valor).

    Args:
        campos: Lista de tuplas (etiqueta, valor).
    """
    max_etiqueta = max(len(e) for e, _ in campos)
    print()
    print("  " + "─" * (max_etiqueta + 30))
    for etiqueta, valor in campos:
        valor_str = str(valor) if valor is not None else "(vacío)"
        print(f"  │ {etiqueta.ljust(max_etiqueta)} │ {valor_str}")
    print("  " + "─" * (max_etiqueta + 30))
    print()


def imprimir_titulo(titulo):
    """
    Imprime un título decorado para secciones del menú.

    Args:
        titulo: Texto del título.
    """
    ancho = max(len(titulo) + 6, 45)
    print()
    print("  " + "═" * ancho)
    print("  " + titulo.center(ancho))
    print("  " + "═" * ancho)


def confirmar(mensaje="¿Está seguro?"):
    """
    Solicita confirmación del usuario (s/n).

    Args:
        mensaje: Mensaje de confirmación.

    Returns:
        True si el usuario confirma, False en caso contrario.
    """
    respuesta = input(f"  {mensaje} (s/n): ").strip().lower()
    return respuesta in ("s", "si", "sí")
