from ConfigDB import db
from Models.RiskLevel import RiskLevel
from sqlalchemy.exc import SQLAlchemyError

class RiskLevelRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):

        if include_deleted:
            return RiskLevel.query.all()
        return RiskLevel.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, risk_level_id, include_deleted=False):

        if include_deleted:
            return RiskLevel.query.filter_by(RiskLevelId=risk_level_id).first()
        return RiskLevel.query.filter_by(RiskLevelId=risk_level_id, IsDeleted=False).first()

    def create(self, description):

        try:
            new_risk = RiskLevel(description=description, IsDeleted=False)
            self.db.session.add(new_risk)
            self.db.session.commit()
            return new_risk
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, risk_level_id, description):

        try:
            existing = RiskLevel.query.get(risk_level_id)
            if not existing or existing.IsDeleted:
                return None
            
            existing.description = description
            self.db.session.commit()
            return existing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete(self, risk_level_id):

        try:
            risk = RiskLevel.query.get(risk_level_id)
            if not risk:
                return None
            
            risk.IsDeleted = True
            self.db.session.commit()
            return risk
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
    
    def restore(self, risk_level_id):

        try:
            risk = RiskLevel.query.get(risk_level_id)
            if not risk:
                return None
            
            risk.IsDeleted = False
            self.db.session.commit()
            return risk
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e