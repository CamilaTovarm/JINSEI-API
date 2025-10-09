# repositories/message_repository.py
from ConfigDB import db
from Models.Message import Message
from sqlalchemy.exc import SQLAlchemyError

class MessageRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return Message.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, message_id):
        return Message.query.filter_by(MessageId=message_id, IsDeleted=False).first()

    def create(self, session_id, bot_message, user_response=None, risk_level_id=None, risk_percent=None):
        try:
            new_message = Message(
                SessionId=session_id,
                BotMessage=bot_message,
                UserResponse=user_response,
                RiskLevelId=risk_level_id,
                RiskPercent=risk_percent,
                IsDeleted=False
            )
            self.db.session.add(new_message)
            self.db.session.commit()
            return new_message
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, message):
        """
        message: instancia models.message.Message (con MessageId)
        """
        existing = Message.query.get(message.MessageId)
        if not existing or existing.IsDeleted:
            return None
        existing.BotMessage = message.BotMessage
        existing.UserResponse = message.UserResponse
        existing.RiskLevelId = message.RiskLevelId
        existing.RiskPercent = message.RiskPercent
        self.db.session.commit()
        return existing

    def delete(self, message):
        message.IsDeleted = True
        self.db.session.commit()
        return message
