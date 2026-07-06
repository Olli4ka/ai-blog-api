from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .models import Comment, Post
from .serializers import (
    CommentSerializer,
    CommentWriteSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostWriteSerializer,
)
from .permissions import (
    IsEditorOrAdmin,
    IsOwnerOrAdmin,
    IsViewerOrHigher,
)


@extend_schema(tags=["Posts"])
class PostViewSet(viewsets.ModelViewSet):
    filterset_fields = ["category", "author"]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "title"]

    queryset = Post.objects.select_related("author").prefetch_related(
        "comments__author"
    )

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        if self.action == "create":
            return [IsEditorOrAdmin()]

        return [
            IsEditorOrAdmin(),
            IsOwnerOrAdmin(),
        ]

    @extend_schema(
        summary="Retrieve all blog posts",
        description="Returns a paginated list of AI blog posts.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve a blog post",
        description="Returns detailed information about a single post, including comments.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create a new blog post",
        description="Creates a new blog post. Authentication is required.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Replace a blog post",
        description="Replaces an existing blog post. Authentication is required.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update a blog post",
        description="Updates part of an existing blog post. Authentication is required.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a blog post",
        description="Deletes an existing blog post. Authentication is required.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return PostWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentListCreateAPIView(generics.ListCreateAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [IsViewerOrHigher()]

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs["post_id"]
        ).select_related("author")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer

        return CommentWriteSerializer

    def perform_create(self, serializer):
        post = get_object_or_404(
            Post,
            pk=self.kwargs["post_id"],
        )

        serializer.save(
            post=post,
            author=self.request.user,
        )


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]

        return [
            IsViewerOrHigher(),
            IsOwnerOrAdmin(),
        ]

    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs["post_id"]
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer

        return CommentWriteSerializer
