from Models.Session import Session
from Models.Database import db
from datetime import datetime

class SessionRepository:

    def get_all(self):
        return Session.query.all()

    def get_by_id(self, session_id: int):
        return Session.query.get(session_id)

    def create(self, user_id: int):
        session = Session(user_id=user_id)
        db.session.add(session)
        db.session.commit()
        return session

    def update(self, session_id: int, **kwargs):
        session = self.get_by_id(session_id)
        if not session:
            return None
        for key, value in kwargs.items():
            setattr(session, key, value)
        db.session.commit()
        return session

    def delete(self, session_id: int):
        session = self.get_by_id(session_id)
        if not session:
            return False
        db.session.delete(session)
        db.session.commit()
        return True
