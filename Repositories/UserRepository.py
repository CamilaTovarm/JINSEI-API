# repositories/user_repository.py
from ConfigDB import db
from Models.User import User
from sqlalchemy.exc import SQLAlchemyError

class UserRepository:
    def __init__(self):
        self.db = db

    def get_all(self):
        return User.query.filter_by(IsDeleted=False).all()

    def get_by_id(self, user_id):
        return User.query.filter_by(UserId=user_id, IsDeleted=False).first()

    def create(self, aka, password):
        try:
            new_user = User(AKA=aka, Password=password, IsDeleted=False)
            self.db.session.add(new_user)
            self.db.session.commit()
            return new_user
        except SQLAlchemyError:
            self.db.session.rollback()
            raise

    def update(self, user):
        existing = User.query.get(user.UserId)
        if not existing or existing.IsDeleted:
            return None
        existing.AKA = user.AKA
        existing.Password = user.Password
        self.db.session.commit()
        return existing

    def delete(self, user):
        try:
            self.db.session.add(user)  # Attach
            self.db.session.commit()   # SaveChanges
            return user
        except SQLAlchemyError:
            self.db.session.rollback()
            raise
