import pytest
import time

from typing import Union
from playwright.sync_api import Locator

LocatorLike = Union[str, Locator]


class BasePage:
    def __init__(self, page):
        self.page = page

    # --------------------------
    # Locator helpers (strategy-aware)
    # --------------------------

    def el(self, selector: str, **kwargs) -> Locator:
        """Generic CSS/XPath selector."""
        return self.page.locator(selector, **kwargs)

    def role(self, role: str, **kwargs) -> Locator:
        """get_by_role: role='button', name='Confirm', exact=False, etc."""
        return self.page.get_by_role(role, **kwargs)

    def text(self, text: str, exact: bool = False) -> Locator:
        """get_by_text."""
        return self.page.get_by_text(text, exact=exact)

    def label(self, text: str, exact: bool = False) -> Locator:
        """get_by_label."""
        return self.page.get_by_label(text, exact=exact)

    def placeholder(self, text: str, exact: bool = False) -> Locator:
        """get_by_placeholder."""
        return self.page.get_by_placeholder(text, exact=exact)

    def test_id(self, test_id: str) -> Locator:
        """get_by_test_id."""
        return self.page.get_by_test_id(test_id)

    def title(self, title: str, exact: bool = False) -> Locator:
        """get_by_title."""
        return self.page.get_by_title(title, exact=exact)

    def alt_text(self, text: str, exact: bool = False) -> Locator:
        """get_by_alt_text."""
        return self.page.get_by_alt_text(text, exact=exact)

    def _loc(self, target: LocatorLike) -> Locator:
        """normalize any target into a Playwright Locator"""
        if isinstance(target, Locator):
            return target
        return self.page.locator(target)

    def first_existing(self, *candidates: LocatorLike, timeout: float = 0) -> Locator:
        """
        Return the first locator that exists (count() > 0) among the given candidates.
        If timeout > 0 (milliseconds), poll until one exists or the timeout expires.
        Usage:
            self.first_existing(self.placeholder("Username"), self.test_id("username"), "#user-name")
        """
        if not candidates:
            raise ValueError("first_existing: no candidates provided")

        deadline = time.time() + (timeout / 1000.0) if timeout else None
        last_exception = None

        while True:
            for c in candidates:
                loc = self._loc(c)
                try:
                    if loc.count() > 0:
                        return loc
                except Exception as e:
                    last_exception = e
            if deadline and time.time() < deadline:
                self.page.wait_for_timeout(50)
                continue
            break

        if last_exception:
            raise ValueError("first_existing: none of the candidate locators matched") from last_exception
        raise ValueError("first_existing: none of the candidate locators matched")

    # --------------------------
    # Navigation
    # --------------------------

    def open(self, url: str):
        self.page.goto(url)

    # --------------------------
    # Basic interactions
    # --------------------------

    def type(self, target: LocatorLike, text: str):
        self._loc(target).fill(text)

    def click(self, target: LocatorLike):
        self._loc(target).click()

    def click_when_ready(self, target: LocatorLike, timeout: float = 5000):
        loc = self._loc(target)
        loc.wait_for(state="visible", timeout=timeout)
        if not loc.is_enabled():
            self.page.wait_for_timeout(50)
        loc.click()

    def scroll_into_view(self, target: LocatorLike, timeout: float = 5000, offset: int = 0) -> Locator:
        """Bring target into viewport reliably across browsers (incl. Firefox headless).
        Steps:
          1) Wait for element attachment.
          2) Try Playwright's scroll_into_view_if_needed.
          3) If still out of view, center it via JS using the element handle.
          4) As a last resort, nudge the page with mouse wheel.
        Returns the normalized Locator for chaining.
        """
        loc = self._loc(target)
        # Ensure element is attached in DOM first
        loc.wait_for(state="attached", timeout=timeout)

        # Primary attempt
        try:
            loc.scroll_into_view_if_needed(timeout=timeout)
        except Exception:
            # Ignore and try fallbacks
            pass

        # If still not fully in viewport, use JS to center with optional offset
        if not self.is_in_viewport(loc):
            handle = loc.element_handle()
            if handle:
                try:
                    handle.evaluate(
                        "(el, off) => {\n"
                        "  const r = el.getBoundingClientRect();\n"
                        "  const y = window.scrollY + r.top - (window.innerHeight / 2) + (off || 0);\n"
                        "  window.scrollTo({ top: Math.max(y, 0) });\n"
                        "}",
                        offset,
                    )
                except Exception:
                    pass

        # Final nudge with mouse wheel if needed (helps Firefox/WebKit intermittence)
        attempts = 0
        while not self.is_in_viewport(loc) and attempts < 10:
            self.page.mouse.wheel(0, 600)
            attempts += 1

        return loc

    def hover(self, target: LocatorLike, timeout: float = 5000) -> None:
        """Reliably hover an element after bringing it into view.
        Falls back to mouse.move or synthetic over event if native hover fails.
        """
        loc = self.scroll_into_view(target, timeout=timeout)
        try:
            loc.hover(timeout=timeout)
            return
        except Exception:
            pass

        # Fallback 1: move the mouse to the element's center
        box = loc.bounding_box()
        if box:
            self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            return

        # Fallback 2: dispatch a synthetic mouseover
        handle = loc.element_handle()
        if handle:
            handle.evaluate(
                "(el) => el.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }))"
            )

    def is_in_viewport(self, target: LocatorLike) -> bool:
        """Check if the element's bounding rect intersects the viewport."""
        loc = self._loc(target)
        handle = loc.element_handle()
        if not handle:
            return False
        return self.page.evaluate(
            """
            (el) => {
              const r = el.getBoundingClientRect();
              const w = window.innerWidth || document.documentElement.clientWidth;
              const h = window.innerHeight || document.documentElement.clientHeight;
              return r.bottom > 0 && r.right > 0 && r.top < h && r.left < w;
            }
            """,
            handle,
        )

    # --------------------------
    # Getters
    # --------------------------

    def get_text(self, target: LocatorLike) -> str:
        return self._loc(target).inner_text().strip()

    def get_attribute(self, target: LocatorLike, attribute: str) -> str:
        return self._loc(target).get_attribute(attribute)

    # --------------------------
    # Waits
    # --------------------------

    def wait_for(self, target: LocatorLike):
        self._loc(target).wait_for(state="visible")

    def wait_for_hidden(self, target: LocatorLike):
        self._loc(target).wait_for(state="hidden")

    def wait_for_disappear(self, target: LocatorLike):
        self._loc(target).wait_for(state="detached")

    # --------------------------
    # Element state checks
    # --------------------------

    def is_visible(self, target: LocatorLike) -> bool:
        pytest.logger.info(f"Verifying element ${target} is visible")
        return self._loc(target).is_visible()

    def is_enabled(self, target: LocatorLike) -> bool:
        pytest.logger.info(f"Verifying element ${target} is enabled")
        return self._loc(target).is_enabled()

    def is_disabled(self, target: LocatorLike) -> bool:
        pytest.logger.info(f"Verifying element ${target} is disabled")
        return not self._loc(target).is_enabled()

    def attribute_equals(self, target: LocatorLike, attribute: str, expected: str) -> bool:
        actual = self.get_attribute(target, attribute)
        return actual == expected

    def contains_text(self, target: LocatorLike, expected: str) -> bool:
        actual = self.get_text(target)
        return expected in actual

    def exists(self, target: LocatorLike) -> bool:
        return self.count(target) > 0

    def count(self, target: LocatorLike) -> int:
        return self._loc(target).count()

    def is_clickable(self, target: LocatorLike) -> bool:
        loc = self._loc(target)
        return loc.is_visible() and loc.is_enabled()

    def check_element_is_present_and_enabled(self, target: LocatorLike) -> bool:
        loc = self._loc(target)
        return loc.is_visible() and loc.is_enabled()