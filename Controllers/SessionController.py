from flask import Blueprint, request, jsonify
from Services.SessionService import SessionService

session_bp = Blueprint("session", __name__)
session_service = SessionService()

@session_bp.route("/sessions", methods=["GET"])
def get_all_sessions():
    sessions = session_service.get_all_sessions()
    return jsonify([s.to_dict() for s in sessions]), 200

@session_bp.route("/sessions/<int:id>", methods=["GET"])
def get_session_by_id(id):
    session = session_service.get_session_by_id(id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(session.to_dict()), 200

@session_bp.route("/sessions", methods=["POST"])
def create_session():
    data = request.get_json()
    try:
        new_session = session_service.create_session(
            user_id=data["user_id"]
        )
        return jsonify(new_session.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
