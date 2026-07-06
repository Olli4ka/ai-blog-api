import pytest
from django.contrib.auth.models import Group, User
from rest_framework.test import APIClient

from app_blog.models import Comment, Post


@pytest.fixture
def api_client():
    """
    Unauthenticated API client.
    """
    return APIClient()


@pytest.fixture
def groups(db):
    """
    Create application groups.
    """
    viewer = Group.objects.create(name="Viewer")
    editor = Group.objects.create(name="Editor")
    admin = Group.objects.create(name="Admin")

    return {
        "viewer": viewer,
        "editor": editor,
        "admin": admin,
    }


@pytest.fixture
def viewer_user(db, groups):
    user = User.objects.create_user(
        username="Anna",
        password="Anna123456",
    )
    user.groups.add(groups["viewer"])
    return user


@pytest.fixture
def editor_user(db, groups):
    user = User.objects.create_user(
        username="John",
        password="John123456",
    )
    user.groups.add(groups["editor"])
    return user


@pytest.fixture
def admin_user(db, groups):
    user = User.objects.create_user(
        username="Olivia",
        password="Olivia123456",
    )
    user.groups.add(groups["admin"])
    return user


@pytest.fixture
def superuser(db):
    return User.objects.create_superuser(
        username="admin",
        password="fb5422",
        email="admin@example.com",
    )


@pytest.fixture
def post(editor_user):
    return Post.objects.create(
        title="AI in Healthcare",
        content="AI helps doctors make better decisions.",
        category="Healthcare",
        image_url="https://example.com/image.jpg",
        author=editor_user,
    )


@pytest.fixture
def comment(post, viewer_user):
    return Comment.objects.create(
        text="Very interesting article!",
        post=post,
        author=viewer_user,
    )


@pytest.fixture
def viewer_client(api_client, viewer_user):
    api_client.force_authenticate(user=viewer_user)
    return api_client


@pytest.fixture
def editor_client(api_client, editor_user):
    api_client.force_authenticate(user=editor_user)
    return api_client


@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def another_post(admin_user):
    return Post.objects.create(
        title="Admin post",
        content="Admin content",
        category="AI",
        image_url="",
        author=admin_user,
    )


@pytest.fixture
def another_comment(post, editor_user):
    return Comment.objects.create(
        text="Editor's comment",
        post=post,
        author=editor_user,
    )
