from Repositories.MessageRepository import MessageRepository
from Repositories.SessionRepository import SessionRepository
from sqlalchemy.exc import SQLAlchemyError

class MessageService:
    def __init__(self):
        self._message_repository = MessageRepository()
        self._session_repository = SessionRepository()

    def get_all_messages(self, include_deleted=False):
        """Obtiene todos los mensajes"""
        try:
            return self._message_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener mensajes: {str(e)}")

    def get_message_by_id(self, message_id, include_deleted=False):
        """Obtiene un mensaje por ID"""
        try:
            message = self._message_repository.get_by_id(message_id, include_deleted=include_deleted)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
            return message
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener mensaje: {str(e)}")
    
    def get_messages_by_session(self, session_id, include_deleted=False):
        """Obtiene todos los mensajes de una sesión"""
        try:
            # Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            return self._message_repository.get_by_session_id(session_id, include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener mensajes de la sesión: {str(e)}")

    def create_message(self, session_id, bot_message, user_response=None, risk_level_id=None, risk_percent=None):
        """Crea un nuevo mensaje"""
        try:
            # Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            return self._message_repository.create(
                session_id=session_id,
                bot_message=bot_message,
                user_response=user_response,
                risk_level_id=risk_level_id,
                risk_percent=risk_percent
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear mensaje: {str(e)}")

    def update_message(self, message_id, session_id=None, bot_message=None, user_response=None, risk_level_id=None, risk_percent=None):
        """Actualiza un mensaje existente"""
        try:
            # Validar que el mensaje existe
            message = self._message_repository.get_by_id(message_id)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
            
            # ✅ Usamos el método update() corregido con **kwargs
            update_data = {}
            if session_id is not None:
                update_data['SessionId'] = session_id
            if bot_message is not None:
                update_data['BotMessage'] = bot_message
            if user_response is not None:
                update_data['UserResponse'] = user_response
            if risk_level_id is not None:
                update_data['RiskLevelId'] = risk_level_id
            if risk_percent is not None:
                update_data['RiskPercent'] = risk_percent
            
            return self._message_repository.update(message_id, **update_data)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar mensaje: {str(e)}")

    def delete_message(self, message_id):
        """Marca un mensaje como eliminado (soft delete)"""
        try:
            message = self._message_repository.get_by_id(message_id)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
            
            # ✅ Solo pasamos el ID
            return self._message_repository.delete(message_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar mensaje: {str(e)}")
    
    def restore_message(self, message_id):
        """Restaura un mensaje marcado como eliminado"""
        try:
            message = self._message_repository.get_by_id(message_id, include_deleted=True)
            if not message:
                raise Exception(f"El mensaje con ID {message_id} no existe.")
            
            if not message.IsDeleted:
                raise Exception(f"El mensaje con ID {message_id} no está eliminado.")
            
            return self._message_repository.restore(message_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar mensaje: {str(e)}")