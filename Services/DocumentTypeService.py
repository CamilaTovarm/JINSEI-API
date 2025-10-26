from Repositories.DocumentTypeRepository import DocumentTypeRepository
from sqlalchemy.exc import SQLAlchemyError

class DocumentTypeService:
    def __init__(self):
        self._document_type_repository = DocumentTypeRepository()

    def get_all_document_types(self, include_deleted=False):
        """Obtiene todos los tipos de documento"""
        try:
            return self._document_type_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener tipos de documento: {str(e)}")

    def get_document_type_by_id(self, document_type_id, include_deleted=False):
        """Obtiene un tipo de documento por ID"""
        try:
            document_type = self._document_type_repository.get_by_id(document_type_id, include_deleted=include_deleted)
            if not document_type:
                raise Exception(f"El tipo de documento con ID {document_type_id} no existe.")
            return document_type
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener tipo de documento: {str(e)}")

    def create_document_type(self, description):
        """Crea un nuevo tipo de documento"""
        try:
            return self._document_type_repository.create(description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear tipo de documento: {str(e)}")

    def update_document_type(self, document_type_id, description):
        """Actualiza un tipo de documento existente"""
        try:
            # Validar que el tipo de documento existe
            document_type = self._document_type_repository.get_by_id(document_type_id)
            if not document_type:
                raise Exception(f"El tipo de documento con ID {document_type_id} no existe.")
            
            # ✅ Ahora pasamos los parámetros directamente
            return self._document_type_repository.update(document_type_id, description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar tipo de documento: {str(e)}")

    def delete_document_type(self, document_type_id):
        """Marca un tipo de documento como eliminado (soft delete)"""
        try:
            document_type = self._document_type_repository.get_by_id(document_type_id)
            if not document_type:
                raise Exception(f"El tipo de documento con ID {document_type_id} no existe.")
            
            # ✅ Solo pasamos el ID
            return self._document_type_repository.delete(document_type_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar tipo de documento: {str(e)}")
    
    def restore_document_type(self, document_type_id):
        """Restaura un tipo de documento marcado como eliminado"""
        try:
            document_type = self._document_type_repository.get_by_id(document_type_id, include_deleted=True)
            if not document_type:
                raise Exception(f"El tipo de documento con ID {document_type_id} no existe.")
            
            if not document_type.IsDeleted:
                raise Exception(f"El tipo de documento con ID {document_type_id} no está eliminado.")
            
            return self._document_type_repository.restore(document_type_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar tipo de documento: {str(e)}")