from Repositories.ContactRepository import ContactRepository
from Repositories.ContactTypeRepository import ContactTypeRepository
from sqlalchemy.exc import SQLAlchemyError
import re

class ContactService:
    def __init__(self):
        self._contact_repository = ContactRepository()
        self._contact_type_repository = ContactTypeRepository()

    def get_all_contacts(self, include_deleted=False):

        try:
            return self._contact_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener contactos: {str(e)}")

    def get_contact_by_id(self, contact_id, include_deleted=False):

        try:
            contact = self._contact_repository.get_by_id(contact_id, include_deleted=include_deleted)
            if not contact:
                raise Exception(f"El contacto con ID {contact_id} no existe.")
            return contact
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener contacto: {str(e)}")
    
    def get_contacts_by_type(self, contact_type_id, include_deleted=False):

        try:
            contact_type = self._contact_type_repository.get_by_id(contact_type_id)
            if not contact_type:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
            
            return self._contact_repository.get_by_type(contact_type_id, include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener contactos por tipo: {str(e)}")

    def _validate_contact_value(self, contact_type_id, value):

        EMAIL_TYPE_ID = 1
        PHONE_TYPE_ID = 2
        
        if contact_type_id == EMAIL_TYPE_ID:
            # Validar email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, value):
                raise Exception(f"El email '{value}' no tiene un formato válido.")
        
        elif contact_type_id == PHONE_TYPE_ID:
            # Validar teléfono
            phone_clean = re.sub(r'[\s\-\(\)\+]', '', value)
            if not phone_clean.isdigit() or len(phone_clean) < 7 or len(phone_clean) > 15:
                raise Exception(f"El teléfono '{value}' no tiene un formato válido.")

    def create_contact(self, contact_type_id, value):

        try:
            # Validar que el tipo de contacto existe
            contact_type = self._contact_type_repository.get_by_id(contact_type_id)
            if not contact_type:
                raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
            
            # Validar el formato del valor según el tipo
            self._validate_contact_value(contact_type_id, value)
            
            # Crear el contacto
            return self._contact_repository.create(contact_type_id, value)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear contacto: {str(e)}")

    def update_contact(self, contact_id, contact_type_id=None, value=None):

        try:
            # Validar que el contacto existe
            contact = self._contact_repository.get_by_id(contact_id)
            if not contact:
                raise Exception(f"El contacto con ID {contact_id} no existe.")
            
            update_data = {}
            
            # Si se cambia el tipo de contacto
            if contact_type_id is not None:
                contact_type = self._contact_type_repository.get_by_id(contact_type_id)
                if not contact_type:
                    raise Exception(f"El tipo de contacto con ID {contact_type_id} no existe.")
                update_data['ContactTypeId'] = contact_type_id
            
            # Si se cambia el valor
            if value is not None:
                # Validar según el tipo (el actual o el nuevo)
                type_to_validate = contact_type_id if contact_type_id is not None else contact.ContactTypeId
                self._validate_contact_value(type_to_validate, value)
                update_data['Description'] = value
            
            return self._contact_repository.update(contact_id, **update_data)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar contacto: {str(e)}")

    def delete_contact(self, contact_id):

        try:
            contact = self._contact_repository.get_by_id(contact_id)
            if not contact:
                raise Exception(f"El contacto con ID {contact_id} no existe.")
            
            return self._contact_repository.delete(contact_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar contacto: {str(e)}")
    
    def restore_contact(self, contact_id):

        try:
            contact = self._contact_repository.get_by_id(contact_id, include_deleted=True)
            if not contact:
                raise Exception(f"El contacto con ID {contact_id} no existe.")
            
            if not contact.IsDeleted:
                raise Exception(f"El contacto con ID {contact_id} no está eliminado.")
            
            return self._contact_repository.restore(contact_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar contacto: {str(e)}")