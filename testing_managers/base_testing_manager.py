from dataclasses import dataclass


@dataclass(frozen=True)
class UserCredentials:
    username: str
    password: str

    def __str__(self):
        return f"Username: \'{self.username}\', Password: \'{self.password}\'"

