from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.ContactService import ContactService

contact_bp = Blueprint('contacts', __name__)
contact_service = ContactService()

@contact_bp.route('/contacts', methods=['GET'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Obtener todos los contactos',
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
        200: {'description': 'Lista de contactos'},
        500: {'description': 'Error del servidor'}
    }
})
def get_all_contacts():

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        contacts = contact_service.get_all_contacts(include_deleted=include_deleted)
        
        contacts_data = [{
            'ContactId': contact.ContactId,
            'ContactTypeId': contact.ContactTypeId,
            'Description': contact.Description,  # Email o teléfono
            'CreatedAt': contact.CreatedAt.isoformat() if contact.CreatedAt else None,
            'IsDeleted': contact.IsDeleted
        } for contact in contacts]
        
        return jsonify({
            'success': True,
            'data': contacts_data,
            'count': len(contacts_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@contact_bp.route('/contacts/<int:contact_id>', methods=['GET'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Obtener un contacto por ID',
    'parameters': [
        {
            'name': 'contact_id',
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
        200: {'description': 'Contacto encontrado'},
        404: {'description': 'Contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_contact_by_id(contact_id):

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        contact = contact_service.get_contact_by_id(contact_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'ContactId': contact.ContactId,
                'ContactTypeId': contact.ContactTypeId,
                'Description': contact.Description,
                'CreatedAt': contact.CreatedAt.isoformat() if contact.CreatedAt else None,
                'IsDeleted': contact.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_bp.route('/contact-types/<int:contact_type_id>/contacts', methods=['GET'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Obtener contactos por tipo',
    'parameters': [
        {
            'name': 'contact_type_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID del tipo de contacto (1=Email, 2=Teléfono, etc.)'
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
        200: {'description': 'Lista de contactos del tipo especificado'},
        404: {'description': 'Tipo de contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_contacts_by_type(contact_type_id):

    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        contacts = contact_service.get_contacts_by_type(contact_type_id, include_deleted=include_deleted)
        
        contacts_data = [{
            'ContactId': contact.ContactId,
            'ContactTypeId': contact.ContactTypeId,
            'Description': contact.Description,
            'CreatedAt': contact.CreatedAt.isoformat() if contact.CreatedAt else None,
            'IsDeleted': contact.IsDeleted
        } for contact in contacts]
        
        return jsonify({
            'success': True,
            'data': contacts_data,
            'count': len(contacts_data)
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_bp.route('/contacts', methods=['POST'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Crear un nuevo contacto',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['contact_type_id', 'value'],
                'properties': {
                    'contact_type_id': {
                        'type': 'integer',
                        'example': 1,
                        'description': 'ID del tipo de contacto (1=Email, 2=Teléfono)'
                    },
                    'value': {
                        'type': 'string',
                        'example': 'ejemplo@email.com',
                        'description': 'Valor del contacto (email o teléfono)'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Contacto creado'},
        400: {'description': 'Datos inválidos'},
        500: {'description': 'Error del servidor'}
    }
})
def create_contact():

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        contact_type_id = data.get('contact_type_id')
        value = data.get('value')
        
        if not contact_type_id or not value:
            return jsonify({
                'success': False,
                'error': 'Los campos "contact_type_id" y "value" son requeridos'
            }), 400
        
        new_contact = contact_service.create_contact(contact_type_id, value)
        
        return jsonify({
            'success': True,
            'message': 'Contacto creado exitosamente',
            'data': {
                'ContactId': new_contact.ContactId,
                'ContactTypeId': new_contact.ContactTypeId,
                'Description': new_contact.Description,
                'CreatedAt': new_contact.CreatedAt.isoformat() if new_contact.CreatedAt else None
            }
        }), 201
    except Exception as e:
        error_msg = str(e)
        status_code = 404 if 'no existe' in error_msg else (400 if 'válido' in error_msg else 500)
        return jsonify({
            'success': False,
            'error': error_msg
        }), status_code


@contact_bp.route('/contacts/<int:contact_id>', methods=['PUT'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Actualizar un contacto',
    'parameters': [
        {
            'name': 'contact_id',
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
                    'contact_type_id': {'type': 'integer'},
                    'value': {'type': 'string', 'description': 'Nuevo email o teléfono'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Contacto actualizado'},
        404: {'description': 'Contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_contact(contact_id):

    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionaron datos'
            }), 400
        
        contact_type_id = data.get('contact_type_id')
        value = data.get('value')
        
        updated_contact = contact_service.update_contact(
            contact_id=contact_id,
            contact_type_id=contact_type_id,
            value=value
        )
        
        return jsonify({
            'success': True,
            'message': 'Contacto actualizado exitosamente',
            'data': {
                'ContactId': updated_contact.ContactId,
                'ContactTypeId': updated_contact.ContactTypeId,
                'Description': updated_contact.Description
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else (400 if 'válido' in str(e) else 500)
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Eliminar un contacto (soft delete)',
    'parameters': [
        {
            'name': 'contact_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Contacto eliminado'},
        404: {'description': 'Contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_contact(contact_id):

    try:
        contact_service.delete_contact(contact_id)
        
        return jsonify({
            'success': True,
            'message': f'Contacto con ID {contact_id} eliminado exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@contact_bp.route('/contacts/<int:contact_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Contacts'],
    'summary': 'Restaurar un contacto eliminado',
    'parameters': [
        {
            'name': 'contact_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Contacto restaurado'},
        404: {'description': 'Contacto no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def restore_contact(contact_id):

    try:
        restored_contact = contact_service.restore_contact(contact_id)
        
        return jsonify({
            'success': True,
            'message': f'Contacto con ID {contact_id} restaurado exitosamente',
            'data': {
                'ContactId': restored_contact.ContactId,
                'IsDeleted': restored_contact.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code