from flask_sqlalchemy import SQLAlchemy
import pyodbc

db = SQLAlchemy()


def ensure_database_exists(server_name: str, database_name: str):

    try:
        # Conexión al servidor 
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server_name};"
            f"Trusted_Connection=yes;"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Verificar si existe la base de datos
        cursor.execute(f"SELECT name FROM sys.databases WHERE name = '{database_name}'")
        exists = cursor.fetchone()

        # Crear base de datos si no existe
        if not exists:
            cursor.execute(f"CREATE DATABASE [{database_name}]")
            print(f"✅ Base de datos '{database_name}' creada exitosamente 😄")
        else:
            print(f"La base de datos '{database_name}' ya existe!!")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error al verificar/crear la base de datos:", e)


def init_db(app):
    """Inicializa SQLAlchemy dentro de la app Flask"""
    db.init_app(app)
