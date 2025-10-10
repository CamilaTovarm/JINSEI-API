from Repositories.SessionRepository import SessionRepository

class SessionService:
    def __init__(self):
        self._sessionRepository = SessionRepository()

    def get_all_sessions(self):
        return self._sessionRepository.get_all()

    def get_session_by_id(self, session_id):
        return self._sessionRepository.get_by_id(session_id)

    def create_session(self, user_id, start_time, end_time=None, risk_level_id=None, final_risk_level=None):
        return self._sessionRepository.create(user_id, start_time, end_time, risk_level_id, final_risk_level)

    def update_session(self, session_id, user_id=None, start_time=None, end_time=None, risk_level_id=None, final_risk_level=None):
        session = self._sessionRepository.get_by_id(session_id)
        if not session:
            raise Exception(f"The session with ID {session_id} doesn't exist.")

        if user_id is not None:
            session.UserId = user_id
        if start_time is not None:
            session.StartTime = start_time
        if end_time is not None:
            session.EndTime = end_time
        if risk_level_id is not None:
            session.RiskLevelId = risk_level_id
        if final_risk_level is not None:
            session.FinalRiskLevel = final_risk_level

        return self._sessionRepository.update(session)

    def delete_session(self, session_id):
        """Soft delete"""
        session_to_delete = self._sessionRepository.get_by_id(session_id)
        if not session_to_delete:
            raise Exception(f"The session with ID {session_id} doesn't exist.")

        session_to_delete.IsDeleted = True
        return self._sessionRepository.delete(session_to_delete)
