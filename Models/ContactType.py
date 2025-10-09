from ConfigDB import db

class ContactType(db.Model):
    __tablename__ = "ContactTypes"

    ContactTypeId = db.Column(db.Integer, primary_key=True)
    Description = db.Column(db.String(100))
    IsDeleted = db.Column(db.Boolean, default=False)

    Contacts = db.relationship("Contact", backref="ContactType", cascade="all, delete-orphan")
