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
def test_home_page_shows_post_list(client, post1):
    post1.publish()
    response = client.get(reverse('post_list'))
    assert response.status_code == 200
    assert post1.title in response.content.decode()


@pytest.mark.django_db
def test_post_list_view_shows_published_item_details(client, post1, post2):
    post2.publish()

    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert post2.title in content
    assert post2.text in content
    assert f"href=\"{reverse('post_detail', kwargs={'slug': post2.slug})}\"" in content


@pytest.mark.django_db
def test_post_list_view_hides_unpublished_item_details(client, post1, post2):
    post2.publish()

    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert post1.title not in content
    assert post1.text not in content
    assert f"href=\"{reverse('post_detail', kwargs={'slug': post1.slug})}\"" not in content


@pytest.mark.django_db
def test_post_detail_view_hides_unpublished_item_details(client, post1):
    post1.publish()

    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    content = response.content.decode()
    assert response.status_code == 200
    assert post1.title in content
    assert post1.text in content


@pytest.mark.django_db
def test_post_list_view_hides_new_post_link_for_anon_user(client):
    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert f"href=\"{reverse('post_new')}\"" not in content


@pytest.mark.django_db
def test_post_list_view_provides_new_post_link(client, user_alice):
    client.force_login(user_alice)
    response = client.get(reverse('post_list'))
    content = response.content.decode()
    assert response.status_code == 200
    assert f"href=\"{reverse('post_new')}\"" in content


@pytest.mark.django_db
def test_post_detail_provides_new_post_link(client, user_alice, post1):
    client.force_login(user_alice)
    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    content = response.content.decode()
    assert response.status_code == 200
    assert f"href=\"{reverse('post_new')}\"" in content


@pytest.mark.django_db
def test_post_detail_page_count_increment(client, post1):
    expected_count = post1.page_hits.count + 1
    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    assert response.status_code == 200
    assert expected_count == Post.objects.get(id=post1.id).page_hits.count


@pytest.mark.django_db
def test_post_detail_page_count_increments_once_per_user(client, post1):
    expected_count = post1.page_hits.count + 1
    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    assert response.status_code == 200
    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    assert response.status_code == 200
    assert expected_count == Post.objects.get(id=post1.id).page_hits.count


@pytest.mark.django_db
def test_post_detail_no_page_count_increments_when_logged_in(client, user_alice, post1):
    client.force_login(user_alice)
    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    assert response.status_code == 200
    assert post1.page_hits.count == Post.objects.get(id=post1.id).page_hits.count


@pytest.mark.django_db
def test_post_detail_displays_latest_page_count(client, post1):
    response = client.get(reverse('post_detail', kwargs={'slug': post1.slug}))
    content = response.content.decode()
    post = Post.objects.get(slug=post1.slug)
    assert response.status_code == 200
    assert f'<page-hits>{post.page_hits.count}</page-hits>' in content
