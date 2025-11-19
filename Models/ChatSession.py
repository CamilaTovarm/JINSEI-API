from ConfigDB import db
from datetime import datetime

class ChatSession(db.Model):
    __tablename__ = "Sessions"

    SessionId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey("Users.UserId"), nullable=False)
    StartTime = db.Column(db.DateTime, default=datetime.utcnow)
    EndTime = db.Column(db.DateTime)
    RiskLevelId = db.Column(db.Integer, db.ForeignKey("RiskLevels.RiskLevelId"))
    FinalRiskLevel = db.Column(db.Float)
    IsDeleted = db.Column(db.Boolean, default=False)

    # Relaciones bidireccionales
    messages = db.relationship("Message", back_populates="chat_session", cascade="all, delete-orphan")
    consents = db.relationship("Consent", back_populates="chat_session", cascade="all, delete-orphan")
    risk_level = db.relationship("RiskLevel", back_populates="chat_sessions")
    user = db.relationship("User", back_populates="chat_sessions")