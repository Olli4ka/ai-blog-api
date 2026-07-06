import pytest
from rest_framework import status


# ===== JWT Authentication =====


@pytest.mark.django_db
def test_user_can_obtain_jwt(api_client, editor_user):
    response = api_client.post(
        "/api/token/",
        {
            "username": editor_user.username,
            "password": "John123456",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_user_cannot_obtain_jwt_with_wrong_password(
    api_client,
    editor_user,
):
    response = api_client.post(
        "/api/token/",
        {
            "username": editor_user.username,
            "password": "WrongPassword",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_user_can_refresh_access_token(api_client, editor_user):
    token_response = api_client.post(
        "/api/token/",
        {
            "username": editor_user.username,
            "password": "John123456",
        },
        format="json",
    )

    refresh = token_response.data["refresh"]

    response = api_client.post(
        "/api/token/refresh/",
        {
            "refresh": refresh,
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
