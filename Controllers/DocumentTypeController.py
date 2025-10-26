from flask import Blueprint, request, jsonify
from flasgger import swag_from
from Services.DocumentTypeService import DocumentTypeService

document_type_bp = Blueprint('document_types', __name__)
document_type_service = DocumentTypeService()

@document_type_bp.route('/document-types', methods=['GET'])
@swag_from({
    'tags': ['Document Types'],
    'summary': 'Obtener todos los tipos de documento',
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
        200: {'description': 'Lista de tipos de documento'},
        500: {'description': 'Error del servidor'}
    }
})
def get_all_document_types():
    """Obtiene todos los tipos de documento"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        document_types = document_type_service.get_all_document_types(include_deleted=include_deleted)
        
        document_types_data = [{
            'DocumentTypeId': dt.DocumentTypeId,
            'Description': dt.Description,
            'IsDeleted': dt.IsDeleted
        } for dt in document_types]
        
        return jsonify({
            'success': True,
            'data': document_types_data,
            'count': len(document_types_data)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@document_type_bp.route('/document-types/<int:document_type_id>', methods=['GET'])
@swag_from({
    'tags': ['Document Types'],
    'summary': 'Obtener un tipo de documento por ID',
    'parameters': [
        {
            'name': 'document_type_id',
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
        200: {'description': 'Tipo de documento encontrado'},
        404: {'description': 'Tipo de documento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def get_document_type_by_id(document_type_id):
    """Obtiene un tipo de documento por ID"""
    try:
        include_deleted = request.args.get('include_deleted', 'false').lower() == 'true'
        document_type = document_type_service.get_document_type_by_id(document_type_id, include_deleted=include_deleted)
        
        return jsonify({
            'success': True,
            'data': {
                'DocumentTypeId': document_type.DocumentTypeId,
                'Description': document_type.Description,
                'IsDeleted': document_type.IsDeleted
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@document_type_bp.route('/document-types', methods=['POST'])
@swag_from({
    'tags': ['Document Types'],
    'summary': 'Crear un nuevo tipo de documento',
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
                        'example': 'Cédula de Ciudadanía',
                        'description': 'Descripción del tipo de documento'
                    }
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Tipo de documento creado'},
        400: {'description': 'Datos inválidos'},
        500: {'description': 'Error del servidor'}
    }
})
def create_document_type():
    """Crea un nuevo tipo de documento"""
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
        
        new_document_type = document_type_service.create_document_type(description)
        
        return jsonify({
            'success': True,
            'message': 'Tipo de documento creado exitosamente',
            'data': {
                'DocumentTypeId': new_document_type.DocumentTypeId,
                'Description': new_document_type.Description
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@document_type_bp.route('/document-types/<int:document_type_id>', methods=['PUT'])
@swag_from({
    'tags': ['Document Types'],
    'summary': 'Actualizar un tipo de documento',
    'parameters': [
        {
            'name': 'document_type_id',
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
                    'description': {'type': 'string', 'example': 'Pasaporte'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Tipo de documento actualizado'},
        404: {'description': 'Tipo de documento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def update_document_type(document_type_id):
    """Actualiza un tipo de documento"""
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
        
        updated_document_type = document_type_service.update_document_type(document_type_id, description)
        
        return jsonify({
            'success': True,
            'message': 'Tipo de documento actualizado exitosamente',
            'data': {
                'DocumentTypeId': updated_document_type.DocumentTypeId,
                'Description': updated_document_type.Description
            }
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@document_type_bp.route('/document-types/<int:document_type_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Document Types'],
    'summary': 'Eliminar un tipo de documento (soft delete)',
    'parameters': [
        {
            'name': 'document_type_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Tipo de documento eliminado'},
        404: {'description': 'Tipo de documento no encontrado'},
        500: {'description': 'Error del servidor'}
    }
})
def delete_document_type(document_type_id):
    """Elimina un tipo de documento (soft delete)"""
    try:
        document_type_service.delete_document_type(document_type_id)
        
        return jsonify({
            'success': True,
            'message': f'Tipo de documento con ID {document_type_id} eliminado exitosamente'
        }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code


@document_type_bp.route('/document-types/<int:document_type_id>/restore', methods=['POST'])
@swag_from({
    'tags': ['Document Types'],
    'summary': 'Restaurar un tipo de documento eliminado',
    'parameters': [
        {
            'name': 'document_type_id',
            'in': 'path',
            'type': 'integer',
            'required': True
        }
    ],
    'responses': {
        200: {'description': 'Tipo de documento restaurado'},
        404: {'description': 'Tipo de documento no encontrado'},
        500: {'description': 'Error del servidor'}
        }
    })

def restore_document_type(document_type_id):
    """Restaura un tipo de documento eliminado"""
    try:
        restored_document_type = document_type_service.restore_document_type(document_type_id)
        return jsonify({
        'success': True,
        'message': f'Tipo de documento con ID {document_type_id} restaurado exitosamente',
        'data': {
            'DocumentTypeId': restored_document_type.DocumentTypeId,
            'IsDeleted': restored_document_type.IsDeleted
        }
    }), 200
    except Exception as e:
        status_code = 404 if 'no existe' in str(e) else 500
        return jsonify({
            'success': False,
            'error': str(e)
        }), status_code