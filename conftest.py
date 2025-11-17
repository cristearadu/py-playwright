import os
import pytest

from playwright.sync_api import sync_playwright
from project_utils import Settings, BrowserFactory, init_logger
from constants import BrowserName, CliConfigCommands

VALID_BROWSERS = {browser.value for browser in BrowserName}
logger = init_logger()
pytest.logger = logger
pytest.logger.debug(f"Worker started: {os.environ.get('PYTEST_XDIST_WORKER', 'controller')}")


def pytest_runtest_call(item):
    doc = item.function.__doc__
    if doc:
        pytest.logger.info(f"Running Test: ${item.name}\n${doc.strip()}")


def pytest_collection_modifyitems(config, items):
    for item in items:
        if 'smoke' in item.keywords:
            item.add_marker(pytest.mark.order(1))


# --------------------------------
# Pytest CLI options
# --------------------------------
def pytest_addoption(parser):
    parser.addoption(
        CliConfigCommands.BROWSER.value,
        action="store",
        default=str(BrowserName.CHROME.value),
        help=f"Browser to use: {', '.join(VALID_BROWSERS)}"
             f" {BrowserName.SAFARI.value}"
    )

    parser.addoption(
        CliConfigCommands.HEADLESS.value,
        action="store_true",
        help="Run in headless mode (default = headed)"
    )


# --------------------------------
# Fixture: browser name from CLI
# --------------------------------
@pytest.fixture(scope="session")
def setup_browser_name(pytestconfig):
    name = pytestconfig.getoption(CliConfigCommands.BROWSER.value)
    if name not in VALID_BROWSERS:
        raise ValueError(f"Unsupported browser '{name}'. Valid options: {str(VALID_BROWSERS)}")
    pytest.logger.debug(f"Browser has been selected: {name}")
    return name


# --------------------------------
# Fixture: headless mode CLI only
# --------------------------------
@pytest.fixture(scope="session")
def headless(pytestconfig):
    return pytestconfig.getoption("--headless")


# ----------------------------------------
# SAFARI LIMITATION: force a single worker
# ----------------------------------------
def pytest_cmdline_main(config):

    # detect if we are in a worker ─ skip entirely
    if hasattr(config, "workerinput"):
        return
    browser = config.getoption(CliConfigCommands.BROWSER.value)
    if browser == BrowserName.SAFARI.value:
        xdist = config.pluginmanager.getplugin("xdist")
        if xdist:
            # override worker count basically
            config.option.numprocesses = 1
            pytest.logger.warning("Safari detected -> forcing 1 worker (no parallel support).")


# -------------------------
# Main Playwright fixtures
# -------------------------


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance, setup_browser_name, headless):
    browser = BrowserFactory.create(playwright_instance, setup_browser_name, headless)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser):
    ctx = browser.new_context(
        viewport={"width": Settings.default_width, "height": Settings.default_height},
        timezone_id=Settings.timezone,
        geolocation={"latitude": Settings.geo_lat, "longitude": Settings.geo_lon},
        permissions=["geolocation"]
    )

    yield ctx
    ctx.close()


@pytest.fixture()
def page(context):
    page = context.new_page()
    yield page
    page.close()
