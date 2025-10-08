from flask import Flask
from flasgger import Swagger
from Models.Database import db, init_db

from Controllers.UserController import user_bp
from Controllers.ChatController import chat_bp
from Controllers.ConsentController import consent_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chatbot.db"  # Cambiar luego por SQL Server
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

swagger = Swagger(app)
db.init_app(app)

# Registrar controladores
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(chat_bp, url_prefix="/chat")
app.register_blueprint(consent_bp, url_prefix="/consent")

with app.app_context():
    init_db()

if __name__ == "__main__":
    app.run(debug=True)
