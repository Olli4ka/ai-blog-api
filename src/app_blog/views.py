from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets

from .models import Comment, Post
from .serializers import (
    CommentSerializer,
    CommentWriteSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostWriteSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related(
        "author"
    ).prefetch_related(
        "comments__author"
    )

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        return PostWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentListCreateAPIView(generics.ListCreateAPIView):

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


class CommentRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs["post_id"]
        )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return CommentSerializer

        return CommentWriteSerializer
