from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from flask_migrate import Migrate
from ConfigDB import init_db, db

# ... (importa tus blueprints como antes)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://localhost/Jinsei?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    init_db(app)
    migrate = Migrate(app, db)  # <<<<< NUEVA LÍNEA

    Swagger(app)
    
    # ... tus blueprints y rutas ...

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
