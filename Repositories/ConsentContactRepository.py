from ConfigDB import db
from Models.ConsentContact import ConsentContact
from Models.Contact import Contact
from sqlalchemy.exc import SQLAlchemyError

class ConsentContactRepository:
    def __init__(self):
        self.db = db

    def add_contact_to_consent(self, consent_id, contact_id):
        """Asocia un contacto existente a un consentimiento"""
        try:
            # Verificar si ya existe la relación
            existing = ConsentContact.query.filter_by(
                ConsentId=consent_id, 
                ContactId=contact_id
            ).first()
            
            if existing:
                return existing  # Ya existe, no duplicar
            
            link = ConsentContact(ConsentId=consent_id, ContactId=contact_id)
            self.db.session.add(link)
            self.db.session.commit()
            return link
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def get_contacts_by_consent(self, consent_id):
        """Obtiene todos los contactos vinculados a un consentimiento (solo activos)"""
        return (
            self.db.session.query(Contact)
            .join(ConsentContact, Contact.ContactId == ConsentContact.ContactId)
            .filter(ConsentContact.ConsentId == consent_id)
            .filter(Contact.IsDeleted == False)
            .all()
        )
    
    def get_consents_by_contact(self, contact_id):
        """Obtiene todos los consentimientos vinculados a un contacto"""
        from Models.Consent import Consent
        return (
            self.db.session.query(Consent)
            .join(ConsentContact, Consent.ConsentId == ConsentContact.ConsentId)
            .filter(ConsentContact.ContactId == contact_id)
            .filter(Consent.IsDeleted == False)
            .all()
        )
    
    def remove_contact_from_consent(self, consent_id, contact_id):
        """Elimina la relación entre un consentimiento y un contacto"""
        try:
            link = ConsentContact.query.filter_by(
                ConsentId=consent_id, 
                ContactId=contact_id
            ).first()
            
            if not link:
                return None
            
            self.db.session.delete(link)
            self.db.session.commit()
            return True
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e