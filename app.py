from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from ConfigDB import init_db, db  
from flask_mail import Mail   
import urllib   
import os

# NO importar Models ni Controllers aquí arriba

mail = Mail()

# Crear la app PRIMERO, a nivel de módulo
app = Flask(__name__)

# Configurar la base de datos
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=tcp:jinsei.database.windows.net,1433;"
    "DATABASE=JINSEI;"
    "UID=adminJinsei;"
    "PWD=Jinsei8988udec;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=60;"
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

# Inicializar extensiones
CORS(app)
init_db(app)
Migrate(app, db)
Swagger(app)
mail.init_app(app)

# AHORA SÍ importar Models y Controllers (después de tener app configurado)
import Models
from Controllers import register_controllers

# Registrar rutas base
@app.route("/")
def index():
    return jsonify({
        "message": "✅ API Jinsei conectada correctamente a Azure SQL Server 😎🐾",
        "docs": "/apidocs/",
        "status": "running"
    })

@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)[:200]}"
    
    return jsonify({
        "status": "healthy" if db_status == "connected" else "degraded",
        "database": db_status
    }), 200 if db_status == "connected" else 503

# Registrar controllers
try:
    register_controllers(app)
    print("✅ Todos los controllers registrados exitosamente")
except Exception as e:
    print(f"❌ Error al registrar controllers: {str(e)}")
    import traceback
    traceback.print_exc()   


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=False)