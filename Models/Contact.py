from Models.Database import db
from datetime import datetime

class Contact(db.Model):
    __tablename__ = "Contacts"

    ContactId = db.Column(db.Integer, primary_key=True)
    ContactTypeId = db.Column(db.Integer, db.ForeignKey("contact_types.contact_type_id"), nullable=False)
    Description = db.Column(db.String(120), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

