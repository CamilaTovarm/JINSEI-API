def register_controllers(app):
    """
    Registra todos los blueprints (controllers) en la aplicación Flask.
    
    Args:
        app: Instancia de la aplicación Flask
    """
    from .UserController import user_bp
    from .SessionController import session_bp
    from .MessageController import message_bp
    from .ConsentController import consent_bp
    from .ContactController import contact_bp
    from .ContactTypeController import contact_type_bp
    from .DocumentTypeController import document_type_bp
    from .RiskLevelController import risk_level_bp
    from .LoginController import auth_bp
    from .EmailController import email_bp
    
    # Registrar blueprints con prefijo '/api'
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(session_bp, url_prefix='/api')
    app.register_blueprint(message_bp, url_prefix='/api')
    app.register_blueprint(consent_bp, url_prefix='/api')
    app.register_blueprint(contact_bp, url_prefix='/api')
    app.register_blueprint(contact_type_bp, url_prefix='/api')
    app.register_blueprint(document_type_bp, url_prefix='/api')
    app.register_blueprint(risk_level_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(email_bp, url_prefix='/api')
    
    print("✅ Todos los controllers registrados exitosamente")