import pytest

from project_utils import get_data, get_names
from test_cases.login_cases import LOGIN_HAPPY_FLOW, LOGIN_CHECK_SCREEN_ELEMENTS


@pytest.mark.parametrize("test_data", get_data(LOGIN_CHECK_SCREEN_ELEMENTS), ids=get_names(LOGIN_CHECK_SCREEN_ELEMENTS))
def test_login_elements_check(test_data, saucedemo_page, testing_manager_standard_user):
    assert saucedemo_page.screen_ready(), "Login screen elements are not ready (controls or header missing)"


@pytest.mark.parametrize("test_data", get_data(LOGIN_HAPPY_FLOW), ids=get_names(LOGIN_HAPPY_FLOW))
def test_login(test_data, saucedemo_page, testing_manager_standard_user):
    saucedemo_page.login_with_user(testing_manager_standard_user)


if __name__ == "__main__":
    pytest.main()
