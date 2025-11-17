from constants import SauceDemoUsers
from .base_testing_manager import UserCredentials


class SauceDemoTestingManager:

    @classmethod
    def get(cls, user: SauceDemoUsers) -> UserCredentials:
        return UserCredentials(
            username=user.value,
            password=SauceDemoUsers.PASSWORD.value
        )

    @classmethod
    def standard(cls) -> UserCredentials:
        return cls.get(SauceDemoUsers.STANDARD)

    @classmethod
    def locked(cls) -> UserCredentials:
        return cls.get(SauceDemoUsers.LOCKED)

    @classmethod
    def problem(cls) -> UserCredentials:
        return cls.get(SauceDemoUsers.LOCKED)

    @classmethod
    def performance(cls) -> UserCredentials:
        return cls.get(SauceDemoUsers.PERFORMANCE)

    @classmethod
    def error(cls) -> UserCredentials:
        return cls.get(SauceDemoUsers.ERROR)

    @classmethod
    def visual(cls) -> UserCredentials:
        return cls.get(SauceDemoUsers.VISUAL)


