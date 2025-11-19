from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.SessionService import SessionService
from datetime import datetime

session_bp = Blueprint('sessions', __name__)
session_service = SessionService()

@session_bp.route('/sessions', methods=['GET'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Obtener todas las sesiones',
    'parameters': [
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False,
            'description': 'Incluir sesiones eliminadas'
        }
    ],
    'responses': {
        200: {'description': 'Lista de sesiones'},
        500: {'description': 'Error del servidor'}
    }
})
def get_all_sessions():
    """Obtiene todas las sesiones"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        sessions = session_service.get_all_sessions(include_deleted=include_deleted)
        
        sessions_data = [{
            'SessionId': session.SessionId,
            'UserId': session.UserId,
            'StartTime': session.StartTime.isoformat() if session.StartTime else None,
            'EndTime': session.EndTime.isoformat() if session.EndTime else None,
            'RiskLevelId': session.RiskLevelId,
            'FinalRiskLevel': session.FinalRiskLevel,
            'IsDeleted': session.IsDeleted
        } for session in sessions]
        
        return jsonify({
            'success': True,
            'data': sessions_data,
            'count': len(sessions_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@session_bp.route('/sessions/<int:session_id>', methods=['GET'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Obtener una sesión por ID',
    'parameters': [
        {
            'name': 'session_id',
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
        200: {'description': 'Sesión encontrada'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def get_session_by_id(session_id):
    """Obtiene una sesión por ID"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        session = session_service.get_session_by_id(session_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'SessionId': session.SessionId,
                'UserId': session.UserId,
                'StartTime': session.StartTime.isoformat() if session.StartTime else None,
                'EndTime': session.EndTime.isoformat() if session.EndTime else None,
                'RiskLevelId': session.RiskLevelId,
                'FinalRiskLevel': session.FinalRiskLevel,
                'IsDeleted': session.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@session_bp.route('/users/<int:user_id>/sessions', methods=['GET'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Obtener todas las sesiones de un usuario',
    'parameters': [
        {
            'name': 'user_id',
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
        200: {'description': 'Lista de sesiones del usuario'},
        404: {'description': 'Usuario no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_sessions_by_user(user_id):
    """Obtiene todas las sesiones de un usuario"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        sessions = session_service.get_sessions_by_user(user_id, include_deleted=include_deleted)
        
        sessions_data = [{
            'SessionId': session.SessionId,
            'UserId': session.UserId,
            'StartTime': session.StartTime.isoformat() if session.StartTime else None,
            'EndTime': session.EndTime.isoformat() if session.EndTime else None,
            'RiskLevelId': session.RiskLevelId,
            'FinalRiskLevel': session.FinalRiskLevel,
            'IsDeleted': session.IsDeleted
        } for session in sessions]
        
        return jsonify({
            'success': True,
            'data': sessions_data,
            'count': len(sessions_data)
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@session_bp.route('/users/<int:user_id>/sessions/active', methods=['GET'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Obtener la sesión activa de un usuario',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        }
    ],
    'responses': {
        200: {'description': 'Sesión activa encontrada'},
        404: {'description': 'No hay sesión activa'},
        500: {'description': 'Error del servidor'}
    }
})
def get_active_session(user_id):
    """Obtiene la sesión activa de un usuario"""
    try:
        session = session_service.get_active_session(user_id)
        
        if not session:
            return jsonify({
                'success': True,
                'data': None,
                'message': 'No hay sesión activa para este usuario'
            }), 200
        
        return jsonify({
            'success': True,
            'data': {
                'SessionId': session.SessionId,
                'UserId': session.UserId,
                'StartTime': session.StartTime.isoformat() if session.StartTime else None,
                'RiskLevelId': session.RiskLevelId,
                'IsDeleted': session.IsDeleted
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@session_bp.route('/sessions', methods=['POST'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Crear una nueva sesión',
    'description': 'Crea una sesión activa para un usuario. Los campos RiskLevelId y FinalRiskLevel se calcularán automáticamente al finalizar la sesión.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['user_id'],
                'properties': {
                    'user_id': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID del usuario que inicia la sesión'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Sesión creada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'SessionId': {'type': 'integer'},
                            'UserId': {'type': 'integer'},
                            'StartTime': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {'description': 'Datos inválidos o usuario ya tiene sesión activa'},
        500: {'description': 'Error del servidor'}
    }
})
def create_session():
    """Crea una nueva sesión"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({
                'success': False,
                'error': 'El campo "user_id" es requerido'
            }), 400
        
        new_session = session_service.create_session(user_id=user_id)
        
        return jsonify({
            'success': True,
            'message': 'Sesión creada exitosamente',
            'data': {
                'SessionId': new_session.SessionId,
                'UserId': new_session.UserId,
                'StartTime': new_session.StartTime.isoformat() if new_session.StartTime else None
            }
        }), 201
    except Exception as e:
        error_msg = str(e)
        status_code = 404 if 'no existe' in error_msg else (400 if 'ya tiene' in error_msg else 500)
        return jsonify({
            'success': False,
            'error': error_msg
        }), status_code


@session_bp.route('/sessions/<int:session_id>/end', methods=['POST'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Finalizar una sesión',
    'description': 'Finaliza una sesión calculando automáticamente el promedio de riesgo (FinalRiskLevel) y el nivel de riesgo (RiskLevelId) basándose en todos los mensajes de la sesión.',
    'parameters': [
        {
            'name': 'session_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID de la sesión a finalizar'
        }
    ],
    'responses': {
        200: {
            'description': 'Sesión finalizada exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'SessionId': {'type': 'integer'},
                            'EndTime': {'type': 'string'},
                            'FinalRiskLevel': {
                                'type': 'number',
                                'description': 'Promedio calculado de riesgo (0-100)'
                            },
                            'RiskLevelId': {
                                'type': 'integer',
                                'description': 'ID del nivel de riesgo asignado'
                            }
                        }
                    }
                }
            }
        },
        404: {'description': 'Sesión no encontrada'},
        400: {'description': 'La sesión ya está finalizada'},
        500: {'description': 'Error del servidor'}
    }
})
def end_session(session_id):
    """Finaliza una sesión calculando automáticamente el riesgo promedio"""
    try:
        session = session_service.end_session(session_id)
        
        return jsonify({
            'success': True,
            'message': 'Sesión finalizada exitosamente',
            'data': {
                'SessionId': session.SessionId,
                'EndTime': session.EndTime.isoformat() if session.EndTime else None,
                'FinalRiskLevel': session.FinalRiskLevel,
                'RiskLevelId': session.RiskLevelId
            }
        }), 200
    except Exception as e:
        error_msg = str(e)
        if 'no existe' in error_msg:
            status_code = 404
        elif 'ya está finalizada' in error_msg:
            status_code = 400
        else:
            status_code = 500
            
        return jsonify({
            'success': False,
            'error': error_msg
        }), status_code


