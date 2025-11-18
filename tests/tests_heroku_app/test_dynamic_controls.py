import pytest

from project_utils import get_data, get_names
from .test_cases.heroku_cases import DYNAMIC_CONTROLS


@pytest.mark.heroku_app
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(DYNAMIC_CONTROLS), ids=get_names(DYNAMIC_CONTROLS))
def test_dynamic_controls(heroku_dynamic_control_page, test_data):
    heroku_dynamic_control_page.remove_checkbox()
    heroku_dynamic_control_page.add_checkbox()
    heroku_dynamic_control_page.enable_input()
    if 'text' in test_data:
        heroku_dynamic_control_page.type_in_input(test_data['text'])
    heroku_dynamic_control_page.disable_input()

