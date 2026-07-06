import pytest

from rest_framework import status

from app_blog.models import Comment


# ===== READ =====


@pytest.mark.django_db
def test_anonymous_can_get_comments(api_client, comment):
    response = api_client.get(f"/api/posts/{comment.post.id}/comments/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1


@pytest.mark.django_db
def test_anonymous_can_retrieve_comment(api_client, comment):
    response = api_client.get(f"/api/posts/{comment.post.id}/comments/{comment.id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["text"] == comment.text


@pytest.mark.django_db
def test_retrieve_non_existing_comment(api_client, post):
    response = api_client.get(f"/api/posts/{post.id}/comments/999/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


# ===== CREATE =====


@pytest.mark.django_db
def test_viewer_can_create_comment(viewer_client, post):
    response = viewer_client.post(
        f"/api/posts/{post.id}/comments/",
        {
            "text": "Great article!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.count() == 1


# ===== UPDATE =====


@pytest.mark.django_db
def test_viewer_can_update_own_comment(viewer_client, comment):
    response = viewer_client.patch(
        f"/api/posts/{comment.post.id}/comments/{comment.id}/",
        {
            "text": "Updated comment",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    comment.refresh_from_db()
    assert comment.text == "Updated comment"


@pytest.mark.django_db
def test_viewer_cannot_update_foreign_comment(
    viewer_client,
    another_comment,
):
    response = viewer_client.patch(
        f"/api/posts/{another_comment.post.id}/comments/{another_comment.id}/",
        {
            "text": "Hacked",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_can_update_any_comment(
    admin_client,
    comment,
):
    response = admin_client.patch(
        f"/api/posts/{comment.post.id}/comments/{comment.id}/",
        {
            "text": "Updated by Admin",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    comment.refresh_from_db()
    assert comment.text == "Updated by Admin"


# ===== DELETE =====


@pytest.mark.django_db
def test_admin_can_delete_any_comment(
    admin_client,
    comment,
):
    response = admin_client.delete(
        f"/api/posts/{comment.post.id}/comments/{comment.id}/"
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not Comment.objects.filter(id=comment.id).exists()
