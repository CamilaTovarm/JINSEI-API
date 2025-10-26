from ConfigDB import db

class ContactType(db.Model):
    __tablename__ = "ContactTypes"

    ContactTypeId = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(100))
    IsDeleted = db.Column(db.Boolean, default=False)

    # Relación bidireccional con Contact
    contacts = db.relationship("Contact", back_populates="contact_type", cascade="all, delete-orphan")