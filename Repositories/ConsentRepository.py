from Models.Consent import Consent
from Models.Database import db

class ConsentRepository:

    def get_all(self):
        return Consent.query.all()

    def get_by_id(self, consent_id):
        return Consent.query.get(consent_id)

    def create(self, session_id, full_name, document_type_id, document_number, consent_version):
        consent = Consent(
            session_id=session_id,
            full_name=full_name,
            document_type_id=document_type_id,
            document_number=document_number,
            consent_version=consent_version
        )
        db.session.add(consent)
        db.session.commit()
        return consent

    def update(self, consent_id, **kwargs):
        consent = self.get_by_id(consent_id)
        if not consent:
            return None
        for key, value in kwargs.items():
            setattr(consent, key, value)
        db.session.commit()
        return consent

    def delete(self, consent_id):
        consent = self.get_by_id(consent_id)
        if not consent:
            return False
        db.session.delete(consent)
        db.session.commit()
        return True
