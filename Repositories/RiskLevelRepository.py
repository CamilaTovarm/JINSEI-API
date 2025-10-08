from Models.RiskLevel import RiskLevel
from Models.Database import db

class RiskLevelRepository:

    def get_all(self):
        return RiskLevel.query.all()

    def get_by_id(self, id):
        return RiskLevel.query.get(id)

    def create(self, name, description):
        rl = RiskLevel(name=name, description=description)
        db.session.add(rl)
        db.session.commit()
        return rl

    def update(self, id, name=None, description=None):
        rl = self.get_by_id(id)
        if not rl:
            return None
        if name: rl.name = name
        if description: rl.description = description
        db.session.commit()
        return rl

    def delete(self, id):
        rl = self.get_by_id(id)
        if not rl:
            return False
        db.session.delete(rl)
        db.session.commit()
        return True
