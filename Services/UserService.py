from Repositories.UserRepository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_id(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception(f"El usuario con ID {user_id} no existe.")
        return user

    def create_user(self, alias, password_hash):
        existing_user = self.user_repo.get_by_alias(alias)
        if existing_user:
            raise Exception(f"El alias '{alias}' ya está registrado.")
        return self.user_repo.create(alias, password_hash)

    def update_user(self, user_id, alias=None, password_hash=None):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception(f"El usuario con ID {user_id} no existe.")

        if alias:
            user.alias = alias
        if password_hash:
            user.password_hash = password_hash

        return self.user_repo.update(user)

    def delete_user(self, user_id):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise Exception(f"El usuario con ID {user_id} no existe.")
        
        user.is_deleted = True
        return self.user_repo.update(user)