@session_bp.route('/sessions/<int:session_id>', methods=['PUT'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Actualizar una sesión',
    'description': 'Solo permite actualizar el user_id. Los campos de riesgo se calculan automáticamente al finalizar.',
    'parameters': [
        {
            'name': 'session_id',
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
                    'user_id': {
                        'type': 'integer',
                        'description': 'Nuevo ID del usuario'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Sesión actualizada'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def update_session(session_id):
    """Actualiza una sesión"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        updated_session = session_service.update_session(
            session_id=session_id,
            user_id=data.get('user_id')
        )
        
        return jsonify({
            'success': True,
            'message': 'Sesión actualizada exitosamente',
            'data': {
                'SessionId': updated_session.SessionId,
                'UserId': updated_session.UserId,
                'RiskLevelId': updated_session.RiskLevelId,
                'FinalRiskLevel': updated_session.FinalRiskLevel
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@session_bp.route('/sessions/<int:session_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Eliminar una sesión (soft delete)',
    'parameters': [
        {
            'name': 'session_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Sesión eliminada'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_session(session_id):
    """Elimina una sesión (soft delete)"""
    try:
        session_service.delete_session(session_id)
        
        return jsonify({
            'success': True,
            'message': f'Sesión con ID {session_id} eliminada exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@session_bp.route('/sessions/<int:session_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Restaurar una sesión eliminada',
    'parameters': [
        {
            'name': 'session_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Sesión restaurada'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def restore_session(session_id):
    """Restaura una sesión eliminada"""
    try:
        restored_session = session_service.restore_session(session_id)
        
        return jsonify({
            'success': True,
            'message': f'Sesión con ID {session_id} restaurada exitosamente',
            'data': {
                'SessionId': restored_session.SessionId,
                'IsDeleted': restored_session.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code
    


@session_bp.route('/sessions/<int:session_id>/history', methods=['GET'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Obtener historial de mensajes de una sesión',
    'description': 'Retorna toda la información de una sesión junto con el historial completo de mensajes intercambiados.',
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
            'default': False,
            'description': 'Incluir mensajes eliminados'
        }
    ],
    'responses': {
        200: {
            'description': 'Historial de mensajes obtenido exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'session': {
                                'type': 'object',
                                'properties': {
                                    'SessionId': {'type': 'integer'},
                                    'UserId': {'type': 'integer'},
                                    'StartTime': {'type': 'string'},
                                    'EndTime': {'type': 'string'},
                                    'RiskLevelId': {'type': 'integer'},
                                    'FinalRiskLevel': {'type': 'number'}
                                }
                            },
                            'messages': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'MessageId': {'type': 'integer'},
                                        'BotMessage': {'type': 'string'},
                                        'UserResponse': {'type': 'string'},
                                        'RiskPercent': {'type': 'number'},
                                        'CreatedAt': {'type': 'string'}
                                    }
                                }
                            },
                            'total_messages': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def get_session_history(session_id):
    """Obtiene el historial completo de mensajes de una sesión"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        history = session_service.get_session_messages_history(session_id, include_deleted=include_deleted)
        
        session = history['session']
        messages = history['messages']
        
        # Serializar sesión
        session_data = {
            'SessionId': session.SessionId,
            'UserId': session.UserId,
            'StartTime': session.StartTime.isoformat() if session.StartTime else None,
            'EndTime': session.EndTime.isoformat() if session.EndTime else None,
            'RiskLevelId': session.RiskLevelId,
            'FinalRiskLevel': session.FinalRiskLevel,
            'IsDeleted': session.IsDeleted
        }
        
        # Serializar mensajes
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
            'data': {
                'session': session_data,
                'messages': messages_data,
                'total_messages': history['total_messages']
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@session_bp.route('/users/<int:user_id>/history', methods=['GET'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Obtener historial completo de un usuario',
    'description': 'Retorna todas las sesiones del usuario con sus respectivos mensajes. Útil para ver el historial completo de conversaciones.',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario'
        },
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False,
            'description': 'Incluir sesiones y mensajes eliminados'
        }
    ],
    'responses': {
        200: {
            'description': 'Historial completo obtenido exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'user': {
                                'type': 'object',
                                'properties': {
                                    'UserId': {'type': 'integer'},
                                    'AKA': {'type': 'string'},
                                    'CreatedAt': {'type': 'string'}
                                }
                            },
                            'sessions': {
                                'type': 'array',
                                'items': {
                                    'type': 'object',
                                    'properties': {
                                        'session': {'type': 'object'},
                                        'messages': {'type': 'array'},
                                        'message_count': {'type': 'integer'}
                                    }
                                }
                            },
                            'total_sessions': {'type': 'integer'},
                            'total_messages': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        404: {'description': 'Usuario no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_user_history(user_id):
    """Obtiene el historial completo de sesiones y mensajes de un usuario"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        history = session_service.get_user_complete_history(user_id, include_deleted=include_deleted)
        
        user = history['user']
        sessions_with_messages = history['sessions']
        
        # Serializar usuario
        user_data = {
            'UserId': user.UserId,
            'AKA': user.AKA,
            'CreatedAt': user.CreatedAt.isoformat() if user.CreatedAt else None,
            'IsDeleted': user.IsDeleted
        }
        
        # Serializar sesiones con sus mensajes
        sessions_data = []
        for item in sessions_with_messages:
            session = item['session']
            messages = item['messages']
            
            session_info = {
                'SessionId': session.SessionId,
                'UserId': session.UserId,
                'StartTime': session.StartTime.isoformat() if session.StartTime else None,
                'EndTime': session.EndTime.isoformat() if session.EndTime else None,
                'RiskLevelId': session.RiskLevelId,
                'FinalRiskLevel': session.FinalRiskLevel,
                'IsDeleted': session.IsDeleted
            }
            
            messages_info = [{
                'MessageId': msg.MessageId,
                'SessionId': msg.SessionId,
                'BotMessage': msg.BotMessage,
                'UserResponse': msg.UserResponse,
                'RiskLevelId': msg.RiskLevelId,
                'RiskPercent': msg.RiskPercent,
                'CreatedAt': msg.CreatedAt.isoformat() if msg.CreatedAt else None,
                'IsDeleted': msg.IsDeleted
            } for msg in messages]
            
            sessions_data.append({
                'session': session_info,
                'messages': messages_info,
                'message_count': item['message_count']
            })
        
        return jsonify({
            'success': True,
            'data': {
                'user': user_data,
                'sessions': sessions_data,
                'total_sessions': history['total_sessions'],
                'total_messages': history['total_messages']
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code