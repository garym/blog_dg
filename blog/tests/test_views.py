import pytest
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from .. import views
from ..models import Post


@pytest.fixture
def user_alice():
    return User.objects.create_user("Alice")


@pytest.fixture
def post1(user_alice):
    title = 'My first post'
    text = "We were happy in those days, though we were poor."
    post = Post.objects.create(
        author=user_alice,
        title=title,
        text=text,
    )
    return post


@pytest.fixture
def post2(user_alice):
    title = 'My second post'
    text = "Ee by gum work seven while nine down mill nah then be reet."
    post = Post.objects.create(
        author=user_alice,
        title=title,
        text=text,
    )
    return post


def test_root_url_resolves_to_post_list():
    found = resolve('/')
    assert found.func == views.post_list


@pytest.mark.django_db
def test_home_page_shows_post_list(client):
    response = client.get(reverse('post_list'))
    assert response.status_code == 200
    assert 'Django Girls' in response.content.decode()


@pytest.mark.django_db
def test_post_list_view_shows_published_item_details(client, post1, post2):
    post2.publish()

    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert post2.title in content
    assert post2.text in content
    assert f"href=\"{reverse('post_detail', kwargs={'pk': post2.id})}\"" in content


@pytest.mark.django_db
def test_post_list_view_hides_unpublished_item_details(client, post1, post2):
    post2.publish()

    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert post1.title not in content
    assert post1.text not in content
    assert f"href=\"{reverse('post_detail', kwargs={'pk': post1.id})}\"" not in content


@pytest.mark.django_db
def test_post_detail_view_hides_unpublished_item_details(client, post1):
    post1.publish()

    response = client.get(reverse('post_detail', kwargs={'pk': post1.id}))
    content = response.content.decode()
    assert response.status_code == 200
    assert post1.title in content
    assert post1.text in content


@pytest.mark.django_db
def test_post_list_view_provides_new_post_link(client):
    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert f"href=\"{reverse('post_new')}\"" in content


@pytest.mark.django_db
def test_post_detail_provides_new_post_link(client, post1):
    response = client.get(reverse('post_detail', kwargs={'pk': post1.id}))
    content = response.content.decode()
    assert response.status_code == 200
    assert f"href=\"{reverse('post_new')}\"" in content


@pytest.mark.django_db
def test_post_new_provides_new_post_link(client):
    response = client.get(reverse('post_new'))
    content = response.content.decode()
    assert response.status_code == 200
    assert f"href=\"{reverse('post_new')}\"" in content
