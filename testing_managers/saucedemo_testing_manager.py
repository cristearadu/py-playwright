from constants import SauceDemoUsers
from .base_testing_manager import BaseTestingManager


class SauceDemoTestingManager:

    @classmethod
    def get(cls, user: SauceDemoUsers) -> BaseTestingManager:
        return BaseTestingManager(
            username=user.value,
            password=SauceDemoUsers.PASSWORD.value
        )

    @classmethod
    def standard(cls) -> BaseTestingManager:
        return cls.get(SauceDemoUsers.STANDARD)

    @classmethod
    def locked(cls) -> BaseTestingManager:
        return cls.get(SauceDemoUsers.LOCKED)

    @classmethod
    def problem(cls) -> BaseTestingManager:
        return cls.get(SauceDemoUsers.LOCKED)

    @classmethod
    def performance(cls) -> BaseTestingManager:
        return cls.get(SauceDemoUsers.PERFORMANCE)

    @classmethod
    def error(cls) -> BaseTestingManager:
        return cls.get(SauceDemoUsers.ERROR)

    @classmethod
    def visual(cls) -> BaseTestingManager:
        return cls.get(SauceDemoUsers.VISUAL)


