from ConfigDB import db

class ConsentContact(db.Model):
    __tablename__ = "ConsentContacts"

    ConsentId = db.Column(db.Integer, db.ForeignKey("Consents.ConsentId"), primary_key=True)
    ContactId = db.Column(db.Integer, db.ForeignKey("Contacts.ContactId"), primary_key=True)