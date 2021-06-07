import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from .. import views
from ..models import Post


@pytest.fixture
def user_alice():
    return User.objects.create_user("Alice")


def test_root_url_resolves_to_post_list():
    found = resolve('/')
    assert found.func == views.post_list


@pytest.mark.django_db
def test_home_page_shows_post_list(client):
    response = client.get(reverse('post_list'))
    assert response.status_code == 200
    assert 'Django Girls' in response.content.decode()


@pytest.mark.django_db
def test_post_list_view_shows_published_items(client, user_alice):
    title1 = 'My first post'
    text1 = "We were happy in those days, though we were poor."
    Post.objects.create(
        author=user_alice,
        title=title1,
        text=text1,
    ).publish()

    title2 = 'My second post'
    text2 = "Ee by gum work seven while nine down mill nah then be reet."
    Post.objects.create(
        author=user_alice,
        title=title2,
        text=text2,
    ).publish()

    response = client.get(reverse('post_list'))
    assert response.status_code == 200
    assert title1 in response.content.decode()
    assert text1 in response.content.decode()
    assert title2 in response.content.decode()
    assert text2 in response.content.decode()
