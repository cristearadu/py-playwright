from dataclasses import dataclass


@dataclass(frozen=True)
class BaseTestingManager:
    username: str
    password: str

    def __str__(self):
        return f"Username: \'{self.username}\', Password: \'{self.password}\'"

