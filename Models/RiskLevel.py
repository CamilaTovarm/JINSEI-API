from ConfigDB import db

class RiskLevel(db.Model):
    __tablename__ = "RiskLevels"

    RiskLevelId = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    IsDeleted = db.Column(db.Boolean, default=False)
 
    chat_sessions = db.relationship("ChatSession", back_populates="risk_level", cascade="all, delete-orphan")
    messages = db.relationship("Message", back_populates="risk_level", cascade="all, delete-orphan")