from pages.base_page import BasePage
from playwright.sync_api import Page, expect


class PracticeHomePage(BasePage):
    TEXT_FIELD_PH = "#displayed-text"
    HIDE_BTN = "#hide-textbox"
    SHOW_BTN = "#show-textbox"
    CONFIRM_BTN_TEXT = "Confirm"
    MOUSE_HOVER_BTN = "#mousehover"
    HOVER_TOP_LINK = "text=Top"
    IFRAME_SEL = "#courses-iframe"
    IFRAME_CLOSE_BTN = "button:has-text('Close')"
    IFRAME_NAV_LEARNING_PATHS = "nav >> text=Learning Paths"

    def __init__(self, page: Page):
        super().__init__(page)

    def check_text_input_visible(self):
        return self.check_element_is_present_and_enabled(self.TEXT_FIELD_PH)

    def hide_text_input(self):
        self.check_element_is_present_and_enabled(self.HIDE_BTN)
        self.is_clickable(self.HIDE_BTN)
        self.click(self.HIDE_BTN)

    def show_text_input(self):
        self.check_element_is_present_and_enabled(self.SHOW_BTN)
        self.is_clickable(self.SHOW_BTN)
        self.click(self.SHOW_BTN)

    def click_confirm_and_accept(self):
        self.page.on("dialog", lambda d: d.accept())
        self.page.get_by_role("button", name=self.CONFIRM_BTN_TEXT).click()

    def hover_menu_and_click_top(self):
        hover_btn = self.page.locator(self.MOUSE_HOVER_BTN)
        hover_btn.scroll_into_view_if_needed()
        hover_btn.hover()
        top_link = self.page.get_by_role("link", name="Top")
        expect(top_link).to_be_visible()
        top_link.click()

    def open_learning_paths_in_iframe(self):
        self.page.locator(self.IFRAME_SEL).scroll_into_view_if_needed()
        frame = self.page.frame_locator(self.IFRAME_SEL)

        close_btn = frame.locator(self.IFRAME_CLOSE_BTN)
        if close_btn.count() > 0:
            close_btn.click()

        nav_lp = frame.locator(self.IFRAME_NAV_LEARNING_PATHS)
        expect(nav_lp).to_be_visible()
        nav_lp.click()

        expect(frame.locator(self.IFRAME_NAV_LEARNING_PATHS)).to_be_visible()
        return frame
