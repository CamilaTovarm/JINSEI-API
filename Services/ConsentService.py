from Repositories.ConsentRepository import ConsentRepository

class ConsentService:
    def __init__(self):
        self._consent_repository = ConsentRepository()

    def get_all_consents(self):
        return self._consent_repository.get_all()

    def get_consent_by_id(self, consent_id):
        return self._consent_repository.get_by_id(consent_id)

    def create_consent(self, session_id, full_name, document_type_id, document_number, contact_id):
        return self._consent_repository.create(session_id, full_name, document_type_id, document_number, contact_id)

    def update_consent(self, consent_id, session_id=None, full_name=None, document_type_id=None, document_number=None, contact_id=None):
        consent = self._consent_repository.get_by_id(consent_id)
        if not consent:
            raise Exception(f"The consent with ID {consent_id} doesn't exist.")

        if session_id is not None:
            consent.SessionId = session_id
        if full_name is not None:
            consent.FullName = full_name
        if document_type_id is not None:
            consent.DocumentTypeId = document_type_id
        if document_number is not None:
            consent.DocumentNumber = document_number
        if contact_id is not None:
            consent.ContactId = contact_id

        return self._consent_repository.update(consent)

    def delete_consent(self, consent_id):
        consent_to_delete = self._consent_repository.get_by_id(consent_id)
        if not consent_to_delete:
            raise Exception(f"The consent with ID {consent_id} doesn't exist.")
        consent_to_delete.IsDeleted = True
        return self._consent_repository.delete(consent_to_delete)
