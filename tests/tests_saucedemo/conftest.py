import pytest

from project_utils import Settings
from testing_managers import SauceDemoTestingManager
from pages import SauceDemoLoginPage


@pytest.fixture(scope="session")
def saucedemo_base_url():
    return Settings.saucedemo_base_url


@pytest.fixture()
def saucedemo_page(page, saucedemo_base_url):
    login_page = SauceDemoLoginPage(page)
    login_page.open(saucedemo_base_url)
    return login_page


@pytest.fixture(scope="package")
def testing_manager_standard_user():
    return SauceDemoTestingManager.standard()
