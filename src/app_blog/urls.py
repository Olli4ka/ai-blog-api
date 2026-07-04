from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    PostViewSet,
)

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:post_id>/comments/",
        CommentListCreateAPIView.as_view(),
        name="comment-list-create",
    ),
    path(
        "posts/<int:post_id>/comments/<int:comment_id>/",
        CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-detail",
    ),
]
