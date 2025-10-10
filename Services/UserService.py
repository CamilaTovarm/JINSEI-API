from Repositories.UserRepository import UserRepository
from Models.User import User
from datetime import datetime

class UserService():
    def __init__(self):
        self._user_repository = UserRepository()

    def get_all_users(self):
        return self._user_repository.get_all()

    def get_user_by_id(self, user_id):
        return self._user_repository.get_by_id(user_id)

    def create_user(self, aka, password):
        return self._user_repository.create(aka, password)

    def update_user(self, user_id, aka=None, password=None):
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise Exception(f"The user with ID {user_id} doesn't exist.")

        if aka is not None:
            user.AKA = aka
        if password is not None:
            user.Password = password

        return self._user_repository.update(user)

    def delete_user(self, user_id):
        user_to_delete = self._user_repository.get_by_id(user_id)
        if not user_to_delete:
            raise Exception(f"The user with ID {user_id} doesn't exist.")

        user_to_delete.IsDeleted = True

        return self._user_repository.delete(user_to_delete)
