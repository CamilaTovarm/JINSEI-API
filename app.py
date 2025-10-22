from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from ConfigDB import init_db, db, ensure_database_exists
from Controllers import register_controllers
import urllib
import Models

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

    CORS(app)
    init_db(app)
    Migrate(app, db)
    Swagger(app)

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
