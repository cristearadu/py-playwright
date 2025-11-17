import pytest


class BasePage:
    def __init__(self, page):
        self.page = page

    # --------------------------
    # Navigation
    # --------------------------

    def open(self, url: str):
        self.page.goto(url)

    # --------------------------
    # Basic interactions
    # --------------------------

    def type(self, locator: str, text: str):
        self.page.fill(locator, text)

    def click(self, locator: str):
        self.page.click(locator)

    # --------------------------
    # Getters
    # --------------------------

    def get_text(self, locator: str) -> str:
        return self.page.inner_text(locator).strip()

    def get_attribute(self, locator: str, attribute: str) -> str:
        return self.page.locator(locator).get_attribute(attribute)

    # --------------------------
    # Waits
    # --------------------------

    def wait_for(self, locator: str):
        self.page.wait_for_selector(locator)

    def wait_for_disappear(self, locator: str):
        self.page.wait_for_selector(locator, state="detached")

    # --------------------------
    # Element state checks
    # --------------------------

    def is_visible(self, locator: str) -> bool:
        pytest.logger.info(f"Verifying element ${locator} is visible")
        return self.page.locator(locator).is_visible()

    def is_enabled(self, locator: str) -> bool:
        pytest.logger.info(f"Verifying element ${locator} is enabled")
        return self.page.locator(locator).is_enabled()

    def is_disabled(self, locator: str) -> bool:
        pytest.logger.info(f"Verifying element ${locator} is disabled")
        return not self.page.locator(locator).is_enabled()

    def attribute_equals(self, locator: str, attribute: str, expected: str) -> bool:
        actual = self.get_attribute(locator, attribute)
        return actual == expected

    def contains_text(self, locator: str, expected: str) -> bool:
        actual = self.page.inner_text(locator)
        return expected in actual

    def exists(self, locator: str) -> bool:
        return self.count(locator) > 0

    def count(self, locator: str) -> int:
        return self.page.locator(locator).count()

    def is_clickable(self, locator: str) -> bool:
        element = self.page.locator(locator)
        return element.is_visible() and element.is_enabled()

    def check_element_is_present_and_enabled(self, locator: str) -> bool:
        element = self.page.locator(locator)
        return element.is_visible() and element.is_enabled()
