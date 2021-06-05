import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Firefox()
    driver.implicitly_wait(3)

    yield driver
    driver.quit()


@pytest.fixture
def logged_in_admin(browser, live_server, admin_user):
    browser.get(f'{live_server}/admin/')

    browser.find_element_by_name("username").send_keys('admin')
    browser.find_element_by_name("password").send_keys('password')
    browser.find_element_by_css_selector("div.submit-row input").click()

    yield

    browser.get(f'{live_server}/admin/logout/')
    assert 'Logged out' in browser.title


def test_using_admin_site_to_add_post(browser, live_server, logged_in_admin):
    if f'{live_server}/admin/' != browser.current_url:
        browser.get(f'{live_server}/admin/')

    browser.find_element_by_link_text('Posts').click()
    browser.find_element_by_link_text('ADD POST').click()
    author_field = browser.find_element_by_name('author')
    title_field = browser.find_element_by_name('title')
    text_field = browser.find_element_by_name('text')

    Select(author_field).select_by_visible_text('admin')
    title_field.send_keys('My first post title')
    text_field.send_keys('This is the text of my first post')
    browser.find_element_by_name('_save').click()

    success_link = browser.find_element_by_css_selector(".success a")
    assert success_link.text == 'My first post title'
