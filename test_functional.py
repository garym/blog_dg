from django.urls import reverse
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
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


def test_front_page_add_post_journey(browser, live_server, logged_in_admin):
    # User goes to front page
    if f'{live_server}/' != browser.current_url:
        browser.get(f'{live_server}/')

    # User spots a button to compose a new post
    browser.find_element_by_name('new_post_link').click()
    assert f'{live_server}/post/new/' == browser.current_url

    # User adds a post
    browser.find_element_by_name('title').send_keys('My first post title')
    browser.find_element_by_name('text').send_keys('This is the text of my first post.')
    browser.find_element_by_css_selector('button.save').click()

    # User finds themselves on the Post detail page
    post_path = reverse('post_detail', kwargs={'slug': 'my-first-post-title'})
    assert f'{live_server}{post_path}' == browser.current_url

    # User decides to edit the post
    browser.find_element_by_name('edit').click()
    edit_path = reverse('post_edit', kwargs={'slug': 'my-first-post-title'})
    assert f'{live_server}{edit_path}' == browser.current_url
    browser.find_element_by_name('text').send_keys(' This is more text for my first post.')
    browser.find_element_by_css_selector('button.save').click()

    # and saving again is successful
    assert f'{live_server}{post_path}' == browser.current_url


def test_cannot_add_two_posts_with_same_title(browser, live_server, logged_in_admin):
    new_path = reverse('post_new')
    post_path = reverse('post_detail', kwargs={'slug': 'unique'})

    browser.get(f"{live_server}{new_path}")

    browser.find_element_by_name('title').send_keys('unique')
    browser.find_element_by_name('text').send_keys('Can add unique title')
    browser.find_element_by_css_selector('button.save').click()

    assert f'{live_server}{post_path}' == browser.current_url

    browser.get(f"{live_server}{new_path}")

    browser.find_element_by_name('title').send_keys('unique')
    browser.find_element_by_name('text').send_keys('Cannot add nonunique title')
    browser.find_element_by_css_selector('button.save').click()

    assert f'{live_server}{new_path}' == browser.current_url
    assert 'non-unique' in browser.find_element_by_css_selector('.errorlist > li').text


def test_anon_user_cannot_add_post(browser, live_server):
    # User goes to front page
    if f'{live_server}/' != browser.current_url:
        browser.get(f'{live_server}/')

    # User can't see the new post link
    with pytest.raises(NoSuchElementException):
        browser.find_element_by_name('new_post_link')

    # User can't access the new post page
    browser.get(f'{live_server}/post/new/')
    assert f'{live_server}/accounts/login/?next=/post/new/' == browser.current_url
