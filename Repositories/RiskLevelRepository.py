from ConfigDB import db
from Models.RiskLevel import RiskLevel
from sqlalchemy.exc import SQLAlchemyError

class RiskLevelRepository:
    def __init__(self):
        self.db = db

    def get_all(self, include_deleted=False):
        """Obtiene todos los niveles de riesgo"""
        if include_deleted:
            return RiskLevel.query.all()
        return RiskLevel.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, risk_level_id, include_deleted=False):
        """Obtiene un nivel de riesgo por ID"""
        if include_deleted:
            return RiskLevel.query.filter_by(RiskLevelId=risk_level_id).first()
        return RiskLevel.query.filter_by(RiskLevelId=risk_level_id, IsDeleted=False).first()

    def create(self, description):
        """Crea un nuevo nivel de riesgo"""
        try:
            new_risk = RiskLevel(description=description, IsDeleted=False)
            self.db.session.add(new_risk)
            self.db.session.commit()
            return new_risk
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update(self, risk_level_id, description):
        """Actualiza un nivel de riesgo existente"""
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
        """Marca un nivel de riesgo como eliminado (soft delete)"""
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
        """Restaura un nivel de riesgo marcado como eliminado"""
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