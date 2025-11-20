from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.ConsentService import ConsentService

consent_bp = Blueprint('consents', __name__)
consent_service = ConsentService()

@consent_bp.route('/consents', methods=['GET'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Obtener todos los consentimientos',
    'parameters': [
        {
            'name': 'include_deleted',
            'in': 'query',
            'type': 'boolean',
            'required': False,
            'default': False
        }
    ],
    'responses': {
        200: {'description': 'Lista de consentimientos'},
        500: {'description': 'Error del servidor'}
    }
})
def get_all_consents():

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        consents = consent_service.get_all_consents(include_deleted=include_deleted)
        
        consents_data = [{
            'ConsentId': consent.ConsentId,
            'SessionId': consent.SessionId,
            'FullName': consent.FullName,
            'DocumentTypeId': consent.DocumentTypeId,
            'DocumentNumber': consent.DocumentNumber,
            'CreatedAt': consent.CreatedAt.isoformat() if consent.CreatedAt else None,
            'IsDeleted': consent.IsDeleted
        } for consent in consents]
        
        return jsonify({
            'success': True,
            'data': consents_data,
            'count': len(consents_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@consent_bp.route('/consents/<int:consent_id>', methods=['GET'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Obtener un consentimiento por ID',
    'parameters': [
        {
            'name': 'consent_id',
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
        200: {'description': 'Consentimiento encontrado'},
        404: {'description': 'Consentimiento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_consent_by_id(consent_id):

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        consent = consent_service.get_consent_by_id(consent_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'ConsentId': consent.ConsentId,
                'SessionId': consent.SessionId,
                'FullName': consent.FullName,
                'DocumentTypeId': consent.DocumentTypeId,
                'DocumentNumber': consent.DocumentNumber,
                'CreatedAt': consent.CreatedAt.isoformat() if consent.CreatedAt else None,
                'IsDeleted': consent.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@consent_bp.route('/sessions/<int:session_id>/consents', methods=['GET'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Obtener todos los consentimientos de una sesión',
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
        200: {'description': 'Lista de consentimientos de la sesión'},
        404: {'description': 'Sesión no encontrada'},
        500: {'description': 'Error del servidor'}
    }
})
def get_consents_by_session(session_id):

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        consents = consent_service.get_consents_by_session(session_id, include_deleted=include_deleted)
        
        consents_data = [{
            'ConsentId': consent.ConsentId,
            'SessionId': consent.SessionId,
            'FullName': consent.FullName,
            'DocumentTypeId': consent.DocumentTypeId,
            'DocumentNumber': consent.DocumentNumber,
            'CreatedAt': consent.CreatedAt.isoformat() if consent.CreatedAt else None,
            'IsDeleted': consent.IsDeleted
        } for consent in consents]
        
        return jsonify({
            'success': True,
            'data': consents_data,
            'count': len(consents_data)
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@consent_bp.route('/consents', methods=['POST'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Crear un nuevo consentimiento con contactos',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['session_id', 'full_name', 'document_type_id', 'document_number', 'email', 'phone'],
                'properties': {
                    'session_id': {'type': 'integer', 'example': 1},
                    'full_name': {'type': 'string', 'example': 'Juan Pérez'},
                    'document_type_id': {'type': 'integer', 'example': 1, 'description': 'ID del tipo de documento (CC, TI, etc.)'},
                    'document_number': {'type': 'string', 'example': '1234567890'},
                    'email': {'type': 'string', 'example': 'juan.perez@email.com', 'description': 'Email del contacto'},
                    'phone': {'type': 'string', 'example': '+57 300 123 4567', 'description': 'Teléfono del contacto'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Consentimiento creado con contactos'},
        400: {'description': 'Datos inválidos'},
        500: {'description': 'Error del servidor'}
    }
})
def create_consent():

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        # Validar campos requeridos
        required_fields = ['session_id', 'full_name', 'document_type_id', 'document_number', 'email', 'phone']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }), 400
        
        new_consent = consent_service.create_consent(
            session_id=data.get('session_id'),
            full_name=data.get('full_name'),
            document_type_id=data.get('document_type_id'),
            document_number=data.get('document_number'),
            email=data.get('email'),
            phone=data.get('phone')
        )
        
        return jsonify({
            'success': True,
            'message': 'Consentimiento creado exitosamente con sus contactos',
            'data': {
                'ConsentId': new_consent.ConsentId,
                'SessionId': new_consent.SessionId,
                'FullName': new_consent.FullName,
                'DocumentTypeId': new_consent.DocumentTypeId,
                'DocumentNumber': new_consent.DocumentNumber,
                'CreatedAt': new_consent.CreatedAt.isoformat() if new_consent.CreatedAt else None
            }
        }), 201
    except Exception as e:
        error_msg = str(e)
        status_code = 404 if 'no existe' in error_msg else (400 if any(word in error_msg for word in ['ya existe', 'válido', 'formato']) else 500)
        return jsonify({
            'success': False,
            'error': error_msg
        }), status_code


@consent_bp.route('/consents/<int:consent_id>', methods=['PUT'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Actualizar un consentimiento',
    'parameters': [
        {
            'name': 'consent_id',
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
                    'session_id': {'type': 'integer'},
                    'full_name': {'type': 'string'},
                    'document_type_id': {'type': 'integer'},
                    'document_number': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Consentimiento actualizado'},
        404: {'description': 'Consentimiento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_consent(consent_id):

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        updated_consent = consent_service.update_consent(
            consent_id=consent_id,
            session_id=data.get('session_id'),
            full_name=data.get('full_name'),
            document_type_id=data.get('document_type_id'),
            document_number=data.get('document_number')
        )
        
        return jsonify({
            'success': True,
            'message': 'Consentimiento actualizado exitosamente',
            'data': {
                'ConsentId': updated_consent.ConsentId,
                'SessionId': updated_consent.SessionId,
                'FullName': updated_consent.FullName,
                'DocumentTypeId': updated_consent.DocumentTypeId,
                'DocumentNumber': updated_consent.DocumentNumber
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@consent_bp.route('/consents/<int:consent_id>/contacts', methods=['PUT'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Actualizar contactos de un consentimiento',
    'parameters': [
        {
            'name': 'consent_id',
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
                    'email': {'type': 'string', 'example': 'nuevo@email.com'},
                    'phone': {'type': 'string', 'example': '+57 310 987 6543'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Contactos actualizados'},
        404: {'description': 'Consentimiento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_consent_contacts(consent_id):

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        email = data.get('email')
        phone = data.get('phone')
        
        if not email and not phone:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar al menos email o phone'
            }), 400
        
        updated_consent = consent_service.update_consent_contacts(
            consent_id=consent_id,
            email=email,
            phone=phone
        )
        
        return jsonify({
            'success': True,
            'message': 'Contactos actualizados exitosamente',
            'data': {
                'ConsentId': updated_consent.ConsentId,
                'FullName': updated_consent.FullName
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else (400 if 'válido' in str(e) else 500)
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@consent_bp.route('/consents/<int:consent_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Eliminar un consentimiento (soft delete)',
    'parameters': [
        {
            'name': 'consent_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Consentimiento eliminado'},
        404: {'description': 'Consentimiento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_consent(consent_id):

    try:
        consent_service.delete_consent(consent_id)
        
        return jsonify({
            'success': True,
            'message': f'Consentimiento con ID {consent_id} eliminado exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@consent_bp.route('/consents/<int:consent_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Consents'],
    'summary': 'Restaurar un consentimiento eliminado',
    'parameters': [
        {
            'name': 'consent_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Consentimiento restaurado'},
        404: {'description': 'Consentimiento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def restore_consent(consent_id):

    try:
        restored_consent = consent_service.restore_consent(consent_id)
        
        return jsonify({
            'success': True,
            'message': f'Consentimiento con ID {consent_id} restaurado exitosamente',
            'data': {
                'ConsentId': restored_consent.ConsentId,
                'IsDeleted': restored_consent.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code