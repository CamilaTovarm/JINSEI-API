from Repositories.MessageRepository import MessageRepository
from Repositories.UserRepository import UserRepository
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
import re

class UserService:
    def __init__(self):
        self._user_repository = UserRepository()
        self._message_repository = MessageRepository()

    def get_all_users(self, include_deleted=False):

        try:
            return self._user_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")

    def get_user_by_id(self, user_id, include_deleted=False):

        try:
            user = self._user_repository.get_by_id(user_id, include_deleted=include_deleted)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener usuario: {str(e)}")
    
    def get_user_by_aka(self, aka):

        try:
            user = self._user_repository.get_by_aka(aka)
            if not user:
                raise Exception(f"El usuario '{aka}' no existe.")
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar usuario: {str(e)}")
    

    def encrypt_password(self, password):

        return generate_password_hash(password, method='pbkdf2:sha256')

    def validate_password_strength(self, password):

        if len(password) < 8:
            raise Exception("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise Exception("La contraseña debe contener al menos una mayúscula.")
        if not re.search(r'[a-z]', password):
            raise Exception("La contraseña debe contener al menos una minúscula.")
        if not re.search(r'[0-9]', password):
            raise Exception("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise Exception("La contraseña debe contener al menos un carácter especial.")

    def create_user(self, aka, password):

        try:
            # 1. Validar que el AKA no exista
            existing_user = self._user_repository.get_by_aka(aka)
            if existing_user:
                raise Exception(f"El usuario '{aka}' ya existe.")
            
            # 2. Validar la contraseña
            self.validate_password_strength(password)
            
            # 3. Encriptar la contraseña 
            encrypted_password = self.encrypt_password(password)
            
            # 4. Crear el usuario 
            return self._user_repository.create(aka, encrypted_password)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear usuario: {str(e)}")

    def update_user(self, user_id, aka=None, password=None):

        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            # Validar que el nuevo AKA no esté en uso (si se está cambiando)
            if aka and aka != user.AKA:
                existing = self._user_repository.get_by_aka(aka)
                if existing:
                    raise Exception(f"El usuario '{aka}' ya existe.")
            
            # Si se proporciona una nueva contraseña, encriptarla
            encrypted_password = None
            if password:
                self._validate_password_strength(password)
                encrypted_password = self._encrypt_password(password)
            
            # Actualizar el usuario
            return self._user_repository.update(user_id, aka=aka, password=encrypted_password)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar usuario: {str(e)}")

    def delete_user(self, user_id):

        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
        
            return self._user_repository.delete(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar usuario: {str(e)}")
    
    def restore_user(self, user_id):

        try:
            user = self._user_repository.get_by_id(user_id, include_deleted=True)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            if not user.IsDeleted:
                raise Exception(f"El usuario con ID {user_id} no está eliminado.")
            
            return self._user_repository.restore(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar usuario: {str(e)}")