from ConfigDB import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = "Contacts"

    ContactId = db.Column(db.Integer, primary_key=True)
    ContactTypeId = db.Column(db.Integer, db.ForeignKey("ContactTypes.ContactTypeId"), nullable=False)
    Description = db.Column(db.String(120), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)
    IsDeleted = db.Column(db.Boolean, default=False)

    ContactType = db.relationship("ContactType", back_populates="Contacts")
     # Relación muchos a muchos con Consent
    Consents = db.relationship("Consent", secondary="ConsentContacts",back_populates="Contacts")
