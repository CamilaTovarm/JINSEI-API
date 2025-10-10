# repositories/session_repository.py
from ConfigDB import db
from Models.ChatSession import ChatSession
from sqlalchemy.exc import SQLAlchemyError

class SessionRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return ChatSession.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, session_id):
        return ChatSession.query.filter_by(SessionId=session_id, IsDeleted=False).first()

    def create(self, user_id, start_time, end_time=None, risk_level_id=None, final_risk_level=None):
        try:
            new_ChatSession = ChatSession(
                UserId=user_id,
                StartTime=start_time,
                EndTime=end_time,
                RiskLevelId=risk_level_id,
                FinalRiskLevel=final_risk_level,
                IsDeleted=False
            )
            self.db.session.add(new_ChatSession)
            self.db.session.commit()
            return new_ChatSession
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, chatSession):
        existing = ChatSession.query.get(chatSession.SessionId)
        if not existing or existing.IsDeleted:
            return None

        existing.UserId = chatSession.UserId
        existing.StartTime = chatSession.StartTime
        existing.EndTime = chatSession.EndTime
        existing.RiskLevelId = chatSession.RiskLevelId
        existing.FinalRiskLevel = chatSession.FinalRiskLevel

        self.db.session.commit()
        return existing

    def delete(self, chatSession):
        try:
            self.db.session.add(chatSession)
            self.db.session.commit()
            return chatSession
        except SQLAlchemyError:
            self.db.session.rollback()
            raise
