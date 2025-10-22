from flask import Blueprint, request, jsonify
from Services.ContactService import ContactService

contact_bp = Blueprint("contact", __name__)
contact_service = ContactService()

@contact_bp.route("/contacts", methods=["GET"])
def get_all_contacts():
    contacts = contact_service.get_all_contacts()
    return jsonify([c.to_dict() for c in contacts]), 200

@contact_bp.route("/contacts/<int:contact_id>", methods=["GET"])
def get_contact_by_id(contact_id):
    contact = contact_service.get_contact_by_id(contact_id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    return jsonify(contact.to_dict()), 200

@contact_bp.route("/contacts", methods=["POST"])
def create_contact():
    data = request.get_json()
    try:
        new_contact = contact_service.create_contact(
            contact_type_id=data["contact_type_id"],
            contact_value=data["contact_value"]
        )
        return jsonify(new_contact.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@contact_bp.route("/contacts/<int:contact_id>", methods=["PUT"])
def update_contact(contact_id):
    data = request.get_json()
    try:
        updated_contact = contact_service.update_contact(
            contact_id,
            contact_type_id=data.get("contact_type_id"),
            contact_value=data.get("contact_value")
        )
        return jsonify(updated_contact.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@contact_bp.route("/contacts/<int:contact_id>", methods=["DELETE"])
def delete_contact(contact_id):
    try:
        deleted_contact = contact_service.delete_contact(contact_id)
        return jsonify(deleted_contact.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
