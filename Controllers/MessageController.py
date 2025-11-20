from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.MessageService import MessageService

message_bp = Blueprint('messages', __name__)
message_service = MessageService()

@message_bp.route('/messages', methods=['GET'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Obtener todos los mensajes',
    'parameters': [
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False,
            'description': 'Incluir mensajes eliminados'
        }
    ],
    'responses': {
        200: {'description': 'Lista de mensajes'},
        500: {'description': 'Error del servidor'}
    }
})
def get_all_messages():
    try: 
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        messages = message_service.get_all_messages(include_deleted=include_deleted)
        
        messages_data = [{
            'MessageId': msg.MessageId,
            'SessionId': msg.SessionId,
            'BotMessage': msg.BotMessage,
            'UserResponse': msg.UserResponse,
            'RiskLevelId': msg.RiskLevelId,
            'RiskPercent': msg.RiskPercent,
            'CreatedAt': msg.CreatedAt.isoformat() if msg.CreatedAt else None,
            'IsDeleted': msg.IsDeleted
        } for msg in messages]
        
        return jsonify({
            'success': True,
            'data': messages_data,
            'count': len(messages_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@message_bp.route('/messages/<int:message_id>', methods=['GET'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Obtener un mensaje por ID',
    'parameters': [
        {
            'name': 'message_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False
        }
    ],
    'responses': {
        200: {'description': 'Mensaje encontrado'},
        404: {'description': 'Mensaje no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_message_by_id(message_id):
    try: 
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        message = message_service.get_message_by_id(message_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'MessageId': message.MessageId,
                'SessionId': message.SessionId,
                'BotMessage': message.BotMessage,
                'UserResponse': message.UserResponse,
                'RiskLevelId': message.RiskLevelId,
                'RiskPercent': message.RiskPercent,
                'CreatedAt': message.CreatedAt.isoformat() if message.CreatedAt else None,
                'IsDeleted': message.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@message_bp.route('/sessions/<int:session_id>/messages', methods=['GET'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Obtener todos los mensajes de una sesión',
    'parameters': [
        {
            'name': 'session_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la sesión'
        },
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False
        }
    ],
    'responses': {
        200: {'description': 'Lista de mensajes de la sesión'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def get_messages_by_session(session_id):
    try: 
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        messages = message_service.get_messages_by_session(session_id, include_deleted=include_deleted)
        
        messages_data = [{
            'MessageId': msg.MessageId,
            'SessionId': msg.SessionId,
            'BotMessage': msg.BotMessage,
            'UserResponse': msg.UserResponse,
            'RiskLevelId': msg.RiskLevelId,
            'RiskPercent': msg.RiskPercent,
            'CreatedAt': msg.CreatedAt.isoformat() if msg.CreatedAt else None,
            'IsDeleted': msg.IsDeleted
        } for msg in messages]
        
        return jsonify({
            'success': True,
            'data': messages_data,
            'count': len(messages_data)
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@message_bp.route('/messages', methods=['POST'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Crear un nuevo mensaje en la sesión activa del usuario',
    'description': 'Crea un mensaje asociado automáticamente a la sesión activa del usuario. El RiskLevelId se calcula automáticamente basado en el risk_percent proporcionado.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['user_id', 'bot_message'],
                'properties': {
                    'user_id': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID del usuario (se usará su sesión activa)'
                    },
                    'bot_message': {
                        'type': 'string',
                        'example': '¿Cómo te sientes hoy?',
                        'description': 'Mensaje enviado por el bot'
                    },
                    'user_response': {
                        'type': 'string',
                        'example': 'Me siento bien',
                        'description': 'Respuesta del usuario (opcional)'
                    },
                    'risk_percent': {
                        'type': 'number',
                        'example': 75.5,
                        'description': 'Porcentaje de riesgo (0-100). El RiskLevelId se calcula automáticamente: 0-33=Bajo, 34-66=Medio, 67-100=Alto'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Mensaje creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'MessageId': {'type': 'integer'},
                            'SessionId': {'type': 'integer'},
                            'BotMessage': {'type': 'string'},
                            'UserResponse': {'type': 'string'},
                            'RiskLevelId': {'type': 'integer'},
                            'RiskPercent': {'type': 'number'},
                            'CreatedAt': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {'description': 'Datos inválidos o faltantes'},
        404: {'description': 'Usuario no encontrado o sin sesión activa'},
        500: {'description': 'Error del servidor'}
    }
})
def create_message():
    try: 
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar campos requeridos
        user_id = data.get('user_id')
        bot_message = data.get('bot_message')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'El campo "user_id" es requerido'
            }), 400
            
        if not bot_message:
            return jsonify({
                'success': False,
                'error': 'El campo "bot_message" es requerido'
            }), 400
        
        # Campos opcionales
        user_response = data.get('user_response') 
        risk_percent = data.get('risk_percent')
        
        # Validar risk_percent si se proporciona
        if risk_percent is not None:
            if not isinstance(risk_percent, (int, float)):
                return jsonify({
                    'success': False,
                    'error': 'El campo "risk_percent" debe ser un número'
                }), 400
            if risk_percent < 0 or risk_percent > 100:
                return jsonify({
                    'success': False,
                    'error': 'El campo "risk_percent" debe estar entre 0 y 100'
                }), 400
        
        # Crear mensaje (el service obtiene la sesión activa y calcula el risk_level_id)
        new_message = message_service.create_message(
            user_id=user_id,
            bot_message=bot_message,
            user_response=user_response, 
            risk_percent=risk_percent
        ) 
        
        return jsonify({
            'success': True,
            'message': 'Mensaje creado exitosamente',
            'data': {
                'MessageId': new_message.MessageId,
                'SessionId': new_message.SessionId,
                'BotMessage': new_message.BotMessage,
                'UserResponse': new_message.UserResponse,
                'RiskLevelId': new_message.RiskLevelId,
                'RiskPercent': new_message.RiskPercent,
                'CreatedAt': new_message.CreatedAt.isoformat() if new_message.CreatedAt else None
            }
        }), 201
    except Exception as e:
        # Determinar código de error apropiado
        error_msg = str(e).lower()
        if 'no existe' in error_msg or 'no tiene una sesión activa' in error_msg:
            status_code = 404
        else:
            status_code = 500
            
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@message_bp.route('/messages/<int:message_id>', methods=['PUT'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Actualizar un mensaje',
    'description': 'Si se actualiza risk_percent, el RiskLevelId se recalcula automáticamente',
    'parameters': [
        {
            'name': 'message_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'bot_message': {
                        'type': 'string',
                        'description': 'Nuevo mensaje del bot'
                    },
                    'user_response': {
                        'type': 'string',
                        'description': 'Nueva respuesta del usuario'
                    },
                    'risk_percent': {
                        'type': 'number',
                        'description': 'Nuevo porcentaje de riesgo (0-100). El RiskLevelId se recalcula automáticamente'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Mensaje actualizado'},
        400: {'description': 'Datos inválidos'},
        404: {'description': 'Mensaje no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_message(message_id):
    try: 
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar risk_percent si se proporciona
        risk_percent = data.get('risk_percent')
        if risk_percent is not None:
            if not isinstance(risk_percent, (int, float)):
                return jsonify({
                    'success': False,
                    'error': 'El campo "risk_percent" debe ser un número'
                }), 400
            if risk_percent < 0 or risk_percent > 100:
                return jsonify({
                    'success': False,
                    'error': 'El campo "risk_percent" debe estar entre 0 y 100'
                }), 400
        
        updated_message = message_service.update_message(
            message_id=message_id,
            bot_message=data.get('bot_message'),
            user_response=data.get('user_response'),
            risk_percent=risk_percent
        )
        
        return jsonify({
            'success': True,
            'message': 'Mensaje actualizado exitosamente',
            'data': {
                'MessageId': updated_message.MessageId,
                'SessionId': updated_message.SessionId,
                'BotMessage': updated_message.BotMessage,
                'UserResponse': updated_message.UserResponse,
                'RiskLevelId': updated_message.RiskLevelId,
                'RiskPercent': updated_message.RiskPercent
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@message_bp.route('/messages/<int:message_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Eliminar un mensaje (soft delete)',
    'parameters': [
        {
            'name': 'message_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Mensaje eliminado'},
        404: {'description': 'Mensaje no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_message(message_id):
    try: 
        message_service.delete_message(message_id)
        
        return jsonify({
            'success': True,
            'message': f'Mensaje con ID {message_id} eliminado exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@message_bp.route('/messages/<int:message_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Restaurar un mensaje eliminado',
    'parameters': [
        {
            'name': 'message_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Mensaje restaurado'},
        404: {'description': 'Mensaje no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def restore_message(message_id):
    try: 
        restored_message = message_service.restore_message(message_id)
        
        return jsonify({
            'success': True,
            'message': f'Mensaje con ID {message_id} restaurado exitosamente',
            'data': {
                'MessageId': restored_message.MessageId,
                'IsDeleted': restored_message.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code