import pytest


def test_login(saucedemo_page):
    saucedemo_page.fill("#user-name", "standard_user")


if __name__ == "__main__":
    pytest.main()
