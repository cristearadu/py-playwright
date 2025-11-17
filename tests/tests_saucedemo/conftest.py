import pytest

from project_utils import Settings
from testing_managers import SauceDemoTestingManager, BaseTestingManager
from pages import SauceDemoLoginPage


@pytest.fixture(scope="session")
def saucedemo_base_url():
    return Settings.saucedemo_base_url


@pytest.fixture()
def saucedemo_page(page, saucedemo_base_url):
    login_page = SauceDemoLoginPage(page)
    login_page.open(saucedemo_base_url)
    return login_page


@pytest.fixture
def compose_user(testing_manager_standard_user):
    """
    Build a credentials object starting from the standard user and optionally
    overriding username/password. Returns BaseTestingManager.
    Usage:
        user = compose_user(password="bad_pass")
        user = compose_user(username="made_up", password="x")
    """
    def _compose_user(**overrides) -> BaseTestingManager:
        username = overrides.get("username", testing_manager_standard_user.username)
        password = overrides.get("password", testing_manager_standard_user.password)
        return BaseTestingManager(username=username, password=password)
    return _compose_user


@pytest.fixture(scope="package")
def testing_manager_standard_user():
    return SauceDemoTestingManager.standard()


@pytest.fixture(scope="package")
def testing_manager_locked_user():
    return SauceDemoTestingManager.locked()
