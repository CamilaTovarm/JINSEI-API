from Repositories.ContactTypeRepository import ContactTypeRepository

class ContactTypeService:
    def __init__(self):
        self._contact_type_repository = ContactTypeRepository()

    def get_all_contact_types(self):
        return self._contact_type_repository.get_all()

    def get_contact_type_by_id(self, contact_type_id):
        return self._contact_type_repository.get_by_id(contact_type_id)

    def create_contact_type(self, description):
        return self._contact_type_repository.create(description)

    def update_contact_type(self, contact_type_id, description=None):
        contact_type = self._contact_type_repository.get_by_id(contact_type_id)
        if not contact_type:
            raise Exception(f"The contact type with ID {contact_type_id} doesn't exist.")

        if description is not None:
            contact_type.Description = description

        return self._contact_type_repository.update(contact_type)

    def delete_contact_type(self, contact_type_id):
        contact_type_to_delete = self._contact_type_repository.get_by_id(contact_type_id)
        if not contact_type_to_delete:
            raise Exception(f"The contact type with ID {contact_type_id} doesn't exist.")

        contact_type_to_delete.IsDeleted = True
        return self._contact_type_repository.delete(contact_type_to_delete)
