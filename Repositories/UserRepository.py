from ConfigDB import db
from Models.User import User
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):
        """Obtiene todos los usuarios"""
        if include_deleted:
            return User.query.all()
        return User.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, user_id, include_deleted=False):
        """Obtiene un usuario por ID"""
        if include_deleted:
            return User.query.filter_by(UserId=user_id).first()
        return User.query.filter_by(UserId=user_id, IsDeleted=False).first()
    
    def get_by_aka(self, aka):
        """Obtiene un usuario por su AKA (útil para login)"""
        return User.query.filter_by(AKA=aka, IsDeleted=False).first()

    def create(self, aka, password):
        """Crea un nuevo usuario"""
        try:
            new_user = User(AKA=aka, Password=password, IsDeleted=False)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, user_id, aka=None, password=None):
        """Actualiza un usuario existente"""
        try:
            existing = User.query.get(user_id)
            if not existing or existing.IsDeleted:
                return None
            
            if aka:
                existing.AKA = aka
            if password:
                existing.Password = password
            
            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, user_id):
        """Marca un usuario como eliminado (soft delete)"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None
            
            user.IsDeleted = True
            self.db.session.commit()
            return user
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, user_id):
        """Restaura un usuario marcado como eliminado"""
        try:
            user = User.query.get(user_id)
            if not user:
                return None
            
            user.IsDeleted = False
            self.db.session.commit()
            return user
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e