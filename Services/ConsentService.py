from Repositories.ConsentRepository import ConsentRepository
from Repositories.ContactRepository import ContactRepository
from Repositories.ConsentContactRepository import ConsentContactRepository
from Repositories.SessionRepository import SessionRepository
from Repositories.DocumentTypeRepository import DocumentTypeRepository
from Repositories.ContactTypeRepository import ContactTypeRepository
from sqlalchemy.exc import SQLAlchemyError
import re

class ConsentService:
    def __init__(self):
        self._consent_repository = ConsentRepository()
        self._contact_repository = ContactRepository()
        self._consent_contact_repository = ConsentContactRepository()
        self._session_repository = SessionRepository()
        self._document_type_repository = DocumentTypeRepository()
        self._contact_type_repository = ContactTypeRepository()

    def get_all_consents(self, include_deleted=False):
        """Obtiene todos los consentimientos"""
        try:
            return self._consent_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener consentimientos: {str(e)}")

    def get_consent_by_id(self, consent_id, include_deleted=False):
        """Obtiene un consentimiento por ID"""
        try:
            consent = self._consent_repository.get_by_id(consent_id, include_deleted=include_deleted)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            return consent
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener consentimiento: {str(e)}")
    
    def get_consents_by_session(self, session_id, include_deleted=False):
        """Obtiene todos los consentimientos de una sesión"""
        try:
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            return self._consent_repository.get_by_session_id(session_id, include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener consentimientos de la sesión: {str(e)}")

    def _validate_email(self, email):
        """Valida formato de email"""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise Exception(f"El email '{email}' no tiene un formato válido.")
    
    def _validate_phone(self, phone):
        """Valida formato de teléfono (básico)"""
        # Acepta números con o sin espacios, guiones, paréntesis y prefijo +
        phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not phone_clean.isdigit() or len(phone_clean) < 7 or len(phone_clean) > 15:
            raise Exception(f"El teléfono '{phone}' no tiene un formato válido.")

    def create_consent(self, session_id, full_name, document_type_id, document_number, email, phone):
        """
        Crea un consentimiento con sus contactos asociados (email y teléfono).
        
        Args:
            session_id: ID de la sesión
            full_name: Nombre completo de la persona
            document_type_id: ID del tipo de documento (ej: 1=CC, 2=TI, etc.)
            document_number: Número del documento
            email: Dirección de correo electrónico (se guarda en Contact.Description)
            phone: Número de teléfono (se guarda en Contact.Description)
        """
        try:
            # 1️⃣ Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            # 2️⃣ Validar que el tipo de documento existe
            doc_type = self._document_type_repository.get_by_id(document_type_id)
            if not doc_type:
                raise Exception(f"El tipo de documento con ID {document_type_id} no existe.")
            
            # 3️⃣ Verificar duplicados por documento
            existing_consent = self._consent_repository.get_by_document(document_type_id, document_number)
            if existing_consent:
                raise Exception(f"Ya existe un consentimiento para el documento {document_number}.")
            
            # 4️⃣ Validar formatos de email y teléfono
            self._validate_email(email)
            self._validate_phone(phone)
            
            # 5️⃣ Verificar que los ContactTypeId existen
            # Asumiendo: ContactTypeId = 1 (Email), ContactTypeId = 2 (Teléfono)
            EMAIL_TYPE_ID = 1
            PHONE_TYPE_ID = 2
            
            email_type = self._contact_type_repository.get_by_id(EMAIL_TYPE_ID)
            if not email_type:
                raise Exception(f"El tipo de contacto Email (ID: {EMAIL_TYPE_ID}) no existe en la base de datos.")
            
            phone_type = self._contact_type_repository.get_by_id(PHONE_TYPE_ID)
            if not phone_type:
                raise Exception(f"El tipo de contacto Teléfono (ID: {PHONE_TYPE_ID}) no existe en la base de datos.")
            
            # 6️⃣ Crear el consentimiento base
            new_consent = self._consent_repository.create(
                session_id=session_id,
                full_name=full_name,
                document_type_id=document_type_id,
                document_number=document_number
            )

            # 7️⃣ Crear los contactos
            # En Contact.Description se guarda el valor real (el email o el teléfono)
            email_contact = self._contact_repository.create(
                contact_type_id=EMAIL_TYPE_ID,
                description=email  # ← Aquí se guarda "usuario@ejemplo.com"
            )
            
            phone_contact = self._contact_repository.create(
                contact_type_id=PHONE_TYPE_ID,
                description=phone  # ← Aquí se guarda "+57 300 123 4567"
            )

            # 8️⃣ Asociar ambos contactos con el consentimiento en la tabla intermedia
            self._consent_contact_repository.add_contact_to_consent(
                new_consent.ConsentId, 
                email_contact.ContactId
            )
            self._consent_contact_repository.add_contact_to_consent(
                new_consent.ConsentId, 
                phone_contact.ContactId
            )

            return new_consent

        except SQLAlchemyError as e:
            raise Exception(f"Error de base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al crear consentimiento: {str(e)}")

    def update_consent(self, consent_id, session_id=None, full_name=None, document_type_id=None, document_number=None):
        """Actualiza un consentimiento existente"""
        try:
            # Validar que el consentimiento existe
            consent = self._consent_repository.get_by_id(consent_id)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            # Construir datos a actualizar
            update_data = {}
            if session_id is not None:
                update_data['SessionId'] = session_id
            if full_name is not None:
                update_data['FullName'] = full_name
            if document_type_id is not None:
                update_data['DocumentTypeId'] = document_type_id
            if document_number is not None:
                update_data['DocumentNumber'] = document_number
            
            return self._consent_repository.update(consent_id, **update_data)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar consentimiento: {str(e)}")
    
    def update_consent_contacts(self, consent_id, email=None, phone=None):
        """
        Actualiza los contactos (email y/o teléfono) de un consentimiento.
        
        Args:
            consent_id: ID del consentimiento
            email: Nuevo email (opcional)
            phone: Nuevo teléfono (opcional)
        """
        try:
            # Validar que el consentimiento existe
            consent = self._consent_repository.get_by_id(consent_id)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            EMAIL_TYPE_ID = 1
            PHONE_TYPE_ID = 2
            
            # Obtener contactos actuales del consentimiento
            current_contacts = self._consent_contact_repository.get_contacts_by_consent(consent_id)
            
            # Actualizar email si se proporciona
            if email is not None:
                self._validate_email(email)
                
                # Buscar el contacto de tipo email
                email_contact = next((c for c in current_contacts if c.ContactTypeId == EMAIL_TYPE_ID), None)
                
                if email_contact:
                    # Actualizar el email existente
                    self._contact_repository.update(
                        contact_id=email_contact.ContactId,
                        Description=email
                    )
                else:
                    # Crear nuevo contacto de email
                    new_email_contact = self._contact_repository.create(
                        contact_type_id=EMAIL_TYPE_ID,
                        description=email
                    )
                    self._consent_contact_repository.add_contact_to_consent(
                        consent_id,
                        new_email_contact.ContactId
                    )
            
            # Actualizar teléfono si se proporciona
            if phone is not None:
                self._validate_phone(phone)
                
                # Buscar el contacto de tipo teléfono
                phone_contact = next((c for c in current_contacts if c.ContactTypeId == PHONE_TYPE_ID), None)
                
                if phone_contact:
                    # Actualizar el teléfono existente
                    self._contact_repository.update(
                        contact_id=phone_contact.ContactId,
                        Description=phone
                    )
                else:
                    # Crear nuevo contacto de teléfono
                    new_phone_contact = self._contact_repository.create(
                        contact_type_id=PHONE_TYPE_ID,
                        description=phone
                    )
                    self._consent_contact_repository.add_contact_to_consent(
                        consent_id,
                        new_phone_contact.ContactId
                    )
            
            return self.get_consent_by_id(consent_id)
            
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar contactos: {str(e)}")

    def delete_consent(self, consent_id):
        """Marca un consentimiento como eliminado (soft delete)"""
        try:
            consent = self._consent_repository.get_by_id(consent_id)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            return self._consent_repository.delete(consent_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar consentimiento: {str(e)}")
    
    def restore_consent(self, consent_id):
        """Restaura un consentimiento marcado como eliminado"""
        try:
            consent = self._consent_repository.get_by_id(consent_id, include_deleted=True)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            if not consent.IsDeleted:
                raise Exception(f"El consentimiento con ID {consent_id} no está eliminado.")
            
            return self._consent_repository.restore(consent_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar consentimiento: {str(e)}")