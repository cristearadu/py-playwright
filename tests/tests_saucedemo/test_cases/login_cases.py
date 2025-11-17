from faker import Faker
from constants.saucedemo_constants import SauceDemoErrors, ColorSchemes
from constants.saucedemo_users import SauceDemoUsers

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

USERNAME_REQUIRED_CASES = [
    (
        "Username required shows error",
        {
            "password": faker.password(),
            "error": SauceDemoErrors.UsernameRequired.value,
        },
    )
]

PASSWORD_REQUIRED_CASES = [
    (
        "Password required shows error",
        {
            "username": faker.user_name(),
            "error": SauceDemoErrors.PasswordRequired.value,
        },
    )
]

COLOR_SCHEME_CHECK_CASE = [
    (
        "Locked-out user shows red error banner and green login button",
        {
            "username": SauceDemoUsers.LOCKED.value,
            "password": SauceDemoUsers.PASSWORD.value,
            "login_button": ColorSchemes.LoginButtonGreenRGB.value,
            "error_message": ColorSchemes.LoginErrorRedRGB.value,
        },
    ),
    (
        "Invalid password shows red error banner and green login button",
        {
            "username": SauceDemoUsers.STANDARD.value,
            "password": faker.password(),
            "login_button": ColorSchemes.LoginButtonGreenRGB.value,
            "error_message": ColorSchemes.LoginErrorRedRGB.value,
        },
    ),
    (
        "Invalid username shows red error banner and green login button",
        {
            "username": faker.user_name(),
            "password": SauceDemoUsers.PASSWORD.value,
            "login_button": ColorSchemes.LoginButtonGreenRGB.value,
            "error_message": ColorSchemes.LoginErrorRedRGB.value,
        },
    ),
    (
        "Empty username shows red error banner and green login button",
        {
            "username": "",
            "password": faker.password(),
            "login_button": ColorSchemes.LoginButtonGreenRGB.value,
            "error_message": ColorSchemes.LoginErrorRedRGB.value,
        },
    ),
    (
        "Empty password shows red error banner and green login button",
        {
            "username": SauceDemoUsers.STANDARD.value,
            "password": "",
            "login_button": ColorSchemes.LoginButtonGreenRGB.value,
            "error_message": ColorSchemes.LoginErrorRedRGB.value,
        },
    ),
]
