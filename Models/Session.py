from models.database import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = "Sessions"

    SeessionId = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    StartTime = db.Column(db.DateTime, default=datetime.utcnow)
    EndTime = db.Column(db.DateTime)
    RiskDetected = db.Column(db.Boolean, default=False)
    RiskLevel = db.Column(db.String(30))

    messages = db.relationship("Message", backref="Session", cascade="all, delete-orphan")
    consents = db.relationship("Consent", backref="Session", cascade="all, delete-orphan")
