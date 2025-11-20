from ConfigDB import db
from Models.ChatSession import ChatSession
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

class SessionRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):

        if include_deleted:
            return ChatSession.query.all()
        return ChatSession.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, session_id, include_deleted=False):

        if include_deleted:
            return ChatSession.query.filter_by(SessionId=session_id).first()
        return ChatSession.query.filter_by(SessionId=session_id, IsDeleted=False).first()
    
    def get_by_user_id(self, user_id, include_deleted=False):

        query = ChatSession.query.filter_by(UserId=user_id)
        if not include_deleted:
            query = query.filter_by(IsDeleted=False)
        return query.order_by(ChatSession.StartTime.desc()).all()
    
    def get_active_session(self, user_id):

        return ChatSession.query.filter_by(
            UserId=user_id,
            EndTime=None,
            IsDeleted=False
        ).first()

    def create(self, user_id, start_time=None, end_time=None, risk_level_id=None, final_risk_level=None):

        try:
            new_chat_session = ChatSession(
                UserId=user_id,
                StartTime=start_time or datetime.utcnow(),
                EndTime=end_time,
                RiskLevelId=risk_level_id,
                FinalRiskLevel=final_risk_level,
                IsDeleted=False
            )
            self.db.session.add(new_chat_session)
            self.db.session.commit()
            return new_chat_session
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, session_id, **kwargs):

        try:
            existing = ChatSession.query.get(session_id)
            if not existing or existing.IsDeleted:
                return None
             
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)

            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def end_session(self, session_id, final_risk_level=None):

        try:
            session = ChatSession.query.get(session_id)
            if not session or session.IsDeleted:
                return None
            
            session.EndTime = datetime.utcnow()
            if final_risk_level:
                session.FinalRiskLevel = final_risk_level
            
            self.db.session.commit()
            return session
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, session_id):

        try:
            chat_session = ChatSession.query.get(session_id)
            if not chat_session:
                return None
            
            chat_session.IsDeleted = True
            self.db.session.commit()
            return chat_session
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, session_id):

        try:
            chat_session = ChatSession.query.get(session_id)
            if not chat_session:
                return None
            
            chat_session.IsDeleted = False
            self.db.session.commit()
            return chat_session
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e