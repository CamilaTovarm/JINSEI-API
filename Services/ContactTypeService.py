from Repositories.ContactTypeRepository import ContactTypeRepository

class ContactTypeService:

    def __init__(self):
        self.repo = ContactTypeRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, type_id):
        ct = self.repo.get_by_id(type_id)
        if not ct:
            raise Exception("Tipo de contacto no encontrado.")
        return ct

    def create(self, name, description):
        return self.repo.create(name, description)

    def update(self, type_id, name=None, description=None):
        updated = self.repo.update(type_id, name, description)
        if not updated:
            raise Exception("Tipo de contacto no encontrado.")
        return updated

    def delete(self, type_id):
        deleted = self.repo.delete(type_id)
        if not deleted:
            raise Exception("Tipo de contacto no encontrado.")
        return True
