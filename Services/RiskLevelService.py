from Repositories.RiskLevelRepository import RiskLevelRepository
from sqlalchemy.exc import SQLAlchemyError

class RiskLevelService:
    def __init__(self):
        self._risk_repository = RiskLevelRepository()

    def get_all_risklevels(self, include_deleted=False):

        try:
            return self._risk_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener niveles de riesgo: {str(e)}")

    def get_risklevel_by_id(self, risk_level_id, include_deleted=False):

        try:
            risk = self._risk_repository.get_by_id(risk_level_id, include_deleted=include_deleted)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
            return risk
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener nivel de riesgo: {str(e)}")

    def create_risklevel(self, description):

        try:
            return self._risk_repository.create(description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear nivel de riesgo: {str(e)}")

    def update_risklevel(self, risk_level_id, description):

        try:
            # Validar que el nivel de riesgo existe
            risk = self._risk_repository.get_by_id(risk_level_id)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")

            return self._risk_repository.update(risk_level_id, description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar nivel de riesgo: {str(e)}")

    def delete_risklevel(self, risk_level_id):

        try:
            risk = self._risk_repository.get_by_id(risk_level_id)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
    
            return self._risk_repository.delete(risk_level_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar nivel de riesgo: {str(e)}")
    
    def restore_risklevel(self, risk_level_id):

        try:
            risk = self._risk_repository.get_by_id(risk_level_id, include_deleted=True)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
            
            if not risk.IsDeleted:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no está eliminado.")
            
            return self._risk_repository.restore(risk_level_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar nivel de riesgo: {str(e)}")