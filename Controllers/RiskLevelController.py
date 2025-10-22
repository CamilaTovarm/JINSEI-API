from flask import Blueprint, request, jsonify
from Services.RiskLevelService import RiskLevelService

risk_level_bp = Blueprint("risk_level", __name__)
risk_level_service = RiskLevelService()

@risk_level_bp.route("/risk-levels", methods=["GET"])
def get_all_risk_levels():
    risks = risk_level_service.get_all_risk_levels()
    return jsonify([r.to_dict() for r in risks]), 200

@risk_level_bp.route("/risk-levels/<int:id>", methods=["GET"])
def get_risk_level_by_id(id):
    risk = risk_level_service.get_risk_level_by_id(id)
    if not risk:
        return jsonify({"error": "Risk level not found"}), 404
    return jsonify(risk.to_dict()), 200

@risk_level_bp.route("/risk-levels", methods=["POST"])
def create_risk_level():
    data = request.get_json()
    try:
        new_risk = risk_level_service.create_risk_level(
            name=data["name"],
            description=data.get("description")
        )
        return jsonify(new_risk.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
