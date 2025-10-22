from flask import Blueprint, request, jsonify
from Services.ContactTypeService import ContactTypeService

contact_type_bp = Blueprint("contact_type", __name__)
contact_type_service = ContactTypeService()

@contact_type_bp.route("/contact-types", methods=["GET"])
def get_all_contact_types():
    types = contact_type_service.get_all_contact_types()
    return jsonify([t.to_dict() for t in types]), 200

@contact_type_bp.route("/contact-types/<int:id>", methods=["GET"])
def get_contact_type_by_id(id):
    ctype = contact_type_service.get_contact_type_by_id(id)
    if not ctype:
        return jsonify({"error": "Contact type not found"}), 404
    return jsonify(ctype.to_dict()), 200

@contact_type_bp.route("/contact-types", methods=["POST"])
def create_contact_type():
    data = request.get_json()
    try:
        new_type = contact_type_service.create_contact_type(
            name=data["name"]
        )
        return jsonify(new_type.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
