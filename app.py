from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from ConfigDB import init_db, db
from Controllers import register_controllers
from flask_mail import Mail 
import urllib
import Models
import os

mail = Mail()

def create_app():
    app = Flask(__name__)

    # Cadena de conexión directa para Azure SQL Database
    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=tcp:jinsei.database.windows.net,1433;"
        "DATABASE=JINSEI;"
        "UID=adminJinsei;"
        "PWD=Jinsei8988udec;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    
    params = urllib.parse.quote_plus(connection_string)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mssql+pyodbc:///?odbc_connect={params}" 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

    # EMAIL 
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
 
    app.config['MAIL_USERNAME'] = "notificaciones.jinsei@gmail.com"
    app.config['MAIL_PASSWORD'] = "cxlo gepz qrla lfph" 
    app.config['MAIL_DEFAULT_SENDER'] = "notificaciones.jinsei@gmail.com" 
    app.config['ALERT_EMAIL_RECIPIENT'] = "mctovar@ucundinamarca.edu.co"  

    CORS(app)
    init_db(app)
    Migrate(app, db)
    Swagger(app)
    mail.init_app(app)

    register_controllers(app)
    
    @app.route("/")
    def index():
        return jsonify({
            "message": "✅ API Jinsei conectada correctamente a Azure SQL Server 😎🐾",
            "docs": "/apidocs/"
        })

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Error al crear tablas: {str(e)}")
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)
else:
    # Para Gunicorn en Azure
    app = create_app()