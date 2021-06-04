import pytest
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import Post


@pytest.fixture
def user_alice():
    return User.objects.create_user("Alice")


@pytest.fixture
def post_a(user_alice):
    return Post.objects.create(
        author=user_alice,
        text='Post a',
        created_date=timezone.now(),
    )


@pytest.mark.django_db
def test_save_and_retrieve_posts(user_alice):
    Post.objects.create(
        author=user_alice,
        text='New Post',
        created_date=timezone.now(),
    )
    all_items = Post.objects.all()
    assert all_items.count() == 1
    assert all_items[0].text == 'New Post'


@pytest.mark.django_db
def test_post_create_sets_sensible_default_date(user_alice):
    time_before = timezone.now()
    post_a = Post.objects.create(
        author=user_alice,
        text='New Post',
    )
    time_after = timezone.now()

    assert time_before < post_a.created_date < time_after


@pytest.mark.django_db
def test_publish_sets_published_date(post_a):
    time_before = timezone.now()
    post_a.publish()
    time_after = timezone.now()

    assert time_before < post_a.published_date < time_after
