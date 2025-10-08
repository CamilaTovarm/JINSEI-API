from Repositories.SessionRepository import SessionRepository

class SessionService:

    def __init__(self):
        self.repo = SessionRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, session_id):
        session = self.repo.get_by_id(session_id)
        if not session:
            raise Exception("Sesión no encontrada.")
        return session

    def create(self, user_id):
        return self.repo.create(user_id)

    def update(self, session_id, **kwargs):
        updated = self.repo.update(session_id, **kwargs)
        if not updated:
            raise Exception("Sesión no encontrada para actualizar.")
        return updated

    def delete(self, session_id):
        deleted = self.repo.delete(session_id)
        if not deleted:
            raise Exception("Sesión no encontrada para eliminar.")
        return True
