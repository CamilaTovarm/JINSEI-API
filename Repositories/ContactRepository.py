from Models.Contact import Contact
from Models.Database import db

class ContactRepository:

    def get_all(self):
        return Contact.query.all()

    def get_by_id(self, contact_id):
        return Contact.query.get(contact_id)

    def create(self, consent_id, contact_type_id, contact_value):
        contact = Contact(
            consent_id=consent_id,
            contact_type_id=contact_type_id,
            contact_value=contact_value
        )
        db.session.add(contact)
        db.session.commit()
        return contact

    def update(self, contact_id, **kwargs):
        contact = self.get_by_id(contact_id)
        if not contact:
            return None
        for key, value in kwargs.items():
            setattr(contact, key, value)
        db.session.commit()
        return contact

    def delete(self, contact_id):
        contact = self.get_by_id(contact_id)
        if not contact:
            return False
        db.session.delete(contact)
        db.session.commit()
        return True
