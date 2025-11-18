import pytest
from playwright.sync_api import expect
from pages.saucedemo_pages.saucedemo_base_page import SauceDemoBasePage
from constants.saucedemo_constants import HeaderTexts


class SauceDemoLoginPage(SauceDemoBasePage):
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR_MSG = "[data-test='error']"
    HEADER = ".login_logo"
    ERROR_MESSAGE_CONTAINER = ".error-message-container.error"
    BACKGROUND_COLOR_CSS = "background-color"
    USER_PLACEHOLDER = "Username"
    PASSWORD_PLACEHOLDER = "Password"
    LOGIN_ROLE_NAME = "Login"

    def __init__(self, page):
        super().__init__(page)

    def username_input(self):
        return self.first_existing(
            self.placeholder(self.USER_PLACEHOLDER),
            self.test_id("username"),
            self.USERNAME,
        )

    def password_input(self):
        return self.first_existing(
            self.placeholder(self.PASSWORD_PLACEHOLDER),
            self.test_id("password"),
            self.PASSWORD,
        )

    def login_button(self):
        return self.first_existing(
            self.role("button", name=self.LOGIN_ROLE_NAME),
            self.LOGIN_BTN,
        )

    def header(self):
        return self.el(self.HEADER)

    def error_banner(self):
        # Container that owns the red background
        return self.el(self.ERROR_MESSAGE_CONTAINER)

    def screen_ready(self) -> bool:
        """
        Check that username, password, and login button are visible & enabled.
        Check that header is visible and contains expected text.
        """
        controls = [self.username_input(), self.password_input(), self.login_button()]
        for loc in controls:
            if not self.check_element_is_present_and_enabled(loc):
                return False
        return self.is_visible(self.header()) and self.contains_text(self.header(), HeaderTexts.MainText.value)

    def login(self, username: str, password: str):
        self.type(self.username_input(), username)
        self.type(self.password_input(), password)
        self.click(self.login_button())

    def login_with_user(self, user):
        pytest.logger.info(f"Trying to login in with {user}")
        self.login(user.username, user.password)

    def get_error(self) -> str:
        self.wait_for(self.ERROR_MSG)
        return self.get_text(self.ERROR_MSG)

    def expect_login_button_green(self, color_scheme: str):
        expect(self.login_button()).to_have_css(self.BACKGROUND_COLOR_CSS, color_scheme)

    def expect_error_banner_red(self, color_scheme: str):
        banner = self.error_banner()
        self.wait_for(banner)
        expect(banner).to_have_css(self.BACKGROUND_COLOR_CSS, color_scheme)
