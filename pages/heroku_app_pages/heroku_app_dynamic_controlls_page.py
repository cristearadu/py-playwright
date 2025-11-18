import pytest
from pages.base_page import BasePage
from playwright.sync_api import expect


class HerokuDynamicControlsPage(BasePage):
    _CHECKBOX_CONTAINER = "#checkbox"
    _CHECKBOX = '//div[@id="checkbox"]/input'
    _TOGGLE_CHECKBOX_BTN = "form#checkbox-example button"
    _INPUT_FIELD = "form#input-example input[type='text']"
    _TOGGLE_INPUT_BTN = "form#input-example button"

    _LOADING = "#loading"
    _MESSAGE = "#message"

    def verify_checkbox_status(self):
        self.is_enabled(self._CHECKBOX)

    def remove_checkbox(self):
        self.click(self._TOGGLE_CHECKBOX_BTN)
        self.wait_for_hidden(self.page.locator(self._LOADING).nth(0))
        self.wait_for_hidden(self._CHECKBOX_CONTAINER)

    def add_checkbox(self):
        self.click(self._TOGGLE_CHECKBOX_BTN)
        # bug inside the page
        self.wait_for_hidden(self.page.locator(self._LOADING).nth(0))
        self.wait_for(self._CHECKBOX_CONTAINER)

    def enable_input(self):
        self.click(self._TOGGLE_INPUT_BTN)
        self.wait_for_hidden(self.page.locator(self._LOADING).nth(0))
        self.wait_for(self._INPUT_FIELD)
        input_box = self.page.locator(self._INPUT_FIELD)
        expect(input_box).to_be_visible()
        expect(input_box).to_be_editable()

    def disable_input(self):
        self.click(self._TOGGLE_INPUT_BTN)
        self.wait_for_hidden(self.page.locator(self._LOADING).nth(0))
        self.wait_for(self._INPUT_FIELD)
        input_box = self.page.locator(self._INPUT_FIELD)
        expect(input_box).not_to_be_editable()

    def type_in_input(self, text: str):
        self.enable_input()
        self.type(self._INPUT_FIELD, text)
