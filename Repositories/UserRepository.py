from Models.Database import db
from Models.User import User
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(alias, password):
    """Crea un nuevo usuario con contraseña cifrada."""
    existing = User.query.filter_by(alias=alias).first()
    if existing:
        raise ValueError("El alias ya existe.")

    hashed = generate_password_hash(password)
    user = User(alias=alias, password_hash=hashed)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_alias(alias):
    """Obtiene un usuario por su alias."""
    return User.query.filter_by(alias=alias).first()

def verify_user(alias, password):
    """Verifica alias y contraseña."""
    user = get_user_by_alias(alias)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None
