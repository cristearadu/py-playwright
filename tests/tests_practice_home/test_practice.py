import pytest

from playwright.sync_api import expect
from .test_cases.practice_cases import *
from project_utils import get_data, get_names


@pytest.mark.practice_tests
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(HIDE_DISPLAY_PLACEHOLDER), ids=get_names(HIDE_DISPLAY_PLACEHOLDER))
def test_hide_and_display_placeholder(practice_home, test_data):
    assert practice_home.check_text_input_visible()
    practice_home.hide_text_input()
    assert not practice_home.check_text_input_visible()
    practice_home.show_text_input()
    assert practice_home.check_text_input_visible()


@pytest.mark.practice_tests
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(CLICK_ALERT_BUTTON), ids=get_names(CLICK_ALERT_BUTTON))
def test_alert_boxes(practice_home, test_data):
    practice_home.click_confirm_and_accept()


@pytest.mark.practice_tests
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(TEST_MOUSE_HOVER), ids=get_names(TEST_MOUSE_HOVER))
def test_mouse_hover(practice_home, test_data):
    practice_home.hover_menu_and_click_top()


@pytest.mark.practice_tests
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(TEST_IFRAME), ids=get_names(TEST_IFRAME))
def test_iframe_open_frame(practice_home, test_data):
    practice_home.open_learning_paths_in_iframe()
