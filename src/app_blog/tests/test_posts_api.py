import pytest
from rest_framework import status

from app_blog.models import Post

# ===== READ =====


@pytest.mark.django_db
def test_anonymous_can_get_posts(api_client, post):
    response = api_client.get("/api/posts/")

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_anonymous_can_retrieve_post(api_client, post):
    response = api_client.get(f"/api/posts/{post.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == post.title


@pytest.mark.django_db
def test_retrieve_non_existing_post(api_client):
    response = api_client.get("/api/posts/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_filter_posts_by_category(api_client, post):
    response = api_client.get("/api/posts/?category=Healthcare")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


# ===== CREATE =====


@pytest.mark.django_db
def test_viewer_cannot_create_post(viewer_client):
    response = viewer_client.post(
        "/api/posts/",
        {
            "title": "New AI Post",
            "content": "Content",
            "category": "AI",
            "image_url": "",
        },
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_editor_can_create_post(editor_client):
    response = editor_client.post(
        "/api/posts/",
        {
            "title": "AI Revolution",
            "content": "Artificial Intelligence is changing the world.",
            "category": "AI",
            "image_url": "",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1


# ===== UPDATE =====


@pytest.mark.django_db
def test_editor_can_update_own_post(editor_client, post):
    response = editor_client.patch(
        f"/api/posts/{post.id}/",
        {
            "title": "Updated title",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    post.refresh_from_db()
    assert post.title == "Updated title"


@pytest.mark.django_db
def test_editor_cannot_update_foreign_post(
    editor_client,
    another_post,
):
    response = editor_client.patch(
        f"/api/posts/{another_post.id}/",
        {
            "title": "Hacked",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_update_any_post(admin_client, post):
    response = admin_client.patch(
        f"/api/posts/{post.id}/",
        {
            "title": "Updated by Admin",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    post.refresh_from_db()
    assert post.title == "Updated by Admin"


# ===== DELETE =====


@pytest.mark.django_db
def test_admin_can_delete_any_post(admin_client, post):
    response = admin_client.delete(f"/api/posts/{post.id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Post.objects.filter(id=post.id).exists()
