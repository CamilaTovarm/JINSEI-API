from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    """Inicializa SQLAlchemy y vincula la app Flask."""
    db.init_app(app)
