from flask import Blueprint, request, jsonify
from Services.ConsentService import ConsentService

consent_bp = Blueprint("consent", __name__)
consent_service = ConsentService()

@consent_bp.route("/consents", methods=["GET"])
def get_all_consents():
    consents = consent_service.get_all_consents()
    return jsonify([c.to_dict() for c in consents]), 200


@consent_bp.route("/consents/<int:consent_id>", methods=["GET"])
def get_consent_by_id(consent_id):
    consent = consent_service.get_consent_by_id(consent_id)
    if not consent:
        return jsonify({"error": "Consent not found"}), 404
    return jsonify(consent.to_dict()), 200


@consent_bp.route("/consents", methods=["POST"])
def create_consent():
    data = request.get_json()
    try:
        new_consent = consent_service.create_consent(
            session_id=data["session_id"],
            full_name=data["full_name"],
            document_type_id=data["document_type_id"],
            document_number=data["document_number"],
            email=data["email"],
            phone=data["phone"]
        )
        return jsonify(new_consent.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@consent_bp.route("/consents/<int:consent_id>", methods=["PUT"])
def update_consent(consent_id):
    data = request.get_json()
    try:
        updated_consent = consent_service.update_consent(
            consent_id,
            session_id=data.get("session_id"),
            full_name=data.get("full_name"),
            document_type_id=data.get("document_type_id"),
            document_number=data.get("document_number")
        )
        return jsonify(updated_consent.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@consent_bp.route("/consents/<int:consent_id>", methods=["DELETE"])
def delete_consent(consent_id):
    try:
        deleted_consent = consent_service.delete_consent(consent_id)
        return jsonify(deleted_consent.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
