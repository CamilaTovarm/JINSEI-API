from ConfigDB import db
from Models.Message import Message
from sqlalchemy.exc import SQLAlchemyError

class MessageRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):

        if include_deleted:
            return Message.query.all()
        return Message.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, message_id, include_deleted=False):

        if include_deleted:
            return Message.query.filter_by(MessageId=message_id).first()
        return Message.query.filter_by(MessageId=message_id, IsDeleted=False).first()
    
    def get_by_session_id(self, session_id, include_deleted=False):

        query = Message.query.filter_by(SessionId=session_id)
        if not include_deleted:
            query = query.filter_by(IsDeleted=False)
        return query.order_by(Message.CreatedAt).all()

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
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, message_id, **kwargs):

        try:
            existing = Message.query.get(message_id)
            if not existing or existing.IsDeleted:
                return None

            # Actualiza solo los campos proporcionados
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, message_id):

        try:
            message = Message.query.get(message_id)
            if not message:
                return None
            
            message.IsDeleted = True
            self.db.session.commit()
            return message
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, message_id):

        try:
            message = Message.query.get(message_id)
            if not message:
                return None
            
            message.IsDeleted = False
            self.db.session.commit()
            return message
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e