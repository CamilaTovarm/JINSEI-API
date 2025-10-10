from Repositories.ContactRepository import ContactRepository

class ContactService:
    def __init__(self):
        self._contact_repository = ContactRepository()

    def get_all_contacts(self):
        return self._contact_repository.get_all()

    def get_contact_by_id(self, contact_id):
        return self._contact_repository.get_by_id(contact_id)

    def create_contact(self, contact_type_id, description):
        return self._contact_repository.create(contact_type_id, description)

    def update_contact(self, contact_id, contact_type_id=None, description=None):
        contact = self._contact_repository.get_by_id(contact_id)
        if not contact:
            raise Exception(f"The contact with ID {contact_id} doesn't exist.")

        if contact_type_id is not None:
            contact.ContactTypeId = contact_type_id
        if description is not None:
            contact.Description = description

        return self._contact_repository.update(contact)

    def delete_contact(self, contact_id):
        contact_to_delete = self._contact_repository.get_by_id(contact_id)
        if not contact_to_delete:
            raise Exception(f"The contact with ID {contact_id} doesn't exist.")

        contact_to_delete.IsDeleted = True
        return self._contact_repository.delete(contact_to_delete)
