from Models.Database import db

class RiskLevel(db.Model):
    __tablename__ = "RiskLevels"

    RiskLevelId = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))

