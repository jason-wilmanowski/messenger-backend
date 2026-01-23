from messenger.repositories.user_repo import UserRepository
from messenger.core.hashing import Hashing
from messenger.core.exceptions import UserNotFoundError, InvalidPasswordError
from messenger.enums import UserStatus

class AuthService:

    def __init__(self, db):

        self.user_repository = UserRepository(db)


    def validate_login(self, email, password):

        user = self.user_repository.get_user_by_email(email)
        if not user:
            raise UserNotFoundError()

        validate_password = Hashing.check_password(password, user.password)
        if not validate_password:
            raise InvalidPasswordError()

        if user.status == UserStatus.INACTIVE.value:
            self.user_repository.activate_user(user.id, UserStatus.ACTIVE.value)

        return user






