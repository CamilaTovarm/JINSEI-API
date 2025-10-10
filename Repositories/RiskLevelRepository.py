from ConfigDB import db
from Models.RiskLevel import RiskLevel
from sqlalchemy.exc import SQLAlchemyError

class RiskLevelRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return RiskLevel.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, risk_level_id):
        return RiskLevel.query.filter_by(RiskLevelId=risk_level_id, IsDeleted=False).first()

    def create(self, description):
        try:
            new_risk = RiskLevel(Description=description, IsDeleted=False)
            self.db.session.add(new_risk)
            self.db.session.commit()
            return new_risk
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, risk):
        existing = RiskLevel.query.get(risk.RiskLevelId)
        if not existing or existing.IsDeleted:
            return None
        existing.Description = risk.Description
        self.db.session.commit()
        return existing

    def delete(self, risk):
        try:
            self.db.session.add(risk)
            self.db.session.commit()
            return risk
        except SQLAlchemyError:
            self.db.session.rollback()
            raise
