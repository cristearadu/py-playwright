import pytest
from constants import BrowserName


class BrowserFactory:
    @staticmethod
    def create(playwright, browser, headless):
        match browser:
            case BrowserName.CHROME.value:
                return playwright.chromium.launch(
                    channel="chrome",
                    headless=headless,
                    args=["--start-maximized"]
                )
            case BrowserName.FIREFOX.value:
                return playwright.firefox.launch(headless=headless)
            case BrowserName.EDGE.value:
                return playwright.edge.launch(
                    channel="msedge",
                    headless=headless,
                    args=["--start-maximized"]
                )
            case BrowserName.SAFARI.value:
                pytest.logger.warning("[BrowserFactory] Safari ignores headless")
                return playwright.webkit.launch(headless=False)
            case _:
                raise ValueError(f"Unknown browser '{browser}'")
