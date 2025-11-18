import pytest
from playwright.sync_api import Page
from pages import PracticeHomePage
from project_utils.settings import Settings


@pytest.fixture(scope="session")
def practice_page_url():
    return Settings.practice_base_url


@pytest.fixture()
def practice_home(page: Page, practice_page_url) -> PracticeHomePage:
    home_page = PracticeHomePage(page)
    home_page.open(practice_page_url)
    return home_page

