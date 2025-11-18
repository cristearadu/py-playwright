import pytest

from project_utils import get_data, get_names
from .test_cases.heroku_cases import DRAG_AND_DROP


@pytest.mark.heroku_app
@pytest.mark.regression
@pytest.mark.parametrize("test_data", get_data(DRAG_AND_DROP), ids=get_names(DRAG_AND_DROP))
def test_drag_and_drop(heroku_drag_and_drop_page, test_data):
    before = heroku_drag_and_drop_page.labels()
    pytest.logger.info(f"Before HEADER A: {before[0]}; Before HEADER B: {before[1]}")
    heroku_drag_and_drop_page.swap_a_to_b()
    after = heroku_drag_and_drop_page.labels()
    pytest.logger.info(f"After HEADER A: {after[0]}; After HEADER B: {after[1]}")

    assert after[0] == test_data["expected_a"]
    assert after[1] == test_data["expected_b"]
    assert before != after
