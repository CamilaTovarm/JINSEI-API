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
    'summary': 'Crear un nuevo mensaje',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['session_id', 'bot_message'],
                'properties': {
                    'session_id': {'type': 'integer', 'example': 1},
                    'bot_message': {'type': 'string', 'example': '¿Cómo te sientes hoy?'},
                    'user_response': {'type': 'string', 'example': 'Me siento bien'},
                    'risk_level_id': {'type': 'integer', 'example': 1},
                    'risk_percent': {'type': 'number', 'example': 20.5}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Mensaje creado'},
        400: {'description': 'Datos inválidos'},
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
        
        session_id = data.get('session_id')
        bot_message = data.get('bot_message')
        
        if not session_id or not bot_message:
            return jsonify({
                'success': False,
                'error': 'Los campos "session_id" y "bot_message" son requeridos'
            }), 400
        
        user_response = data.get('user_response')
        risk_level_id = data.get('risk_level_id')
        risk_percent = data.get('risk_percent')
        
        new_message = message_service.create_message(
            session_id=session_id,
            bot_message=bot_message,
            user_response=user_response,
            risk_level_id=risk_level_id,
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
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@message_bp.route('/messages/<int:message_id>', methods=['PUT'])
@swag_from({
    'tags': ['Messages'],
    'summary': 'Actualizar un mensaje',
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
                    'bot_message': {'type': 'string'},
                    'user_response': {'type': 'string'},
                    'risk_level_id': {'type': 'integer'},
                    'risk_percent': {'type': 'number'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Mensaje actualizado'},
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
        
        updated_message = message_service.update_message(
            message_id=message_id,
            bot_message=data.get('bot_message'),
            user_response=data.get('user_response'),
            risk_level_id=data.get('risk_level_id'),
            risk_percent=data.get('risk_percent')
        )
        
        return jsonify({
            'success': True,
            'message': 'Mensaje actualizado exitosamente',
            'data': {
                'MessageId': updated_message.MessageId,
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