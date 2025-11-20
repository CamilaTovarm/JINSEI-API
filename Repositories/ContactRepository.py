from ConfigDB import db
from Models.Contact import Contact
from sqlalchemy.exc import SQLAlchemyError

class ContactRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):

        if include_deleted:
            return Contact.query.all()
        return Contact.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, contact_id, include_deleted=False):

        if include_deleted:
            return Contact.query.filter_by(ContactId=contact_id).first()
        return Contact.query.filter_by(ContactId=contact_id, IsDeleted=False).first()
    
    def get_by_type(self, contact_type_id, include_deleted=False):

        query = Contact.query.filter_by(ContactTypeId=contact_type_id)
        if not include_deleted:
            query = query.filter_by(IsDeleted=False)
        return query.all()

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
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, contact_id, **kwargs):

        try:
            existing = Contact.query.get(contact_id)
            if not existing or existing.IsDeleted:
                return None
        
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            
            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, contact_id):

        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return None
            
            contact.IsDeleted = True
            self.db.session.commit()
            return contact
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, contact_id):

        try:
            contact = Contact.query.get(contact_id)
            if not contact:
                return None
            
            contact.IsDeleted = False
            self.db.session.commit()
            return contact
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e