import pytest
from pages.heroku_app_pages import HerokuHomePage, HerokuDragAndDropPage, HerokuDynamicControlsPage
from project_utils.settings import Settings


@pytest.fixture(scope="session")
def heroku_app_base_url():
    return Settings.heroku_base_url


@pytest.fixture()
def heroku_home(page, heroku_app_base_url):
    home = HerokuHomePage(page)
    home.open(heroku_app_base_url)
    return home


@pytest.fixture()
def heroku_drag_and_drop_page(page, heroku_home):
    heroku_home.click_drag_and_drop()
    drag_and_drop_page = HerokuDragAndDropPage(page)
    return drag_and_drop_page


@pytest.fixture()
def heroku_dynamic_control_page(page, heroku_home):
    heroku_home.click_dynamic_controls()
    drag_and_drop_page = HerokuDynamicControlsPage(page)
    return drag_and_drop_page
