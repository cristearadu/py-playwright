import os
import pytest
from constants import BrowserName


class BrowserFactory:
    @staticmethod
    def create(playwright, browser, headless):
        match browser:
            case BrowserName.CHROME.value:
                return playwright.chromium.launch(
                    headless=headless,
                    args=["--start-maximized"]
                )
            case BrowserName.FIREFOX.value:
                return playwright.firefox.launch(headless=headless)
            case BrowserName.EDGE.value:
                return playwright.chromium.launch(
                    channel="msedge",
                    headless=headless,
                    args=["--start-maximized"]
                )
            case BrowserName.SAFARI.value:
                if not os.environ.get("DISPLAY"):
                    headless = True
                return playwright.webkit.launch(headless=headless)
            case _:
                raise ValueError(f"Unknown browser '{browser}'")
