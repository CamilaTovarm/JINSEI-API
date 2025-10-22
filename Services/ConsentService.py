from Repositories.ConsentRepository import ConsentRepository
from Repositories.ContactRepository import ContactRepository
from Repositories.ConsentContactRepository import ConsentContactRepository
from Models.Consent import Consent
from sqlalchemy.exc import SQLAlchemyError

class ConsentService:
    def __init__(self):
        self._consent_repository = ConsentRepository()
        self._contact_repository = ContactRepository()
        self._consent_contact_repository = ConsentContactRepository()

    def get_all_consents(self):
        return self._consent_repository.get_all()

    def get_consent_by_id(self, consent_id):
        return self._consent_repository.get_by_id(consent_id)

    def create_consent(self, session_id, full_name, document_type_id, document_number, email, phone):
        try:
            # 1️⃣ Crear el consentimiento base
            new_consent = Consent(
                SessionId=session_id,
                FullName=full_name,
                DocumentTypeId=document_type_id,
                DocumentNumber=document_number,
                IsDeleted=False
            )
            self._consent_repository.create_entity(new_consent)

            # 2️⃣ Crear los contactos: correo y teléfono
            # (Nota: aquí los ContactTypeId deben coincidir con los definidos en tu tabla ContactTypes)
            email_contact = self._contact_repository.create(contact_type_id=1, description=email)
            phone_contact = self._contact_repository.create(contact_type_id=2, description=phone)

            # 3️⃣ Asociar ambos contactos con el consentimiento en la tabla intermedia
            self._consent_contact_repository.create(new_consent.ConsentId, email_contact.ContactId)
            self._consent_contact_repository.create(new_consent.ConsentId, phone_contact.ContactId)

            return new_consent

        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
        except Exception as e:
            raise Exception(f"Error creating consent: {str(e)}")

    def update_consent(self, consent_id, session_id=None, full_name=None, document_type_id=None, document_number=None):
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

        return self._consent_repository.update(consent)

    def delete_consent(self, consent_id):
        consent_to_delete = self._consent_repository.get_by_id(consent_id)
        if not consent_to_delete:
            raise Exception(f"The consent with ID {consent_id} doesn't exist.")

        consent_to_delete.IsDeleted = True
        return self._consent_repository.delete(consent_to_delete)
