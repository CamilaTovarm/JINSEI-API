from Repositories.ConsentRepository import ConsentRepository
from Repositories.ContactRepository import ContactRepository
from Repositories.ConsentContactRepository import ConsentContactRepository
from Repositories.SessionRepository import SessionRepository
from Repositories.DocumentTypeRepository import DocumentTypeRepository
from Repositories.ContactTypeRepository import ContactTypeRepository
from Services.EmailService import EmailService
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

        try:
            return self._consent_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener consentimientos: {str(e)}")

    def get_consent_by_id(self, consent_id, include_deleted=False):

        try:
            consent = self._consent_repository.get_by_id(consent_id, include_deleted=include_deleted)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            return consent
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener consentimiento: {str(e)}")
    
    def get_consents_by_session(self, session_id, include_deleted=False):

        try:
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            return self._consent_repository.get_by_session_id(session_id, include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener consentimientos de la sesión: {str(e)}")

    def _validate_email(self, email):

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise Exception(f"El email '{email}' no tiene un formato válido.")
    
    def _validate_phone(self, phone):
    # Acepta números con o sin espacios, guiones, paréntesis y prefijo +
        phone_clean = re.sub(r'[\s\-\(\)\+]', '', phone)
        if not phone_clean.isdigit() or len(phone_clean) < 7 or len(phone_clean) > 15:
            raise Exception(f"El teléfono '{phone}' no tiene un formato válido.")

    def create_consent(self, session_id, full_name, document_type_id, document_number, email, phone):

        try:
            #Validar que la sesión existe
            session = self._session_repository.get_by_id(session_id)
            if not session:
                raise Exception(f"La sesión con ID {session_id} no existe.")
            
            #Validar que el tipo de documento existe
            doc_type = self._document_type_repository.get_by_id(document_type_id)
            if not doc_type:
                raise Exception(f"El tipo de documento con ID {document_type_id} no existe.")
            
            #Verificar duplicados por documento
            existing_consent = self._consent_repository.get_by_document(document_type_id, document_number)
            if existing_consent:
                raise Exception(f"Ya existe un consentimiento para el documento {document_number}.")
            
            #Validar formatos de email y teléfono
            self._validate_email(email)
            self._validate_phone(phone)
            
            #Verificar que los ContactTypeId existen
            #ContactTypeId = 1 (Email), ContactTypeId = 2 (Teléfono)
            EMAIL_TYPE_ID = 3
            PHONE_TYPE_ID = 4
            
            email_type = self._contact_type_repository.get_by_id(EMAIL_TYPE_ID)
            if not email_type:
                raise Exception(f"El tipo de contacto Email (ID: {EMAIL_TYPE_ID}) no existe en la base de datos.")
            
            phone_type = self._contact_type_repository.get_by_id(PHONE_TYPE_ID)
            if not phone_type:
                raise Exception(f"El tipo de contacto Teléfono (ID: {PHONE_TYPE_ID}) no existe en la base de datos.")
        
            new_consent = self._consent_repository.create(
                session_id=session_id,
                full_name=full_name,
                document_type_id=document_type_id,
                document_number=document_number
            )

            #Crear los contactos
            email_contact = self._contact_repository.create(
                contact_type_id=EMAIL_TYPE_ID,
                description=email  
            )
            
            phone_contact = self._contact_repository.create(
                contact_type_id=PHONE_TYPE_ID,
                description=phone  
            )

            #Asociar ambos contactos con el consentimiento en la tabla intermedia
            self._consent_contact_repository.add_contact_to_consent(
                new_consent.ConsentId, 
                email_contact.ContactId
            )
            self._consent_contact_repository.add_contact_to_consent(
                new_consent.ConsentId, 
                phone_contact.ContactId
            )

            #ENVIAR CORREO AUTOMÁTICAMENTE
            try:
                # Obtener instancia Flask-Mail desde el contexto de la app
                from app import mail
                email_service = EmailService(mail)
            
                consent_data = {
                    'ConsentId': new_consent.ConsentId,
                    'FullName': full_name,
                    'DocumentNumber': document_number,
                    'DocumentType': doc_type.Description,
                    'SessionId': session_id,
                    'CreatedAt': new_consent.CreatedAt
                }
                
                contact_data = {
                    'email': email,
                    'phone': phone
                }
                
                # Enviar correo 
                email_sent = email_service.send_consent_alert_email(consent_data, contact_data)
                
                if email_sent:
                    print(f"Correo de alerta enviado por consentimiento ID: {new_consent.ConsentId}")
                else:
                    print(f"No se pudo enviar el correo de alerta para el consentimiento ID: {new_consent.ConsentId}")
                    # No lanzamos excepción para que no falle la creación del consentimiento
                    
            except Exception as email_error:
                print(f"Error al enviar correo de alerta: {str(email_error)}")
            # ============================================================

            return new_consent

        except SQLAlchemyError as e:
            raise Exception(f"Error de base de datos: {str(e)}")
        except Exception as e:
            raise Exception(f"Error al crear consentimiento: {str(e)}")

    def update_consent(self, consent_id, session_id=None, full_name=None, document_type_id=None, document_number=None):

        try:
            # Validar que el consentimiento existe
            consent = self._consent_repository.get_by_id(consent_id)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
          
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

        try:
            # Validar que el consentimiento existe
            consent = self._consent_repository.get_by_id(consent_id)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            EMAIL_TYPE_ID = 1
            PHONE_TYPE_ID = 2
            
            # Obtener contactos actuales del consentimiento
            current_contacts = self._consent_contact_repository.get_contacts_by_consent(consent_id)
        
            if email is not None:
                self._validate_email(email)
                
                # Buscar el contacto de tipo email
                email_contact = next((c for c in current_contacts if c.ContactTypeId == EMAIL_TYPE_ID), None)
                
                if email_contact: 
                    self._contact_repository.update(
                        contact_id=email_contact.ContactId,
                        Description=email
                    )
                else: 
                    new_email_contact = self._contact_repository.create(
                        contact_type_id=EMAIL_TYPE_ID,
                        description=email
                    )
                    self._consent_contact_repository.add_contact_to_consent(
                        consent_id,
                        new_email_contact.ContactId
                    )
        
            if phone is not None:
                self._validate_phone(phone)
                
                # Buscar el contacto de tipo teléfono
                phone_contact = next((c for c in current_contacts if c.ContactTypeId == PHONE_TYPE_ID), None)
                
                if phone_contact: 
                    self._contact_repository.update(
                        contact_id=phone_contact.ContactId,
                        Description=phone
                    )
                else: 
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

        try:
            consent = self._consent_repository.get_by_id(consent_id)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            return self._consent_repository.delete(consent_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar consentimiento: {str(e)}")
    
    def restore_consent(self, consent_id):

        try:
            consent = self._consent_repository.get_by_id(consent_id, include_deleted=True)
            if not consent:
                raise Exception(f"El consentimiento con ID {consent_id} no existe.")
            
            if not consent.IsDeleted:
                raise Exception(f"El consentimiento con ID {consent_id} no está eliminado.")
            
            return self._consent_repository.restore(consent_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar consentimiento: {str(e)}")