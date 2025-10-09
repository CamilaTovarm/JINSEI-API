# repositories/consent_repository.py
from ConfigDB import db
from Models.Consent import Consent
from sqlalchemy.exc import SQLAlchemyError

class ConsentRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return Consent.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, consent_id):
        return Consent.query.filter_by(ConsentId=consent_id, IsDeleted=False).first()

    def create(self, session_id, full_name, document_type_id, document_number, contact_id=None):
        try:
            new_consent = Consent(
                SessionId=session_id,
                FullName=full_name,
                DocumentTypeId=document_type_id,
                DocumentNumber=document_number,
                ContactId=contact_id,
                IsDeleted=False
            )
            self.db.session.add(new_consent)
            self.db.session.commit()
            return new_consent
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, consent):
        existing = Consent.query.get(consent.ConsentId)
        if not existing or existing.IsDeleted:
            return None
        existing.FullName = consent.FullName
        existing.DocumentTypeId = consent.DocumentTypeId
        existing.DocumentNumber = consent.DocumentNumber
        existing.ContactId = consent.ContactId
        self.db.session.commit()
        return existing

    def delete(self, consent):
        consent.IsDeleted = True
        self.db.session.commit()
        return consent
