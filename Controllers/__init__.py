
from .ConsentController import consent_bp
from .ContactController import contact_bp
from .ContactTypeController import contact_type_bp
from .DocumentTypeController import document_type_bp
from .RiskLevelController import risk_level_bp
from .SessionController import session_bp
from .UserController import user_bp

def register_controllers(app):
    """
    Registra automáticamente todos los Blueprints de los controladores.
    Así Flask reconoce todas las rutas definidas y Swagger las muestra.
    """
    app.register_blueprint(consent_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(contact_type_bp)
    app.register_blueprint(document_type_bp)
    app.register_blueprint(risk_level_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(user_bp)
