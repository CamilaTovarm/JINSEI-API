from Repositories.SessionRepository import SessionRepository

class SessionService:
    def __init__(self):
        self.session_repo = SessionRepository()

    def get_all_sessions(self):
        return self.session_repo.get_all()

    def get_session_by_id(self, session_id):
        session = self.session_repo.get_by_id(session_id)
        if not session:
            raise Exception(f"La sesión con ID {session_id} no existe.")
        return session

    def create_session(self, user_id, start_time, end_time=None):
        return self.session_repo.create(user_id, start_time, end_time)

    def update_session(self, session_id, end_time=None):
        session = self.session_repo.get_by_id(session_id)
        if not session:
            raise Exception(f"La sesión con ID {session_id} no existe.")
        if end_time:
            session.end_time = end_time
        return self.session_repo.update(session)

    def delete_session(self, session_id):
        session = self.session_repo.get_by_id(session_id)
        if not session:
            raise Exception(f"La sesión con ID {session_id} no existe.")
        session.is_deleted = True
        return self.session_repo.update(session)
