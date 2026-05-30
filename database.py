"""
Módulo de conexión y gestión de la base de datos SQLite.

Proporciona una clase Database con patrón Singleton para gestionar
la conexión, ejecución de consultas e inicialización del esquema.
"""

import sqlite3
import os

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "mantenimiento.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


class Database:
    """Clase Singleton para gestionar la conexión a la base de datos SQLite."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._conexion = None
        return cls._instance

    def conectar(self):
        """Establece la conexión a la base de datos y activa claves foráneas."""
        if self._conexion is None:
            self._conexion = sqlite3.connect(DB_PATH, check_same_thread=False)
            self._conexion.execute("PRAGMA foreign_keys = ON")
            # Retornar filas como objetos Row (acceso por nombre de columna)
            self._conexion.row_factory = sqlite3.Row
        return self._conexion

    def inicializar(self):
        """
        Inicializa la base de datos ejecutando schema.sql.
        Solo ejecuta el script si la base de datos no tiene tablas creadas.
        """
        conn = self.conectar()

        # Verificar si las tablas ya existen
        cursor = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='equipos'"
        )
        tablas_existen = cursor.fetchone()[0] > 0

        if tablas_existen:
            print("  [OK] Base de datos ya inicializada.")
            return

        if os.path.exists(SCHEMA_PATH):
            with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
                script = f.read()
            conn.executescript(script)
            conn.commit()
            print("  [OK] Base de datos inicializada correctamente.")
        else:
            print(f"  [ERROR] No se encontro el archivo de esquema: {SCHEMA_PATH}")

    def ejecutar(self, query, params=None):
        """
        Ejecuta una consulta SQL (INSERT, UPDATE, DELETE).

        Args:
            query: Sentencia SQL a ejecutar.
            params: Tupla con los parámetros de la consulta.

        Returns:
            El cursor resultante de la ejecución.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor
        except sqlite3.IntegrityError as e:
            conn.rollback()
            raise e
        except sqlite3.Error as e:
            conn.rollback()
            raise e

    def fetchone(self, query, params=None):
        """
        Ejecuta una consulta y retorna un solo registro.

        Args:
            query: Sentencia SQL SELECT.
            params: Tupla con los parámetros de la consulta.

        Returns:
            Un registro (sqlite3.Row) o None si no hay resultados.
        """
        conn = self.conectar()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchone()

    def fetchall(self, query, params=None):
        """
        Ejecuta una consulta y retorna todos los registros.

        Args:
            query: Sentencia SQL SELECT.
            params: Tupla con los parámetros de la consulta.

        Returns:
            Lista de registros (sqlite3.Row).
        """
        conn = self.conectar()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()

    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        if self._conexion:
            self._conexion.close()
            self._conexion = None
            Database._instance = None
