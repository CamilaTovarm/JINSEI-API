from models.database import db
from datetime import datetime

class Consent(db.Model):
    __tablename__ = "Consents"

    ConsentId = db.Column(db.Integer, primary_key=True)
    SessionId = db.Column(db.Integer, db.ForeignKey("Sessions.SessionId"), nullable=False)
    FullName = db.Column(db.String(150), nullable=False)
    DocumentTypeId = db.Column(db.Integer, db.ForeignKey("DocumentTypes.DocumentTypeId"), nullable=False)
    DocumentNumber = db.Column(db.String(30), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

    Contacts = db.relationship("Contact", backref="Consent", cascade="all, delete-orphan")
