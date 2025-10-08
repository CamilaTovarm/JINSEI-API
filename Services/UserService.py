from Repositories.UserRepository import UserRepository

class UserService:

    def __init__(self):
        self.repo = UserRepository()

    def get_all(self):
        return self.repo.get_all()

    def get_by_id(self, user_id):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("Usuario no encontrado.")
        return user

    def create(self, alias, password):
        if self.repo.get_by_alias(alias):
            raise Exception("El alias ya está en uso.")
        return self.repo.create(alias, password)

    def update(self, user_id, alias=None, password=None):
        updated = self.repo.update(user_id, alias, password)
        if not updated:
            raise Exception("Usuario no encontrado para actualizar.")
        return updated

    def delete(self, user_id):
        deleted = self.repo.delete(user_id)
        if not deleted:
            raise Exception("Usuario no encontrado para eliminar.")
        return True
