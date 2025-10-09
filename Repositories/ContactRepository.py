# repositories/contact_repository.py
from ConfigDB import db
from Models.Contact import Contact
from sqlalchemy.exc import SQLAlchemyError

class ContactRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return Contact.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, contact_id):
        return Contact.query.filter_by(ContactId=contact_id, IsDeleted=False).first()

    def create(self, contact_type_id, description):
        try:
            new_contact = Contact(
                ContactTypeId=contact_type_id,
                Description=description,
                IsDeleted=False
            )
            self.db.session.add(new_contact)
            self.db.session.commit()
            return new_contact
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, contact):
        existing = Contact.query.get(contact.ContactId)
        if not existing or existing.IsDeleted:
            return None
        existing.ContactTypeId = contact.ContactTypeId
        existing.Description = contact.Description
        self.db.session.commit()
        return existing

    def delete(self, contact):
        contact.IsDeleted = True
        self.db.session.commit()
        return contact
