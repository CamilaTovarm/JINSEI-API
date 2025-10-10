from Repositories.RiskLevelRepository import RiskLevelRepository

class RiskLevelService:
    def __init__(self):
        self._risk_repository = RiskLevelRepository()

    def get_all_risklevels(self):
        return self._risk_repository.get_all()

    def get_risklevel_by_id(self, risk_level_id):
        return self._risk_repository.get_by_id(risk_level_id)

    def create_risklevel(self, description):
        return self._risk_repository.create(description)

    def update_risklevel(self, risk_level_id, description=None):
        risk = self._risk_repository.get_by_id(risk_level_id)
        if not risk:
            raise Exception(f"The risk level with ID {risk_level_id} doesn't exist.")
        if description is not None:
            risk.Description = description
        return self._risk_repository.update(risk)

    def delete_risklevel(self, risk_level_id):
        risk_to_delete = self._risk_repository.get_by_id(risk_level_id)
        if not risk_to_delete:
            raise Exception(f"The risk level with ID {risk_level_id} doesn't exist.")
        risk_to_delete.IsDeleted = True
        return self._risk_repository.delete(risk_to_delete)
