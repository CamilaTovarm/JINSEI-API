from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.ContactTypeService import ContactTypeService

contact_type_bp = Blueprint('contact_types', __name__)
contact_type_service = ContactTypeService()

@contact_type_bp.route('/contact-types', methods=['GET'])
@swag_from({
    'tags': ['Contact Types'],
    'summary': 'Obtener todos los tipos de contacto',
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
        200: {'description': 'Lista de tipos de contacto'},
        500: {'description': 'Error del servidor'}
    }
})
def get_all_contact_types():

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        contact_types = contact_type_service.get_all_contact_types(include_deleted=include_deleted)
        
        contact_types_data = [{
            'ContactTypeId': ct.ContactTypeId,
            'Description': ct.Description,
            'IsDeleted': ct.IsDeleted
        } for ct in contact_types]
        
        return jsonify({
            'success': True,
            'data': contact_types_data,
            'count': len(contact_types_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@contact_type_bp.route('/contact-types/<int:contact_type_id>', methods=['GET'])
@swag_from({
    'tags': ['Contact Types'],
    'summary': 'Obtener un tipo de contacto por ID',
    'parameters': [
        {
            'name': 'contact_type_id',
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
        200: {'description': 'Tipo de contacto encontrado'},
        404: {'description': 'Tipo de contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_contact_type_by_id(contact_type_id):

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        contact_type = contact_type_service.get_contact_type_by_id(contact_type_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'ContactTypeId': contact_type.ContactTypeId,
                'Description': contact_type.Description,
                'IsDeleted': contact_type.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_type_bp.route('/contact-types', methods=['POST'])
@swag_from({
    'tags': ['Contact Types'],
    'summary': 'Crear un nuevo tipo de contacto',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['description'],
                'properties': {
                    'description': {
                        'type': 'string',
                        'example': 'Email',
                        'description': 'Descripción del tipo de contacto'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Tipo de contacto creado'},
        400: {'description': 'Datos inválidos'},
        500: {'description': 'Error del servidor'}
    }
})
def create_contact_type():

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        description = data.get('description')
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'El campo "description" es requerido'
            }), 400
        
        new_contact_type = contact_type_service.create_contact_type(description)
        
        return jsonify({
            'success': True,
            'message': 'Tipo de contacto creado exitosamente',
            'data': {
                'ContactTypeId': new_contact_type.ContactTypeId,
                'Description': new_contact_type.Description
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@contact_type_bp.route('/contact-types/<int:contact_type_id>', methods=['PUT'])
@swag_from({
    'tags': ['Contact Types'],
    'summary': 'Actualizar un tipo de contacto',
    'parameters': [
        {
            'name': 'contact_type_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['description'],
                'properties': {
                    'description': {'type': 'string', 'example': 'Teléfono Móvil'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Tipo de contacto actualizado'},
        404: {'description': 'Tipo de contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_contact_type(contact_type_id):

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        description = data.get('description')
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'El campo "description" es requerido'
            }), 400
        
        updated_contact_type = contact_type_service.update_contact_type(contact_type_id, description)
        
        return jsonify({
            'success': True,
            'message': 'Tipo de contacto actualizado exitosamente',
            'data': {
                'ContactTypeId': updated_contact_type.ContactTypeId,
                'Description': updated_contact_type.Description
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_type_bp.route('/contact-types/<int:contact_type_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Contact Types'],
    'summary': 'Eliminar un tipo de contacto (soft delete)',
    'parameters': [
        {
            'name': 'contact_type_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Tipo de contacto eliminado'},
        404: {'description': 'Tipo de contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_contact_type(contact_type_id):

    try:
        contact_type_service.delete_contact_type(contact_type_id)
        
        return jsonify({
            'success': True,
            'message': f'Tipo de contacto con ID {contact_type_id} eliminado exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_type_bp.route('/contact-types/<int:contact_type_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Contact Types'],
    'summary': 'Restaurar un tipo de contacto eliminado',
    'parameters': [
        {
            'name': 'contact_type_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Tipo de contacto restaurado'},
        404: {'description': 'Tipo de contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def restore_contact_type(contact_type_id):

    try:
        restored_contact_type = contact_type_service.restore_contact_type(contact_type_id)
        
        return jsonify({
            'success': True,
            'message': f'Tipo de contacto con ID {contact_type_id} restaurado exitosamente',
            'data': {
                'ContactTypeId': restored_contact_type.ContactTypeId,
                'IsDeleted': restored_contact_type.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code