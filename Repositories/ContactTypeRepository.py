# repositories/contacttype_repository.py
from ConfigDB import db
from Models.ContactType import ContactType
from sqlalchemy.exc import SQLAlchemyError

class ContactTypeRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return ContactType.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, contact_type_id):
        return ContactType.query.filter_by(ContactTypeId=contact_type_id, IsDeleted=False).first()

    def create(self, description):
        try:
            new_type = ContactType(Description=description, IsDeleted=False)
            self.db.session.add(new_type)
            self.db.session.commit()
            return new_type
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, contact_type):
        existing = ContactType.query.get(contact_type.ContactTypeId)
        if not existing or existing.IsDeleted:
            return None
        existing.Description = contact_type.Description
        self.db.session.commit()
        return existing

    def delete(self, contact_type):
        contact_type.IsDeleted = True
        self.db.session.commit()
        return contact_type
