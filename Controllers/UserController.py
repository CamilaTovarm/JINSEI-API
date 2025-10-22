from flask import Blueprint, request, jsonify
from Services.UserService import UserService

user_bp = Blueprint('users', __name__, url_prefix='/api/users')
user_service = UserService()

@user_bp.get('/')
def get_all_users():
    try:
        users = user_service.get_all_users()
        return jsonify([u.to_dict() for u in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@user_bp.get('/<int:user_id>')
def get_user_by_id(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@user_bp.post('/')
def create_user():
    data = request.json
    if not data or 'AKA' not in data or 'Password' not in data:
        return jsonify({"error": "AKA and Password are required"}), 400

    user = user_service.create_user(data['AKA'], data['Password'])
    return jsonify(user.to_dict()), 201

@user_bp.put('/<int:user_id>')
def update_user(user_id):
    data = request.json
    updated = user_service.update_user(user_id, aka=data.get('AKA'), password=data.get('Password'))
    return jsonify(updated.to_dict()), 200

@user_bp.delete('/<int:user_id>')
def delete_user(user_id):
    deleted = user_service.delete_user(user_id)
    return jsonify(deleted.to_dict()), 200
