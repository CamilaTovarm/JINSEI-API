from Models.User import User
from Models.Database import db
from werkzeug.security import generate_password_hash, check_password_hash

class UserRepository:

    def get_all(self):
        return User.query.all()

    def get_by_id(self, user_id: int):
        return User.query.get(user_id)

    def get_by_alias(self, alias: str):
        return User.query.filter_by(alias=alias).first()

    def create(self, alias: str, password: str):
        hashed = generate_password_hash(password)
        user = User(alias=alias, password_hash=hashed)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_id: int, alias=None, password=None):
        user = self.get_by_id(user_id)
        if not user:
            return None
        if alias:
            user.alias = alias
        if password:
            user.password_hash = generate_password_hash(password)
        db.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True
