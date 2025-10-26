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
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['user_id'],
                'properties': {
                    'user_id': {'type': 'integer', 'example': 1},
                    'risk_level_id': {'type': 'integer', 'example': 1},
                    'final_risk_level': {'type': 'string', 'example': 'Bajo'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Sesión creada'},
        400: {'description': 'Datos inválidos'},
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
        
        risk_level_id = data.get('risk_level_id')
        final_risk_level = data.get('final_risk_level')
        
        new_session = session_service.create_session(
            user_id=user_id,
            risk_level_id=risk_level_id,
            final_risk_level=final_risk_level
        )
        
        return jsonify({
            'success': True,
            'message': 'Sesión creada exitosamente',
            'data': {
                'SessionId': new_session.SessionId,
                'UserId': new_session.UserId,
                'StartTime': new_session.StartTime.isoformat() if new_session.StartTime else None,
                'RiskLevelId': new_session.RiskLevelId,
                'FinalRiskLevel': new_session.FinalRiskLevel
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
                    'final_risk_level': {'type': 'string', 'example': 'Moderado'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Sesión finalizada'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def end_session(session_id):
    """Finaliza una sesión"""
    try:
        data = request.get_json() or {}
        final_risk_level = data.get('final_risk_level')
        
        session = session_service.end_session(session_id, final_risk_level)
        
        return jsonify({
            'success': True,
            'message': 'Sesión finalizada exitosamente',
            'data': {
                'SessionId': session.SessionId,
                'EndTime': session.EndTime.isoformat() if session.EndTime else None,
                'FinalRiskLevel': session.FinalRiskLevel
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@session_bp.route('/sessions/<int:session_id>', methods=['PUT'])
@swag_from({
    'tags': ['Sessions'],
    'summary': 'Actualizar una sesión',
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
                    'user_id': {'type': 'integer'},
                    'risk_level_id': {'type': 'integer'},
                    'final_risk_level': {'type': 'string'}
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
            user_id=data.get('user_id'),
            risk_level_id=data.get('risk_level_id'),
            final_risk_level=data.get('final_risk_level')
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