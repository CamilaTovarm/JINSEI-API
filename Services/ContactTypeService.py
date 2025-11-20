from Repositories.ContactTypeRepository import ContactTypeRepository
from sqlalchemy.exc import SQLAlchemyError

class ContactTypeService:
    def __init__(self):
        self._contact_type_repository = ContactTypeRepository()

    def get_all_contact_types(self, include_deleted=False):

        try:
            return self._contact_type_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener tipos de contacto: {str(e)}")

    def get_contact_type_by_id(self, contact_type_id, include_deleted=False):

        try:
            contact_type = self._contact_type_repository.get_by_id(contact_type_id, include_deleted=include_deleted)
            if not contact_type:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
            return contact_type
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener tipo de contacto: {str(e)}")

    def create_contact_type(self, description):

        try:
            return self._contact_type_repository.create(description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear tipo de contacto: {str(e)}")

    def update_contact_type(self, contact_type_id, description):

        try:
            # Validar que el tipo de contacto existe
            contact_type = self._contact_type_repository.get_by_id(contact_type_id)
            if not contact_type:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
           
            return self._contact_type_repository.update(contact_type_id, description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar tipo de contacto: {str(e)}")

    def delete_contact_type(self, contact_type_id):

        try:
            contact_type = self._contact_type_repository.get_by_id(contact_type_id)
            if not contact_type:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
        
            return self._contact_type_repository.delete(contact_type_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar tipo de contacto: {str(e)}")
    
    def restore_contact_type(self, contact_type_id):

        try:
            contact_type = self._contact_type_repository.get_by_id(contact_type_id, include_deleted=True)
            if not contact_type:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
            
            if not contact_type.IsDeleted:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no está eliminado.")
            
            return self._contact_type_repository.restore(contact_type_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar tipo de contacto: {str(e)}")