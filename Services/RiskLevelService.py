from Repositories.RiskLevelRepository import RiskLevelRepository
from sqlalchemy.exc import SQLAlchemyError

class RiskLevelService:
    def __init__(self):
        self._risk_repository = RiskLevelRepository()

    def get_all_risklevels(self, include_deleted=False):
        """Obtiene todos los niveles de riesgo"""
        try:
            return self._risk_repository.get_all(include_deleted=include_deleted)
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener niveles de riesgo: {str(e)}")

    def get_risklevel_by_id(self, risk_level_id, include_deleted=False):
        """Obtiene un nivel de riesgo por ID"""
        try:
            risk = self._risk_repository.get_by_id(risk_level_id, include_deleted=include_deleted)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
            return risk
        except SQLAlchemyError as e:
            raise Exception(f"Error al obtener nivel de riesgo: {str(e)}")

    def create_risklevel(self, description):
        """Crea un nuevo nivel de riesgo"""
        try:
            return self._risk_repository.create(description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al crear nivel de riesgo: {str(e)}")

    def update_risklevel(self, risk_level_id, description):
        """Actualiza un nivel de riesgo existente"""
        try:
            # Validar que el nivel de riesgo existe
            risk = self._risk_repository.get_by_id(risk_level_id)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
            
            # ✅ Ahora pasamos los parámetros directamente
            return self._risk_repository.update(risk_level_id, description)
        except SQLAlchemyError as e:
            raise Exception(f"Error al actualizar nivel de riesgo: {str(e)}")

    def delete_risklevel(self, risk_level_id):
        """Marca un nivel de riesgo como eliminado (soft delete)"""
        try:
            risk = self._risk_repository.get_by_id(risk_level_id)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
            
            # ✅ Solo pasamos el ID
            return self._risk_repository.delete(risk_level_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al eliminar nivel de riesgo: {str(e)}")
    
    def restore_risklevel(self, risk_level_id):
        """Restaura un nivel de riesgo marcado como eliminado"""
        try:
            risk = self._risk_repository.get_by_id(risk_level_id, include_deleted=True)
            if not risk:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no existe.")
            
            if not risk.IsDeleted:
                raise Exception(f"El nivel de riesgo con ID {risk_level_id} no está eliminado.")
            
            return self._risk_repository.restore(risk_level_id)
        except SQLAlchemyError as e:
            raise Exception(f"Error al restaurar nivel de riesgo: {str(e)}")