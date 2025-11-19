from Repositories.SessionRepository import SessionRepository
from Repositories.UserRepository import UserRepository
from Repositories.MessageRepository import MessageRepository
from Repositories.RiskLevelRepository import RiskLevelRepository
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class SessionService:
    def __init__(self):
        self._session_repository = SessionRepository()
        self._user_repository = UserRepository()
        self._message_repository = MessageRepository()
        self._risk_level_repository = RiskLevelRepository()

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

    def _calculate_risk_level_id(self, average_percent):
        """
        Determina el RiskLevelId basado en el promedio de porcentaje.
        
        Rangos sugeridos (ajusta según tus necesidades):
        - Bajo: 0-33%
        - Medio: 34-66%
        - Alto: 67-100%
        
        Retorna el ID correspondiente de la tabla RiskLevels
        """
        try:
            # Obtener todos los niveles de riesgo
            risk_levels = self._risk_level_repository.get_all()
            
            if not risk_levels:
                return None
            
            # Asumiendo que los IDs son: 1=Bajo, 2=Medio, 3=Alto
            # Ajusta estos valores según tu tabla RiskLevels
            if average_percent <= 33:
                # Buscar "Bajo" en la descripción
                for level in risk_levels:
                    if level.description and 'bajo' in level.description.lower():
                        return level.RiskLevelId
                return 1  # Fallback al ID 1
            elif average_percent <= 66:
                # Buscar "Medio" en la descripción
                for level in risk_levels:
                    if level.description and 'medio' in level.description.lower():
                        return level.RiskLevelId
                return 2  # Fallback al ID 2
            else:
                # Buscar "Alto" en la descripción
                for level in risk_levels:
                    if level.description and 'alto' in level.description.lower():
                        return level.RiskLevelId
                return 3  # Fallback al ID 3
        except Exception as e:
            print(f"Error al calcular RiskLevelId: {str(e)}")
            return None

    def _calculate_average_risk(self, session_id):
        """
        Calcula el promedio de RiskPercent de todos los mensajes de una sesión.
        
        Returns:
            float: Promedio de los porcentajes de riesgo, o 0 si no hay mensajes
        """
        try:
            # Obtener todos los mensajes de la sesión
            messages = self._message_repository.get_by_session_id(session_id, include_deleted=False)
            
            if not messages:
                return 0.0
            
            # Filtrar mensajes que tienen RiskPercent no nulo
            risk_percentages = [msg.RiskPercent for msg in messages if msg.RiskPercent is not None]
            
            if not risk_percentages:
                return 0.0
            
            # Calcular promedio
            average = sum(risk_percentages) / len(risk_percentages)
            return round(average, 2)  # Redondear a 2 decimales
            
        except Exception as e:
            print(f"Error al calcular promedio de riesgo: {str(e)}")
            return 0.0

    def create_session(self, user_id):
        """
        Crea una nueva sesión (sin solicitar risk_level_id ni final_risk_level).
        Estos campos se calcularán automáticamente al finalizar la sesión.
        """
        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            # Verificar si ya tiene una sesión activa
            active_session = self._session_repository.get_active_session(user_id)
            if active_session:
                raise Exception(f"El usuario ya tiene una sesión activa (ID: {active_session.SessionId}).")
            
            # Crear sesión sin RiskLevelId ni FinalRiskLevel
            return self._session_repository.create(
                user_id=user_id,
                start_time=datetime.utcnow(),
                end_time=None,
                risk_level_id=None,
                final_risk_level=None
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear sesión: {str(e)}")

    def update_session(self, session_id, user_id=None):
        """
        Actualiza una sesión existente.
        Solo permite actualizar el user_id.
        Los campos de riesgo se calculan automáticamente al finalizar.
        """
        try:
            # Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            update_data = {}
            if user_id is not None:
                # Validar que el nuevo usuario existe
                user = self._user_repository.get_by_id(user_id)
                if not user:
                    raise Exception(f"El usuario con ID {user_id} no existe.")
                update_data['UserId'] = user_id
            
            if not update_data:
                raise Exception("No se proporcionaron campos para actualizar.")
            
            return self._session_repository.update(session_id, **update_data)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar sesión: {str(e)}")
    
    def end_session(self, session_id):
        """
        Finaliza una sesión calculando automáticamente:
        1. El promedio de RiskPercent de todos los mensajes (FinalRiskLevel)
        2. El RiskLevelId correspondiente según el promedio
        """
        try:
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            if session.EndTime is not None:
                raise Exception(f"La sesión con ID {session_id} ya está finalizada.")
            
            # Calcular el promedio de riesgo de todos los mensajes
            average_risk = self._calculate_average_risk(session_id)
            
            # Determinar el RiskLevelId basado en el promedio
            risk_level_id = self._calculate_risk_level_id(average_risk)
            
            # Actualizar la sesión con EndTime, FinalRiskLevel (promedio) y RiskLevelId
            update_data = {
                'EndTime': datetime.utcnow(),
                'FinalRiskLevel': average_risk,  # Guardamos el promedio numérico
                'RiskLevelId': risk_level_id
            }
            
            return self._session_repository.update(session_id, **update_data)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al finalizar sesión: {str(e)}")

    def delete_session(self, session_id):
        """Marca una sesión como eliminada (soft delete)"""
        try:
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
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
        


    def get_session_messages_history(self, session_id, include_deleted=False):
        """
        Obtiene el historial completo de mensajes de una sesión específica.
        
        Args:
            session_id: ID de la sesión
            include_deleted: Si incluir mensajes eliminados
            
        Returns:
            dict: Información de la sesión con su historial de mensajes
        """
        try:
            # Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id, include_deleted=include_deleted)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            # Obtener todos los mensajes de la sesión
            messages = self._message_repository.get_by_session_id(session_id, include_deleted=include_deleted)
            
            # Construir respuesta con información de la sesión y mensajes
            return {
                'session': session,
                'messages': messages,
                'total_messages': len(messages)
            }
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener historial de mensajes: {str(e)}")
    
    def get_user_complete_history(self, user_id, include_deleted=False):
        """
        Obtiene el historial completo de todas las sesiones y mensajes de un usuario.
        
        Args:
            user_id: ID del usuario
            include_deleted: Si incluir sesiones y mensajes eliminados
            
        Returns:
            dict: Información del usuario con todas sus sesiones y mensajes
        """
        try:
            # Validar que el usuario existe
            user = self._user_repository.get_by_id(user_id, include_deleted=include_deleted)
            if not user:
                raise Exception(f"El usuario con ID {user_id} no existe.")
            
            # Obtener todas las sesiones del usuario
            sessions = self._session_repository.get_by_user_id(user_id, include_deleted=include_deleted)
            
            # Para cada sesión, obtener sus mensajes
            sessions_with_messages = []
            total_messages = 0
            
            for session in sessions:
                messages = self._message_repository.get_by_session_id(
                    session.SessionId, 
                    include_deleted=include_deleted
                )
                
                sessions_with_messages.append({
                    'session': session,
                    'messages': messages,
                    'message_count': len(messages)
                })
                
                total_messages += len(messages)
            
            return {
                'user': user,
                'sessions': sessions_with_messages,
                'total_sessions': len(sessions),
                'total_messages': total_messages
            }
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener historial completo del usuario: {str(e)}")