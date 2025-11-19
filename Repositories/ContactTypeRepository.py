from ConfigDB import db
from Models.ContactType import ContactType
from sqlalchemy.exc import SQLAlchemyError

class ContactTypeRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):
        """Obtiene todos los tipos de contacto"""
        if include_deleted:
            return ContactType.query.all()
        return ContactType.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, contact_type_id, include_deleted=False):
        """Obtiene un tipo de contacto por ID"""
        if include_deleted:
            return ContactType.query.filter_by(ContactTypeId=contact_type_id).first()
        return ContactType.query.filter_by(ContactTypeId=contact_type_id, IsDeleted=False).first()

    def create(self, description):
        """Crea un nuevo tipo de contacto"""
        try:
            new_contact_type = ContactType(Description=description, IsDeleted=False)
            self.db.session.add(new_contact_type)
            self.db.session.commit()
            return new_contact_type
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, contact_type_id, description):
        """Actualiza un tipo de contacto existente"""
        try:
            existing = ContactType.query.get(contact_type_id)
            if not existing or existing.IsDeleted:
                return None
            
            existing.Description = description
            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, contact_type_id):
        """Marca un tipo de contacto como eliminado (soft delete)"""
        try:
            contact_type = ContactType.query.get(contact_type_id)
            if not contact_type:
                return None
            
            contact_type.IsDeleted = True
            self.db.session.commit()
            return contact_type
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, contact_type_id):
        """Restaura un tipo de contacto marcado como eliminado"""
        try:
            contact_type = ContactType.query.get(contact_type_id)
            if not contact_type:
                return None
            
            contact_type.IsDeleted = False
            self.db.session.commit()
            return contact_type
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e