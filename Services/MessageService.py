from Repositories.MessageRepository import MessageRepository

class MessageService:

    def __init__(self):
        self.repo = MessageRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, message_id):
        msg = self.repo.get_by_id(message_id)
        if not msg:
            raise Exception("Mensaje no encontrado.")
        return msg

    def create(self, session_id, bot_message, user_response, risk_level_id=None, risk_label=None, risk_score=None):
        return self.repo.create(session_id, bot_message, user_response, risk_level_id, risk_label, risk_score)

    def update(self, message_id, **kwargs):
        updated = self.repo.update(message_id, **kwargs)
        if not updated:
            raise Exception("Mensaje no encontrado para actualizar.")
        return updated

    def delete(self, message_id):
        deleted = self.repo.delete(message_id)
        if not deleted:
            raise Exception("Mensaje no encontrado para eliminar.")
        return True
