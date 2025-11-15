import pytest


def test_login(page):
    page.fill("#user-name", "standard_user")


if __name__ == "__main__":
    pytest.main()
