from messenger.repositories.user_repo import UserRepository
from messenger.core.hashing import Hashing
from messenger.core.exceptions import UserExistsError, UserNotFoundError, UserSameStatusError, InvalidPasswordError
from messenger.enums import UserStatus


class UserService:

    def __init__(self, db):

        self.repository = UserRepository(db)


    def create_user(self, email : str, password : str, user_name : str ):

        validate = self.repository.get_user_by_email(email)
        if validate:
            raise UserExistsError()

        hashed_pw = Hashing.hash_password(password)
        return self.repository.create_user(email, hashed_pw, user_name)


    def get_user_by_email(self, email : str):

        user =  self.repository.get_user_by_email(email)
        if not user:
            raise UserNotFoundError()
        return user

    def get_user_by_id(self, user_id : int):

        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    def get_user_by_username(self, username : str):

        users = self.repository.get_user_by_username(username)
        if not users:
            raise UserNotFoundError()
        return users

    def get_all_users(self):
        return self.repository.get_all_users()


    def update_user(self, user_id : int, user_details : dict):

        user = self.repository.get_user_by_id(user_id)

        if not user:
            raise UserNotFoundError()

        allowed_keys = ['email', 'name']
        updates = {k: v for k, v in user_details.items() if k in allowed_keys}

        return self.repository.update_user(user, updates)

    def update_user_password(self, password : str, user_id : int, new_password : str):

        user = self.repository.get_user_by_id(user_id)
        user_validate = Hashing.check_password(password, user.password)
        if not user_validate:
            raise InvalidPasswordError()
        updated_user = self.repository.update_user_password(user, Hashing.hash_password(new_password))
        return updated_user

    def deactivate_user(self, user_id : int):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return self.repository.deactivate_user(user, UserStatus.INACTIVE)



