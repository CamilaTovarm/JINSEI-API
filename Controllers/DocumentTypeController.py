from flask import Blueprint, request, jsonify
from Services.DocumentTypeService import DocumentTypeService

document_type_bp = Blueprint("document_type", __name__)
document_type_service = DocumentTypeService()

@document_type_bp.route("/document-types", methods=["GET"])
def get_all_document_types():
    types = document_type_service.get_all_document_types()
    return jsonify([t.to_dict() for t in types]), 200

@document_type_bp.route("/document-types/<int:id>", methods=["GET"])
def get_document_type_by_id(id):
    doc_type = document_type_service.get_document_type_by_id(id)
    if not doc_type:
        return jsonify({"error": "Document type not found"}), 404
    return jsonify(doc_type.to_dict()), 200

@document_type_bp.route("/document-types", methods=["POST"])
def create_document_type():
    data = request.get_json()
    try:
        new_type = document_type_service.create_document_type(
            name=data["name"],
            description=data.get("description")
        )
        return jsonify(new_type.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
