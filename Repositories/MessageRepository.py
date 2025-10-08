from Models.Message import Message
from Models.Database import db

class MessageRepository:

    def get_all(self):
        return Message.query.all()

    def get_by_id(self, message_id):
        return Message.query.get(message_id)

    def create(self, session_id, bot_message, user_response, risk_level_id=None, risk_label=None, risk_score=None):
        message = Message(
            session_id=session_id,
            bot_message=bot_message,
            user_response=user_response,
            risk_level_id=risk_level_id,
            risk_label=risk_label,
            risk_score=risk_score
        )
        db.session.add(message)
        db.session.commit()
        return message

    def update(self, message_id, **kwargs):
        message = self.get_by_id(message_id)
        if not message:
            return None
        for key, value in kwargs.items():
            setattr(message, key, value)
        db.session.commit()
        return message

    def delete(self, message_id):
        message = self.get_by_id(message_id)
        if not message:
            return False
        db.session.delete(message)
        db.session.commit()
        return True
