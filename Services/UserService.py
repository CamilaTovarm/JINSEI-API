from Repositories.UserRepository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

class UserService:
    def __init__(self):
        self._user_repository = UserRepository()

    def get_all_users(self, include_deleted=False):
        """Obtiene todos los usuarios"""
        try:
            return self._user_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener usuarios: {str(e)}")

    def get_user_by_id(self, user_id, include_deleted=False):
        """Obtiene un usuario por ID"""
        try:
            user = self._user_repository.get_by_id(user_id, include_deleted=include_deleted)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener usuario: {str(e)}")
    
    def get_user_by_aka(self, aka):
        """Obtiene un usuario por su AKA (útil para login)"""
        try:
            user = self._user_repository.get_by_aka(aka)
            if not user:
                raise Exception(f"El usuario '{aka}' no existe.")
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar usuario: {str(e)}")

    def create_user(self, aka, password):
        """Crea un nuevo usuario"""
        try:
            # Validación: verificar si el AKA ya existe
            existing_user = self._user_repository.get_by_aka(aka)
            if existing_user:
                raise Exception(f"El usuario '{aka}' ya existe.")
            
            return self._user_repository.create(aka, password)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear usuario: {str(e)}")

    def update_user(self, user_id, aka=None, password=None):
        """Actualiza un usuario existente"""
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
            
            # ✅ Ahora usamos el método update() corregido del repositorio
            return self._user_repository.update(user_id, aka=aka, password=password)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar usuario: {str(e)}")

    def delete_user(self, user_id):
        """Marca un usuario como eliminado (soft delete)"""
        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            # ✅ Ahora solo pasamos el ID
            return self._user_repository.delete(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar usuario: {str(e)}")
    
    def restore_user(self, user_id):
        """Restaura un usuario marcado como eliminado"""
        try:
            user = self._user_repository.get_by_id(user_id, include_deleted=True)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            if not user.IsDeleted:
                raise Exception(f"El usuario con ID {user_id} no está eliminado.")
            
            return self._user_repository.restore(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar usuario: {str(e)}")