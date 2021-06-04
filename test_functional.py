import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def browser():
    print("\nStarting Firefox Session")
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)

    yield driver
    print("\nStopping Firefox Session")
    driver.quit()


def test_get_title(browser):
    browser.get('http://localhost:8000')
    assert 'success' in browser.title
