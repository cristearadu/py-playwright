import pytest

from playwright.sync_api import expect

from project_utils import get_data, get_names
from .test_cases.login_cases import *


@pytest.mark.smoke
@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(LOGIN_CHECK_SCREEN_ELEMENTS), ids=get_names(LOGIN_CHECK_SCREEN_ELEMENTS))
def test_login_elements_check(test_data, saucedemo_page):
    assert saucedemo_page.screen_ready(), "Login screen elements are not ready (controls or header missing)"


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(LOGIN_HAPPY_FLOW), ids=get_names(LOGIN_HAPPY_FLOW))
def test_login_happy_flow(test_data, testing_manager_standard_user, saucedemo_page, saucedemo_base_url):
    saucedemo_page.login_with_user(testing_manager_standard_user)
    expect(saucedemo_page.page).not_to_have_url(saucedemo_base_url)


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(LOCKED_OUT_USER_CASES), ids=get_names(LOCKED_OUT_USER_CASES))
def test_locked_out_user_error(test_data, testing_manager_locked_user, saucedemo_page):
    saucedemo_page.login_with_user(testing_manager_locked_user)
    error_message = saucedemo_page.get_error()
    assert error_message == test_data['error'], \
        f"Failed!\n Expected message: {test_data['error']}\nActual message: {error_message}"


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(INVALID_PASSWORD_CASES), ids=get_names(INVALID_PASSWORD_CASES))
def test_invalid_password_error(test_data, compose_user, saucedemo_page):
    user = compose_user(password=test_data['password'])
    saucedemo_page.login_with_user(user)
    error_message = saucedemo_page.get_error()
    assert error_message == test_data['error'], \
        f"Failed!\n Expected message: {test_data['error']}\nActual message: {error_message}"


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(INVALID_USERNAME_CASES), ids=get_names(INVALID_USERNAME_CASES))
def test_invalid_username_error(test_data, compose_user, saucedemo_page):
    user = compose_user(username=test_data['username'], password=test_data['password'])
    saucedemo_page.login_with_user(user)
    error_message = saucedemo_page.get_error()
    assert error_message == test_data['error'], \
        f"Failed!\n Expected message: {test_data['error']}\nActual message: {error_message}"


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(USERNAME_REQUIRED_CASES), ids=get_names(USERNAME_REQUIRED_CASES))
def test_username_required_error(test_data, compose_user, saucedemo_page):
    user = compose_user(username="", password=test_data["password"])  # reuse generated password
    saucedemo_page.login_with_user(user)
    error_message = saucedemo_page.get_error()
    assert error_message == test_data["error"], (
        f"Failed!\n Expected message: {test_data['error']}\nActual message: {error_message}"
    )


@pytest.mark.login
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(PASSWORD_REQUIRED_CASES), ids=get_names(PASSWORD_REQUIRED_CASES))
def test_password_required_error(test_data, compose_user, saucedemo_page):
    user = compose_user(username=test_data["username"], password="")
    saucedemo_page.login_with_user(user)
    error_message = saucedemo_page.get_error()
    assert error_message == test_data["error"], (
        f"Failed!\n Expected message: {test_data['error']}\nActual message: {error_message}"
    )


@pytest.mark.order("last")
@pytest.mark.login
@pytest.mark.regression
@pytest.mark.color_scheme
@pytest.mark.parametrize("test_data", get_data(COLOR_SCHEME_CHECK_CASE), ids=get_names(COLOR_SCHEME_CHECK_CASE))
def test_color_scheme_login_page(test_data, compose_user, saucedemo_page):
    user = compose_user(username=test_data['username'], password=test_data['password'])
    saucedemo_page.login_with_user(user)
    saucedemo_page.expect_login_button_green(test_data['login_button'])
    saucedemo_page.expect_error_banner_red(test_data['error_message'])


if __name__ == "__main__":
    pytest.main()
