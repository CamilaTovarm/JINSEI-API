from Repositories.ContactRepository import ContactRepository

class ContactService:

    def __init__(self):
        self.repo = ContactRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, contact_id):
        contact = self.repo.get_by_id(contact_id)
        if not contact:
            raise Exception("Contacto no encontrado.")
        return contact

    def create(self, consent_id, contact_type_id, contact_value):
        return self.repo.create(consent_id, contact_type_id, contact_value)

    def update(self, contact_id, **kwargs):
        updated = self.repo.update(contact_id, **kwargs)
        if not updated:
            raise Exception("Contacto no encontrado.")
        return updated

    def delete(self, contact_id):
        deleted = self.repo.delete(contact_id)
        if not deleted:
            raise Exception("Contacto no encontrado.")
        return True
