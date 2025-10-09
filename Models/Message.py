from ConfigDB import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = "Messages"

    MessageId = db.Column(db.Integer, primary_key=True)
    SessionId = db.Column(db.Integer, db.ForeignKey("Sessions.SessionId"), nullable=False)
    BotMessage = db.Column(db.Text, nullable=False)
    UserResponse = db.Column(db.Text)
    RiskLevelId = db.Column(db.Integer, db.ForeignKey("RiskLevels.RiskLevelId"))
    RiskPercent = db.Column(db.Float)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    IsDeleted = db.Column(db.Boolean, default=False)

    RiskLevel = db.relationship("RiskLevel", backref="Messages")
    Session = db.relationship("Session", backref="Messages")