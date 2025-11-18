from pages.base_page import BasePage
from constants import HerokuMenuItemsName


class HerokuHomePage(BasePage):

    _HREF_DRAG_DROP = "a[href='/drag_and_drop']"
    _HREF_DYNAMIC_CTRL = "a[href='/dynamic_controls']"
    _HREF_EXIT_INTENT = "a[href='/exit_intent']"
    _HREF_IFRAME = "a[href='/iframe']"
    _HREF_NESTED_FRAMES = "a[href='/nested_frames']"
    _HREF_SECURE_DOWNLOAD = "a[href='/download_secure']"
    _HREF_SHADOW_DOM = "a[href='/shadowdom']"

    _TXT_DRAG_DROP = HerokuMenuItemsName.DRAG_DROP.value
    _TXT_DYNAMIC_CTRL = HerokuMenuItemsName.DYNAMIC_CTRL.value
    _TXT_EXIT_INTENT = HerokuMenuItemsName.EXIT_INTENT.value
    _TXT_IFRAME = HerokuMenuItemsName.IFRAME.value
    _TXT_NESTED_FRAMES = HerokuMenuItemsName.NESTED_FRAMES.value
    _TXT_SECURE_DOWNLOAD = HerokuMenuItemsName.SECURE_DOWNLOAD.value
    _TXT_SHADOW_DOM = HerokuMenuItemsName.SHADOW_DOM.value

    def link_drag_and_drop(self):
        return self.first_existing(self.el(self._HREF_DRAG_DROP),
                                   self.role("link", name=self._TXT_DRAG_DROP))

    def link_dynamic_controls(self):
        return self.first_existing(self.el(self._HREF_DYNAMIC_CTRL),
                                   self.role("link", name=self._TXT_DYNAMIC_CTRL))

    def link_exit_intent(self):
        return self.first_existing(self.el(self._HREF_EXIT_INTENT),
                                   self.role("link", name=self._TXT_EXIT_INTENT))

    def link_iframe(self):
        return self.first_existing(self.el(self._HREF_IFRAME),
                                   self.role("link", name=self._TXT_IFRAME))

    def link_nested_frames(self):
        return self.first_existing(self.el(self._HREF_NESTED_FRAMES),
                                   self.role("link", name=self._TXT_NESTED_FRAMES))

    def link_secure_download(self):
        return self.first_existing(self.el(self._HREF_SECURE_DOWNLOAD),
                                   self.role("link", name=self._TXT_SECURE_DOWNLOAD))

    def link_shadow_dom(self):
        return self.first_existing(self.el(self._HREF_SHADOW_DOM),
                                   self.role("link", name=self._TXT_SHADOW_DOM))

    def click_drag_and_drop(self):
        self.click(self.link_drag_and_drop())

    def click_dynamic_controls(self):
        self.click(self.link_dynamic_controls())

    def click_exit_intent(self):
        self.click(self.link_exit_intent())

    def click_iframe(self):
        self.click(self.link_iframe())

    def click_nested_frames(self):
        self.click(self.link_nested_frames())

    def click_secure_download(self):
        self.click(self.link_secure_download())

    def click_shadow_dom(self):
        self.click(self.link_shadow_dom())
