from ConfigDB import db
from Models.Consent import Consent
from sqlalchemy.exc import SQLAlchemyError

class ConsentRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):

        if include_deleted:
            return Consent.query.all()
        return Consent.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, consent_id, include_deleted=False):

        if include_deleted:
            return Consent.query.filter_by(ConsentId=consent_id).first()
        return Consent.query.filter_by(ConsentId=consent_id, IsDeleted=False).first()
    
    def get_by_session_id(self, session_id, include_deleted=False):

        query = Consent.query.filter_by(SessionId=session_id)
        if not include_deleted:
            query = query.filter_by(IsDeleted=False)
        return query.all()
    
    def get_by_document(self, document_type_id, document_number, include_deleted=False):

        query = Consent.query.filter_by(
            DocumentTypeId=document_type_id,
            DocumentNumber=document_number
        )
        if not include_deleted:
            query = query.filter_by(IsDeleted=False)
        return query.first()

    def create(self, session_id, full_name, document_type_id, document_number):

        try:
            new_consent = Consent(
                SessionId=session_id,
                FullName=full_name,
                DocumentTypeId=document_type_id,
                DocumentNumber=document_number,
                IsDeleted=False
            )
            self.db.session.add(new_consent)
            self.db.session.commit()
            return new_consent
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, consent_id, **kwargs):

        try:
            existing = Consent.query.get(consent_id)
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

    def delete(self, consent_id):

        try:
            consent = Consent.query.get(consent_id)
            if not consent:
                return None
            
            consent.IsDeleted = True
            self.db.session.commit()
            return consent
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, consent_id):

        try:
            consent = Consent.query.get(consent_id)
            if not consent:
                return None
            
            consent.IsDeleted = False
            self.db.session.commit()
            return consent
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e