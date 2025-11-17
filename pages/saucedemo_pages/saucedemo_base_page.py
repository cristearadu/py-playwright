
from pages.base_page import BasePage


class SauceDemoBasePage(BasePage):

    HEADER_TEXT = ""

    def __init__(self, page):
        super().__init__(page)
