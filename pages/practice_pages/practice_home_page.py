from pages.base_page import BasePage
from playwright.sync_api import Page, expect
import pytest


class PracticeHomePage(BasePage):
    TEXT_FIELD_PH = "#displayed-text"
    TEXT_FIELD_PLACEHOLDER = "Hide/Show Example"
    HIDE_BTN = "#hide-textbox"
    SHOW_BTN = "#show-textbox"
    CONFIRM_BTN_TEXT = "Confirm"
    MOUSE_HOVER_BTN = "#mousehover"
    HOVER_TOP_NAME = "Top"
    IFRAME_SEL = "#courses-iframe"
    IFRAME_CLOSE_BTN = "button:has-text('Close')"
    IFRAME_NAV_LEARNING_PATHS = "nav >> text=Learning Paths"

    def __init__(self, page: Page):
        super().__init__(page)

    def _text_input_locator(self):
        """Return the most robust locator for the text field, falling back to CSS if needed."""
        loc = self.placeholder(self.TEXT_FIELD_PLACEHOLDER)
        if loc.count() == 0:
            loc = self.el(self.TEXT_FIELD_PH)
        return loc

    def check_text_input_visible(self) -> bool:
        loc = self._text_input_locator()
        return self.check_element_is_present_and_enabled(loc)

    def hide_text_input(self):
        pytest.logger.info("Clicking Hide Textbox button")
        self.click_when_ready(self.HIDE_BTN)

    def show_text_input(self):
        pytest.logger.info("Clicking Show Textbox button")
        self.click_when_ready(self.SHOW_BTN)

    def is_text_input_hidden(self) -> bool:
        return not self.is_visible(self._text_input_locator())

    def click_confirm_and_accept(self):
        # one-shot handler is safer than a permanent listener
        self.page.once("dialog", lambda d: d.accept())
        self.click_when_ready(self.role("button", name=self.CONFIRM_BTN_TEXT))

    def hover_menu_and_click_top(self):
        # Ensure button is in view and perform a robust hover
        self.hover(self.MOUSE_HOVER_BTN)
        top_link = self.role("link", name=self.HOVER_TOP_NAME)
        top_link.wait_for(state="visible", timeout=3000)
        top_link.click()

    def open_learning_paths_in_iframe(self):
        # Bring iframe into view then switch via frame_locator
        self.scroll_into_view(self.IFRAME_SEL)
        frame = self.page.frame_locator(self.IFRAME_SEL)

        close_btn = frame.locator(self.IFRAME_CLOSE_BTN)
        if close_btn.count() > 0:
            close_btn.click()

        nav_lp = frame.locator(self.IFRAME_NAV_LEARNING_PATHS)
        expect(nav_lp).to_be_visible()
        nav_lp.click()

        expect(frame.locator(self.IFRAME_NAV_LEARNING_PATHS)).to_be_visible()
        return frame
