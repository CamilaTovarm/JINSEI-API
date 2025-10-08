from Models.Database import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "Messages"

    MessageId = db.Column(db.Integer, primary_key=True)
    SessionId = db.Column(db.Integer, db.ForeignKey("sessions.session_id"), nullable=False)
    BotMessage = db.Column(db.Text, nullable=False)
    UserResponse = db.Column(db.Text)
    RiskLevelId = db.Column(db.Integer, db.ForeignKey("risk_levels.risk_level_id"))
    RiskPercent = db.Column(db.Float)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
