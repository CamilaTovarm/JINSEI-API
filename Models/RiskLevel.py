from ConfigDB import db

class RiskLevel(db.Model):
    __tablename__ = "RiskLevels"

    RiskLevelId = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    IsDeleted = db.Column(db.Boolean, default=False)


    Sessions = db.relationship("Session", backref="RiskLevel", cascade="all, delete-orphan")
    Messages = db.relationship("Message", backref="RiskLevel", cascade="all, delete-orphan")