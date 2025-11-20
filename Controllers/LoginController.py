from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.LoginService import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Iniciar sesión',
    'description': 'Autentica un usuario con su AKA (username) y contraseña',
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
                        'description': 'Nombre de usuario (AKA)'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'SecurePass123',
                        'description': 'Contraseña del usuario'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Autenticación exitosa',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': 'Inicio de sesión exitoso'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'UserId': {'type': 'integer', 'example': 1},
                            'AKA': {'type': 'string', 'example': 'john_doe'},
                            'CreatedAt': {'type': 'string', 'example': '2024-01-15T10:30:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': 'Datos incompletos o inválidos',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'error': {'type': 'string', 'example': 'Los campos "aka" y "password" son requeridos'}
                }
            }
        },
        401: {
            'description': 'Credenciales inválidas',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'error': {'type': 'string', 'example': 'Usuario o contraseña incorrectos.'}
                }
            }
        },
        500: {'description': 'Error del servidor'}
    }
})
def login():

    try:
        # Obtener datos del body
        data = request.get_json()

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

        # Validar formato de credenciales
        try:
            auth_service.validate_credentials_format(aka, password)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            }), 400

        # Autenticar usuario
        user = auth_service.authenticate_user(aka, password)

        # login exitoso
        return jsonify({
            'success': True,
            'message': 'Inicio de sesión exitoso',
            'data': {
                'UserId': user.UserId,
                'AKA': user.AKA,
                'CreatedAt': user.CreatedAt.isoformat() if user.CreatedAt else None
            }
        }), 200

    except Exception as e:
        error_msg = str(e)
        
        # Determinar el código de estado HTTP según el error
        if 'incorrectos' in error_msg or 'desactivada' in error_msg:
            status_code = 401  # Unauthorized
        else:
            status_code = 500  # Internal Server Error
        
        return jsonify({
            'success': False,
            'error': error_msg
        }), status_code


@auth_bp.route('/auth/validate-username', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Validar si un usuario existe',
    'description': 'Verifica si un AKA (username) existe en el sistema',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['aka'],
                'properties': {
                    'aka': {
                        'type': 'string',
                        'example': 'john_doe',
                        'description': 'Nombre de usuario a validar'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Usuario existe',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'exists': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Datos incompletos'},
        500: {'description': 'Error del servidor'}
    }
})
def validate_username():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400

        aka = data.get('aka')

        if not aka:
            return jsonify({
                'success': False,
                'error': 'El campo "aka" es requerido'
            }), 400

        # Intentar buscar el usuario
        try:
            user = auth_service.get_user_by_aka(aka)
            
            # el usuario existe
            return jsonify({
                'success': True,
                'exists': True,
                'message': f'El usuario "{aka}" ya existe'
            }), 200

        except Exception as e:
            if 'no existe' in str(e):
                # El usuario NO existe
                return jsonify({
                    'success': True,
                    'exists': False,
                    'message': f'El usuario "{aka}" está disponible'
                }), 200
            else:
                # Otro tipo de error
                raise e

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@auth_bp.route('/auth/check-username/<string:aka>', methods=['GET'])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Verificar disponibilidad de username (método GET)',
    'description': 'Verifica si un AKA está disponible para registro',
    'parameters': [
        {
            'name': 'aka',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Nombre de usuario a verificar'
        }
    ],
    'responses': {
        200: {
            'description': 'Verificación completada',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'available': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        500: {'description': 'Error del servidor'}
    }
})
def check_username_availability(aka):
    """
    Verifica si un AKA está disponible (alternativa GET).
    
    Endpoint útil para verificar en tiempo real mientras el usuario escribe.
    """
    try:
        # Intentar obtener el usuario
        user = auth_service.get_user_by_aka(aka)
        
        # Si llega aquí, el usuario existe
        return jsonify({
            'success': True,
            'available': False,
            'message': f'El usuario "{aka}" ya está en uso'
        }), 200

    except Exception as e:
        error_msg = str(e)
        
        if 'no existe' in error_msg:
            # El usuario NO existe, está disponible
            return jsonify({
                'success': True,
                'available': True,
                'message': f'El usuario "{aka}" está disponible'
            }), 200
        else:
            # Error del servidor
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500