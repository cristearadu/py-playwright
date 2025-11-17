import pytest

from pages.saucedemo_pages.saucedemo_base_page import SauceDemoBasePage
from constants.saucedemo_constants import HeaderTexts


class SauceDemoLoginPage(SauceDemoBasePage):

    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR_MSG = "[data-test='error']"
    HEADER = ".login_logo"

    def __init__(self, page):
        super().__init__(page)

    def screen_ready(self) -> bool:
        """
        Check that username, password, and login button are visible & enabled
        Check that header is enabled
        """
        controls = {self.USERNAME, self.PASSWORD, self.LOGIN_BTN}
        for locator in controls:
            if not self.check_element_is_present_and_enabled(locator):
                return False
        return self.is_visible(self.HEADER) and self.contains_text(self.HEADER, HeaderTexts.MAIN_TEXT.value)

    def login(self, username: str, password: str):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BTN)

    def login_with_user(self, user):
        pytest.logger.info(f"Logging in with {user}")
        self.login(user.username, user.password)

    def get_error(self) -> str:
        self.wait_for(self.ERROR_MSG)
        return self.get_text(self.ERROR_MSG)
