from flask import Blueprint, request, jsonify
from Services.UserService import UserService

user_bp = Blueprint("user", __name__)
user_service = UserService()

@user_bp.route("/users", methods=["GET"])
def get_all_users():
    users = user_service.get_all_users()
    return jsonify([u.to_dict() for u in users]), 200

@user_bp.route("/users/<int:id>", methods=["GET"])
def get_user_by_id(id):
    user = user_service.get_user_by_id(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    try:
        new_user = user_service.create_user(
            username=data["username"],
            password=data["password"]
        )
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

