from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.UserService import UserService

user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('/users', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Obtener todos los usuarios',
    'parameters': [
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False,
            'description': 'Incluir usuarios eliminados'
        }
    ],
    'responses': {
        200: {
            'description': 'Lista de usuarios',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'UserId': {'type': 'integer'},
                                'AKA': {'type': 'string'},
                                'CreatedAt': {'type': 'string', 'format': 'date-time'},
                                'IsDeleted': {'type': 'boolean'}
                            }
                        }
                    }
                }
            }
        },
        500: {'description': 'Error del servidor'}
    }
})
def get_all_users():
    """Obtiene todos los usuarios"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        users = user_service.get_all_users(include_deleted=include_deleted)
        
        # Serializar usuarios
        users_data = [{
            'UserId': user.UserId,
            'AKA': user.AKA,
            'CreatedAt': user.CreatedAt.isoformat() if user.CreatedAt else None,
            'IsDeleted': user.IsDeleted
        } for user in users]
        
        return jsonify({
            'success': True,
            'data': users_data,
            'count': len(users_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@user_bp.route('/users/<int:user_id>', methods=['GET'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Obtener un usuario por ID',
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
            'description': 'Incluir si está eliminado'
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario encontrado',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'UserId': {'type': 'integer'},
                            'AKA': {'type': 'string'},
                            'CreatedAt': {'type': 'string'},
                            'IsDeleted': {'type': 'boolean'}
                        }
                    }
                }
            }
        },
        404: {'description': 'Usuario no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_user_by_id(user_id):
    """Obtiene un usuario por ID"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        user = user_service.get_user_by_id(user_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'UserId': user.UserId,
                'AKA': user.AKA,
                'CreatedAt': user.CreatedAt.isoformat() if user.CreatedAt else None,
                'IsDeleted': user.IsDeleted
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404 if 'no existe' in str(e) else 500


@user_bp.route('/users', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Crear un nuevo usuario',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['aka', 'password'],
                'properties': {
                    'aka': {
                        'type': 'string',
                        'example': 'john_doe',
                        'description': 'Nombre de usuario único'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'hashedPassword123',
                        'description': 'Contraseña (debe estar hasheada)'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Usuario creado exitosamente',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'UserId': {'type': 'integer'},
                            'AKA': {'type': 'string'},
                            'CreatedAt': {'type': 'string'}
                        }
                    }
                }
            }
        },
        400: {'description': 'Datos inválidos'},
        500: {'description': 'Error del servidor'}
    }
})
def create_user():
    """Crea un nuevo usuario"""
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        aka = data.get('aka')
        password = data.get('password')
        
        if not aka or not password:
            return jsonify({
                'success': False,
                'error': 'Los campos "aka" y "password" son requeridos'
            }), 400
        
        # Crear usuario
        new_user = user_service.create_user(aka, password)
        
        return jsonify({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': {
                'UserId': new_user.UserId,
                'AKA': new_user.AKA,
                'CreatedAt': new_user.CreatedAt.isoformat() if new_user.CreatedAt else None
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400 if 'ya existe' in str(e) else 500


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Actualizar un usuario',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a actualizar'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'aka': {
                        'type': 'string',
                        'example': 'new_username',
                        'description': 'Nuevo nombre de usuario (opcional)'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'newHashedPassword',
                        'description': 'Nueva contraseña (opcional)'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Usuario actualizado'},
        400: {'description': 'Datos inválidos'},
        404: {'description': 'Usuario no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_user(user_id):
    """Actualiza un usuario existente"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        aka = data.get('aka')
        password = data.get('password')
        
        # Actualizar usuario
        updated_user = user_service.update_user(user_id, aka=aka, password=password)
        
        return jsonify({
            'success': True,
            'message': 'Usuario actualizado exitosamente',
            'data': {
                'UserId': updated_user.UserId,
                'AKA': updated_user.AKA,
                'CreatedAt': updated_user.CreatedAt.isoformat() if updated_user.CreatedAt else None
            }
        }), 200
    except Exception as e:
        error_msg = str(e)
        status_code = 404 if 'no existe' in error_msg else (400 if 'ya existe' in error_msg else 500)
        return jsonify({
            'success': False,
            'error': error_msg
        }), status_code


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Eliminar un usuario (soft delete)',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a eliminar'
        }
    ],
    'responses': {
        200: {'description': 'Usuario eliminado'},
        404: {'description': 'Usuario no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_user(user_id):
    """Elimina un usuario (soft delete)"""
    try:
        user_service.delete_user(user_id)
        
        return jsonify({
            'success': True,
            'message': f'Usuario con ID {user_id} eliminado exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@user_bp.route('/users/<int:user_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Restaurar un usuario eliminado',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del usuario a restaurar'
        }
    ],
    'responses': {
        200: {'description': 'Usuario restaurado'},
        404: {'description': 'Usuario no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def restore_user(user_id):
    """Restaura un usuario eliminado"""
    try:
        restored_user = user_service.restore_user(user_id)
        
        return jsonify({
            'success': True,
            'message': f'Usuario con ID {user_id} restaurado exitosamente',
            'data': {
                'UserId': restored_user.UserId,
                'AKA': restored_user.AKA,
                'IsDeleted': restored_user.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code