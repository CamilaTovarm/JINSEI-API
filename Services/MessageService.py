from Repositories.MessageRepository import MessageRepository
from Repositories.SessionRepository import SessionRepository
from Repositories.RiskLevelRepository import RiskLevelRepository
from sqlalchemy.exc import SQLAlchemyError

class MessageService:
    def __init__(self):
        self._message_repository = MessageRepository()
        self._session_repository = SessionRepository()
        self._risk_level_repository = RiskLevelRepository()

    def get_all_messages(self, include_deleted=False):
        try: 
            return self._message_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener mensajes: {str(e)}")

    def get_message_by_id(self, message_id, include_deleted=False):
        try: 
            message = self._message_repository.get_by_id(message_id, include_deleted=include_deleted)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
            return message
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener mensaje: {str(e)}")
    
    def get_messages_by_session(self, session_id, include_deleted=False):
        try: 
            # Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            return self._message_repository.get_by_session_id(session_id, include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener mensajes de la sesión: {str(e)}")

    def _calculate_risk_level_id(self, risk_percent):
        """
        Calcula el RiskLevelId basado en el porcentaje de riesgo.
        Retorna el ID correspondiente de la tabla RiskLevels.
        """
        try:
            if risk_percent is None:
                return None

            risk_levels = self._risk_level_repository.get_all()
            
            if not risk_levels:
                return None

            if risk_percent <= 20:
                # Buscar "Bajo" en la descripción
                for level in risk_levels:
                    if level.description and 'bajo' in level.description.lower():
                        return level.RiskLevelId
                return 1  # Fallback por defecto
            elif risk_percent <= 66:
                # Buscar "Medio" en la descripción
                for level in risk_levels:
                    if level.description and 'medio' in level.description.lower():
                        return level.RiskLevelId
                return 2  # Fallback por defecto
            else:
                # Buscar "Alto" en la descripción
                for level in risk_levels:
                    if level.description and 'alto' in level.description.lower():
                        return level.RiskLevelId
                return 3  # Fallback por defecto
        except Exception as e:
            print(f"Error al calcular RiskLevelId: {str(e)}")
            return None

    def create_message(self, user_id, bot_message, user_response=None, risk_percent=None):
        """
        Crea un mensaje asociado a la sesión activa del usuario.
        Calcula automáticamente el RiskLevelId basado en risk_percent.
        
        Args:
            user_id: ID del usuario (requerido para obtener su sesión activa)
            bot_message: Mensaje enviado por el bot
            user_response: Respuesta del usuario (opcional)
            risk_percent: Porcentaje de riesgo (0-100)
        """
        try:
            # Obtener la sesión activa del usuario
            active_session = self._session_repository.get_active_session(user_id)
            
            if not active_session:
                raise Exception(f"El usuario con ID {user_id} no tiene una sesión activa. Debe crear una sesión primero.")
            
            # Calcular el RiskLevelId basado en el porcentaje
            risk_level_id = None
            if risk_percent is not None:
                risk_level_id = self._calculate_risk_level_id(risk_percent)
            
            # Crear el mensaje con la sesión activa del usuario
            return self._message_repository.create(
                session_id=active_session.SessionId,
                bot_message=bot_message,
                user_response=user_response,
                risk_level_id=risk_level_id,
                risk_percent=risk_percent
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear mensaje: {str(e)}")

    def update_message(self, message_id, session_id=None, bot_message=None, user_response=None, risk_level_id=None, risk_percent=None):
        """
        Actualiza un mensaje existente.
        Si se proporciona risk_percent pero no risk_level_id, lo calcula automáticamente.
        """
        try:
            # Validar que el mensaje existe
            message = self._message_repository.get_by_id(message_id)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
        
            update_data = {}
            if session_id is not None:
                update_data['SessionId'] = session_id
            if bot_message is not None:
                update_data['BotMessage'] = bot_message
            if user_response is not None:
                update_data['UserResponse'] = user_response
            
            # Si se proporciona risk_percent, calcular risk_level_id automáticamente
            if risk_percent is not None:
                update_data['RiskPercent'] = risk_percent
                if risk_level_id is None:  # Solo calcular si no se proporciona explícitamente
                    calculated_risk_level_id = self._calculate_risk_level_id(risk_percent)
                    if calculated_risk_level_id is not None:
                        update_data['RiskLevelId'] = calculated_risk_level_id
            
            # Si se proporciona risk_level_id explícitamente, usarlo
            if risk_level_id is not None: 
                update_data['RiskLevelId'] = risk_level_id
            
            return self._message_repository.update(message_id, **update_data)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar mensaje: {str(e)}")

    def delete_message(self, message_id): 
        try:
            message = self._message_repository.get_by_id(message_id)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
        
            return self._message_repository.delete(message_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar mensaje: {str(e)}")
    
    def restore_message(self, message_id): 
        try:
            message = self._message_repository.get_by_id(message_id, include_deleted=True)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
            
            if not message.IsDeleted:
                raise Exception(f"El mensaje con ID {message_id} no está eliminado.")
            
            return self._message_repository.restore(message_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar mensaje: {str(e)}")