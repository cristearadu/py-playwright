import pytest

from project_utils import Settings


@pytest.fixture(scope="session")
def saucedemo_base_url():
    return Settings.saucedemo_base_url


@pytest.fixture()
def saucedemo_page(page, saucedemo_base_url):
    page.goto(saucedemo_base_url)
    return page
