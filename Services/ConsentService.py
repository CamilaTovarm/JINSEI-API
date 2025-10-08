from Repositories.ConsentRepository import ConsentRepository

class ConsentService:

    def __init__(self):
        self.repo = ConsentRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, consent_id):
        consent = self.repo.get_by_id(consent_id)
        if not consent:
            raise Exception("Consentimiento no encontrado.")
        return consent

    def create(self, session_id, full_name, document_type_id, document_number, consent_version):
        return self.repo.create(session_id, full_name, document_type_id, document_number, consent_version)

    def update(self, consent_id, **kwargs):
        updated = self.repo.update(consent_id, **kwargs)
        if not updated:
            raise Exception("Consentimiento no encontrado.")
        return updated

    def delete(self, consent_id):
        deleted = self.repo.delete(consent_id)
        if not deleted:
            raise Exception("Consentimiento no encontrado.")
        return True
