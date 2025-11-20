# Controllers/EmailController.py (NUEVO - Solo para pruebas)

from flask import Blueprint, request, jsonify, current_app
from flasgger import swag_from
from Services.EmailService import EmailService
from app import mail

email_bp = Blueprint('email', __name__)

@email_bp.route('/email/test', methods=['POST'])
@swag_from({
    'tags': ['Email'],
    'summary': 'Probar configuración de correo',
    'description': 'Envía un correo de prueba para verificar que la configuración funciona',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['recipient_email'],
                'properties': {
                    'recipient_email': {
                        'type': 'string',
                        'example': 'test@ejemplo.com',
                        'description': 'Email destinatario de la prueba'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Correo de prueba enviado'},
        400: {'description': 'Datos inválidos'},
        500: {'description': 'Error al enviar correo'}
    }
})
def test_email():

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        recipient_email = data.get('recipient_email')
        
        if not recipient_email:
            return jsonify({
                'success': False,
                'error': 'El campo "recipient_email" es requerido'
            }), 400
        
        # Crear servicio de email y enviar prueba
        email_service = EmailService(mail)
        success = email_service.send_test_email(recipient_email)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Correo de prueba enviado exitosamente a {recipient_email}'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo enviar el correo de prueba'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500