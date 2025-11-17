from faker import Faker
from constants.saucedemo_constants import SauceDemoErrors

faker = Faker()

LOGIN_HAPPY_FLOW = [
    (
        'Testing Login Happy Flow works on the page',
        {}
    )
]

LOGIN_CHECK_SCREEN_ELEMENTS = [
    (
        'Verify that all login page elements are present and correct: username, password, login button, and header',
        {}
    )
]


LOCKED_OUT_USER_CASES = [
    (
        "Locked out user shows proper error",
        {
            "error": SauceDemoErrors.LockedOutUser.value
        },
    )
]

INVALID_PASSWORD_CASES = [
    (
        "Invalid password for valid username shows error",
        {
            "password": faker.password(),
            "error": SauceDemoErrors.UsernamePasswordDoNotMatch.value,
        },
    )
]

INVALID_USERNAME_CASES = [
    (
        "Invalid username shows error",
        {
            "username": faker.user_name(),
            "password": faker.password(),
            "error": SauceDemoErrors.UsernamePasswordDoNotMatch.value,
        },
    )
]
