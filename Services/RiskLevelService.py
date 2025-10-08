from Repositories.RiskLevelRepository import RiskLevelRepository

class RiskLevelService:

    def __init__(self):
        self.repo = RiskLevelRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, risk_id):
        rl = self.repo.get_by_id(risk_id)
        if not rl:
            raise Exception("Nivel de riesgo no encontrado.")
        return rl

    def create(self, name, description):
        return self.repo.create(name, description)

    def update(self, risk_id, name=None, description=None):
        updated = self.repo.update(risk_id, name, description)
        if not updated:
            raise Exception("Nivel de riesgo no encontrado.")
        return updated

    def delete(self, risk_id):
        deleted = self.repo.delete(risk_id)
        if not deleted:
            raise Exception("Nivel de riesgo no encontrado.")
        return True
