import pytest
from django.urls import resolve, reverse
from .. import views


def test_root_url_resolves_to_post_list():
    found = resolve('/')
    assert found.func == views.post_list


@pytest.mark.django_db
def test_home_page_shows_post_list(client):
    response = client.get(reverse('post_list'))
    assert response.content.find(b'It works!') > 0
