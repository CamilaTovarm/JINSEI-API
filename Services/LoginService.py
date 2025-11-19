from Repositories.UserRepository import UserRepository
from werkzeug.security import check_password_hash
from sqlalchemy.exc import SQLAlchemyError

class AuthService:
    def __init__(self):
        self._user_repository = UserRepository()

    def authenticate_user(self, aka, password):
        """
        Autentica un usuario verificando AKA y password.
        Retorna el usuario si las credenciales son válidas.
        """
        try:
            # 1. Obtener el usuario por AKA (username)
            user = self._user_repository.get_by_aka(aka)

            if not user:
                raise Exception("Usuario o contraseña incorrectos.")

            # 2. Verificar que no esté eliminado
            if user.IsDeleted:
                raise Exception("Esta cuenta ha sido desactivada.")

            # 3. Verificar la contraseña hasheada
            # check_password_hash compara la contraseña en texto plano
            # con la contraseña hasheada almacenada en la BD
            if not check_password_hash(user.Password, password):
                raise Exception("Usuario o contraseña incorrectos.")

            # 4. Autenticación exitosa
            return user

        except SQLAlchemyError as e:
            raise Exception(f"Error en la autenticación: {str(e)}")

    def get_user_by_aka(self, aka):
        """Obtiene un usuario por su AKA"""
        try:
            user = self._user_repository.get_by_aka(aka)
            if not user:
                raise Exception(f"El usuario '{aka}' no existe.")
            return user
        except SQLAlchemyError as e:
            raise Exception(f"Error al buscar usuario: {str(e)}")

    def validate_credentials_format(self, aka, password):
        """Valida el formato de las credenciales antes de autenticar"""
        if not aka or not password:
            raise Exception("El usuario y la contraseña son requeridos.")
        
        if len(aka) < 3:
            raise Exception("El nombre de usuario debe tener al menos 3 caracteres.")
        
        if len(password) < 8:
            raise Exception("La contraseña debe tener al menos 8 caracteres.")