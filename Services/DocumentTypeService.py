from Repositories.DocumentTypeRepository import DocumentTypeRepository

class DocumentTypeService:
    def __init__(self):
        self._document_type_repository = DocumentTypeRepository()

    def get_all_document_types(self):
        return self._document_type_repository.get_all()

    def get_document_type_by_id(self, document_type_id):
        return self._document_type_repository.get_by_id(document_type_id)

    def create_document_type(self, description):
        return self._document_type_repository.create(description)

    def update_document_type(self, document_type_id, description=None):
        document_type = self._document_type_repository.get_by_id(document_type_id)
        if not document_type:
            raise Exception(f"The document type with ID {document_type_id} doesn't exist.")
        if description is not None:
            document_type.Description = description
        return self._document_type_repository.update(document_type)

    def delete_document_type(self, document_type_id):
        document_type_to_delete = self._document_type_repository.get_by_id(document_type_id)
        if not document_type_to_delete:
            raise Exception(f"The document type with ID {document_type_id} doesn't exist.")
        document_type_to_delete.IsDeleted = True
        return self._document_type_repository.delete(document_type_to_delete)
