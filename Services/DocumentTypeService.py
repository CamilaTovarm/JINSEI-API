from Repositories.DocumentTypeRepository import DocumentTypeRepository

class DocumentTypeService:

    def __init__(self):
        self.repo = DocumentTypeRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, doc_id):
        doc = self.repo.get_by_id(doc_id)
        if not doc:
            raise Exception("Tipo de documento no encontrado.")
        return doc

    def create(self, code, description):
        return self.repo.create(code, description)

    def update(self, doc_id, code=None, description=None):
        updated = self.repo.update(doc_id, code, description)
        if not updated:
            raise Exception("Tipo de documento no encontrado.")
        return updated

    def delete(self, doc_id):
        deleted = self.repo.delete(doc_id)
        if not deleted:
            raise Exception("Tipo de documento no encontrado.")
        return True
