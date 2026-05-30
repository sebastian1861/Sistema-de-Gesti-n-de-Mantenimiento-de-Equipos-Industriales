"""
Sistema de Gestión de Mantenimiento de Equipos
Punto de entrada principal de la aplicación.

Este sistema permite gestionar el ciclo de vida del mantenimiento
de equipos industriales, incluyendo planificación, ejecución,
historial y generación de reportes.
"""

import sys
import os

# Configurar encoding UTF-8 para la consola de Windows
if sys.platform == "win32":
    os.system("chcp 65001 >nul 2>&1")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Database
from views.menu import menu_principal


def main():
    """Función principal del sistema."""
    print()
    print("  ╔═══════════════════════════════════════════════════╗")
    print("  ║   SISTEMA DE GESTIÓN DE MANTENIMIENTO DE EQUIPOS ║")
    print("  ║          Inicializando sistema...                 ║")
    print("  ╚═══════════════════════════════════════════════════╝")
    print()

    # Inicializar base de datos
    db = Database()
    try:
        db.inicializar()
        print()
        input("  Presione Enter para continuar al menú principal...")

        # Lanzar menú principal
        menu_principal()

    except KeyboardInterrupt:
        print("\n\n  Sistema interrumpido por el usuario.")
    except Exception as e:
        print(f"\n  ✗ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.cerrar()
        print("  ✓ Conexión a la base de datos cerrada.")
        print()


if __name__ == "__main__":
    main()
