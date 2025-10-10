from Repositories.MessageRepository import MessageRepository

class MessageService:
    def __init__(self):
        self._message_repository = MessageRepository()

    def get_all_messages(self):
        return self._message_repository.get_all()

    def get_message_by_id(self, message_id):
        return self._message_repository.get_by_id(message_id)

    def create_message(self, session_id, bot_message, user_response, risk_level_id=None, risk_percent=None):
        return self._message_repository.create(session_id, bot_message, user_response, risk_level_id, risk_percent)

    def update_message(self, message_id, session_id=None, bot_message=None, user_response=None, risk_level_id=None, risk_percent=None):
        message = self._message_repository.get_by_id(message_id)
        if not message:
            raise Exception(f"The message with ID {message_id} doesn't exist.")

        if session_id is not None:
            message.SessionId = session_id
        if bot_message is not None:
            message.BotMessage = bot_message
        if user_response is not None:
            message.UserResponse = user_response
        if risk_level_id is not None:
            message.RiskLevelId = risk_level_id
        if risk_percent is not None:
            message.RiskPercent = risk_percent

        return self._message_repository.update(message)

    def delete_message(self, message_id):
        message_to_delete = self._message_repository.get_by_id(message_id)
        if not message_to_delete:
            raise Exception(f"The message with ID {message_id} doesn't exist.")

        message_to_delete.IsDeleted = True
        return self._message_repository.delete(message_to_delete)
