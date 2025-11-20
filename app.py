from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from ConfigDB import init_db, db, ensure_database_exists
from Controllers import register_controllers
from flask_mail import Mail
from dotenv import load_dotenv
import urllib
import Models
import os

mail = Mail()

def create_app():
    app = Flask(__name__)

    SERVER_NAME = "HPPAVILION"   # 👈 nombre de tu servidor local
    DATABASE_NAME = "JINSEI"     # 👈 nombre de la base de datos

    ensure_database_exists(SERVER_NAME, DATABASE_NAME)
                           
    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={SERVER_NAME};"
        f"DATABASE={DATABASE_NAME};"
        "Trusted_Connection=yes;"
        "Encrypt=yes;"
        "TrustServerCertificate=yes;"
        "Application Name=FlaskApp;"
    )
    params = urllib.parse.quote_plus(connection_string)

    app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    # ============================================================
    # CONFIGURACIÓN DE CORREO ELECTRÓNICO (TEST LOCAL)
    # ============================================================
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    # 👉 Coloca directamente tu correo y contraseña de aplicación
    app.config['MAIL_USERNAME'] = "notificaciones.jinsei@gmail.com"
    app.config['MAIL_PASSWORD'] = "cxlo gepz qrla lfph"

    app.config['MAIL_DEFAULT_SENDER'] = "notificaciones.jinsei@gmail.com"

    # Email donde se enviarán las alertas
    app.config['ALERT_EMAIL_RECIPIENT'] = "mctovar@ucundinamarca.edu.co"
    # ============================================================



    CORS(app)
    init_db(app)
    Migrate(app, db)
    Swagger(app)
    mail.init_app(app)  # Inicializar Flask-Mail

    register_controllers(app)
    
    @app.route("/")
    def index():
        return jsonify({
            "message": "✅ API Jinsei conectada correctamente a SQL Server",
            "docs": "/apidocs/"
        })

    with app.app_context():
        db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
