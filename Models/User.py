from ConfigDB import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "Users"

    UserId = db.Column(db.Integer, primary_key=True)
    AKA = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    IsDeleted = db.Column(db.Boolean, default=False)

    sessions = db.relationship("Session", backref="user", cascade="all, delete-orphan")
