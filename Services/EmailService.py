# Services/EmailService.py

from flask_mail import Message
from flask import current_app, render_template_string
from datetime import datetime
import os

class EmailService:
    def __init__(self, mail_instance):
        """
        Inicializa el servicio de correo.
        
        Args:
            mail_instance: Instancia de Flask-Mail
        """
        self.mail = mail_instance
    
    def send_consent_alert_email(self, consent_data, contact_data):
        
        try:
            # Obtener el correo destinatario desde la configuración
            recipient_email = current_app.config.get('ALERT_EMAIL_RECIPIENT')
            
            if not recipient_email:
                raise Exception("No se configuró el correo destinatario (ALERT_EMAIL_RECIPIENT)")
            
            # Crear el asunto del correo
            subject = f"🚨 ALERTA: Nuevo consentimiento por riesgo de ideación suicida - {consent_data['FullName']}"
            
            # Crear el cuerpo del correo en HTML
            html_body = self._create_consent_alert_html(consent_data, contact_data)
            
            # Crear mensaje
            msg = Message(
                subject=subject,
                recipients=[recipient_email],
                html=html_body
            )
            
            # Enviar correo
            self.mail.send(msg)
            
            print(f"✅ Correo de alerta enviado exitosamente a: {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar correo de alerta: {str(e)}")
            # No lanzamos la excepción para que no falle la creación del consentimiento
            # Solo registramos el error
            return False
    
    def _create_consent_alert_html(self, consent_data, contact_data):
        
        html_template = """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Alerta de Consentimiento</title>
                <style>
                    body {
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f5f5f5;
                        margin: 0;
                        padding: 20px;
                    }
                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }
                    .header {
                        background: none;
                        padding: 30px;
                        text-align: center;
                    }
                    .alert-icon {
                        font-size: 48px;
                        margin-bottom: 10px;
                    }
                    .header h1 {
                        margin: 0;
                        font-size: 24px;
                        font-weight: bold;
                        color: #181818;
                    }
                    .priority-badge {
                        background-color: #d32f2f;
                        color: white;
                        padding: 5px 15px;
                        border-radius: 20px;
                        font-size: 12px;
                        font-weight: 600;
                        display: inline-block;
                        margin-top: 10px;
                    }
                    .content {
                        padding: 30px;
                    }
                    .alert-message {
                        background-color: #fff3e0;
                        border-left: 4px solid #ff9800;
                        padding: 15px;
                        margin-bottom: 25px;
                        border-radius: 4px;
                    }
                    .alert-message p {
                        margin: 0;
                        color: #e65100;
                        font-weight: 500;
                    }
                    .info-section {
                        margin-bottom: 25px;
                    }
                    .info-section h2 {
                        color: #333;
                        font-size: 18px;
                        margin-bottom: 15px;
                        border-bottom: 2px solid #e0e0e0;
                        padding-bottom: 8px;
                    }
                    .info-row {
                        display: flex;
                        padding: 10px 0;
                        border-bottom: 1px solid #f0f0f0;
                    }
                    .info-label {
                        font-weight: 600;
                        color: #666;
                        min-width: 180px;
                    }
                    .info-value {
                        color: #333;
                        flex: 1;
                    }
                    .contact-box {
                        background-color: #e8f5e9;
                        border: 1px solid #4caf50;
                        border-radius: 8px;
                        padding: 20px;
                        margin-top: 20px;
                    }
                    .contact-box h3 {
                        margin-top: 0;
                        color: #2e7d32;
                        font-size: 16px;
                    }
                    .contact-item {
                        margin: 10px 0;
                    }
                    .contact-item strong {
                        color: #1b5e20;
                    }
                    .footer {
                        background-color: #f5f5f5;
                        padding: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                    }
                    .timestamp {
                        color: #999;
                        font-size: 13px;
                        margin-top: 20px;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <div class="alert-icon">🚨</div>
                        <h1>ALERTA DE RIESGO DE IDEACIÓN SUICIDA</h1>
                        <span class="priority-badge">PRIORIDAD ALTA</span>
                    </div>
                    
                    <div class="content">
                        <div class="alert-message">
                            <p>
                                <strong>⚠️ Atención Inmediata Requerida ⚠️</strong><br>
                                Un usuario ha solicitado ayuda profesional tras detectarse riesgo de ideación suicida.
                                El usuario ha dado su consentimiento para ser contactado.
                            </p>
                        </div>
                        
                        <div class="info-section">
                            <h2>📋 Información del Paciente</h2>
                            <div class="info-row">
                                <div class="info-label">Nombre Completo:</div>
                                <div class="info-value"><strong>{{ full_name }}</strong></div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">Tipo de Documento:</div>
                                <div class="info-value">{{ document_type }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">Número de Documento:</div>
                                <div class="info-value">{{ document_number }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">ID de Consentimiento:</div>
                                <div class="info-value">#{{ consent_id }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">ID de Sesión:</div>
                                <div class="info-value">#{{ session_id }}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">Fecha y Hora:</div>
                                <div class="info-value">{{ created_at }}</div>
                            </div>
                        </div>
                        
                        <div class="contact-box">
                            <h3>📞 Información de Contacto</h3>
                            <div class="contact-item">
                                <strong>📧 Email:</strong> 
                                <a href="mailto:{{ email }}" style="color: #1976d2; text-decoration: none;">{{ email }}</a>
                            </div>
                            <div class="contact-item">
                                <strong>📱 Teléfono:</strong> 
                                <a href="tel:{{ phone }}" style="color: #1976d2; text-decoration: none;">{{ phone }}</a>
                            </div>
                        </div>
                        
                        <div class="info-section" style="margin-top: 25px;">
                            <h2>⚡ Acciones Recomendadas</h2>
                            <ul style="color: #333; line-height: 1.8;">
                                <li>Contactar al paciente <strong>lo más pronto posible</strong></li>
                                <li>Realizar evaluación inicial del riesgo</li>
                                <li>Determinar necesidad de intervención inmediata</li>
                                <li>Documentar toda comunicación</li>
                                <li>Seguir protocolo de crisis si es necesario</li>
                            </ul>
                        </div>
                        
                        <div class="timestamp">
                            📅 Correo generado automáticamente el {{ current_date }}
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p><strong>Sistema de Alertas Tempranas - Plataforma Jinsei</strong></p>
                        <p>Este es un correo automático. Por favor no responder a esta dirección.</p>
                        <p>Para consultas, contacte al administrador del sistema.</p>
                    </div>
                </div>
            </body>
            </html>


        """
        
        # Formatear la fecha
        created_at_formatted = consent_data['CreatedAt'].strftime('%d/%m/%Y %H:%M:%S') if isinstance(consent_data['CreatedAt'], datetime) else str(consent_data['CreatedAt'])
        current_date_formatted = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        # Renderizar el template con los datos
        html = render_template_string(
            html_template,
            full_name=consent_data['FullName'],
            document_type=consent_data['DocumentType'],
            document_number=consent_data['DocumentNumber'],
            consent_id=consent_data['ConsentId'],
            session_id=consent_data['SessionId'],
            created_at=created_at_formatted,
            email=contact_data['email'],
            phone=contact_data['phone'],
            current_date=current_date_formatted
        )
        
        return html
    
    def send_test_email(self, recipient_email):

        try:
            msg = Message(
                subject="🧪 Prueba de Configuración - Sistema Jinsei",
                recipients=[recipient_email],
                html="""
                <html>
                    <body style="font-family: Arial, sans-serif; padding: 20px;">
                        <h2 style="color: #4caf50;">✅ Configuración de Correo Exitosa</h2>
                        <p>Este es un correo de prueba del sistema Jinsei.</p>
                        <p>Si recibes este mensaje, significa que la configuración de correo está funcionando correctamente.</p>
                        <hr>
                        <p style="color: #666; font-size: 12px;">Sistema de Alerta Temprana - Plataforma Jinsei</p>
                    </body>
                </html>
                """
            )
            
            self.mail.send(msg)
            print(f"✅ Correo de prueba enviado exitosamente a: {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Error al enviar correo de prueba: {str(e)}")
            return False