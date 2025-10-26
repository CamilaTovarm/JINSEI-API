from Repositories.SessionRepository import SessionRepository
from Repositories.UserRepository import UserRepository
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class SessionService:
    def __init__(self):
        self._session_repository = SessionRepository()
        self._user_repository = UserRepository()

    def get_all_sessions(self, include_deleted=False):
        """Obtiene todas las sesiones"""
        try:
            return self._session_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener sesiones: {str(e)}")

    def get_session_by_id(self, session_id, include_deleted=False):
        """Obtiene una sesión por ID"""
        try:
            session = self._session_repository.get_by_id(session_id, include_deleted=include_deleted)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            return session
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener sesión: {str(e)}")
    
    def get_sessions_by_user(self, user_id, include_deleted=False):
        """Obtiene todas las sesiones de un usuario"""
        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            return self._session_repository.get_by_user_id(user_id, include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener sesiones del usuario: {str(e)}")
    
    def get_active_session(self, user_id):
        """Obtiene la sesión activa de un usuario (sin EndTime)"""
        try:
            return self._session_repository.get_active_session(user_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener sesión activa: {str(e)}")

    def create_session(self, user_id, start_time=None, end_time=None, risk_level_id=None, final_risk_level=None):
        """Crea una nueva sesión"""
        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            # Verificar si ya tiene una sesión activa
            active_session = self._session_repository.get_active_session(user_id)
            if active_session:
                raise Exception(f"El usuario ya tiene una sesión activa (ID: {active_session.SessionId}).")
            
            return self._session_repository.create(
                user_id=user_id,
                start_time=start_time or datetime.utcnow(),
                end_time=end_time,
                risk_level_id=risk_level_id,
                final_risk_level=final_risk_level
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear sesión: {str(e)}")

    def update_session(self, session_id, user_id=None, start_time=None, end_time=None, risk_level_id=None, final_risk_level=None):
        """Actualiza una sesión existente"""
        try:
            # Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            # ✅ Usamos el método update() corregido con **kwargs
            update_data = {}
            if user_id is not None:
                update_data['UserId'] = user_id
            if start_time is not None:
                update_data['StartTime'] = start_time
            if end_time is not None:
                update_data['EndTime'] = end_time
            if risk_level_id is not None:
                update_data['RiskLevelId'] = risk_level_id
            if final_risk_level is not None:
                update_data['FinalRiskLevel'] = final_risk_level
            
            return self._session_repository.update(session_id, **update_data)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar sesión: {str(e)}")
    
    def end_session(self, session_id, final_risk_level=None):
        """Finaliza una sesión estableciendo el EndTime"""
        try:
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            if session.EndTime is not None:
                raise Exception(f"La sesión con ID {session_id} ya está finalizada.")
            
            return self._session_repository.end_session(session_id, final_risk_level)
        except SQLAlchemyError as e:
            raise Exception(f"Error al finalizar sesión: {str(e)}")

    def delete_session(self, session_id):
        """Marca una sesión como eliminada (soft delete)"""
        try:
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            # ✅ Solo pasamos el ID
            return self._session_repository.delete(session_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar sesión: {str(e)}")
    
    def restore_session(self, session_id):
        """Restaura una sesión marcada como eliminada"""
        try:
            session = self._session_repository.get_by_id(session_id, include_deleted=True)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            if not session.IsDeleted:
                raise Exception(f"La sesión con ID {session_id} no está eliminada.")
            
            return self._session_repository.restore(session_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar sesión: {str(e)}")