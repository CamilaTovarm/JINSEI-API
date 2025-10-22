from ConfigDB import db
from Models.ConsentContact import ConsentContact
from sqlalchemy.exc import SQLAlchemyError

class ConsentContactRepository:
    def __init__(self):
        self.db = db

    def add_contact_to_consent(self, consent_id, contact_id):
        """
        Asocia un contacto existente a un consentimiento.
        """
        try:
            link = ConsentContact(ConsentId=consent_id, ContactId=contact_id)
            self.db.session.add(link)
            self.db.session.commit()
            return link
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def get_contacts_by_consent(self, consent_id):
        """
        Obtiene todos los contactos vinculados a un consentimiento.
        """
        return ConsentContact.query.filter_by(ConsentId=consent_id).all()

