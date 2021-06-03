from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')


def test_get_title():
    assert 'success' in browser.title

