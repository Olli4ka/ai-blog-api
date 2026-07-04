from rest_framework import serializers

from .models import Comment, Post


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author",
            "category",
            "created_at",
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "created_at",
        )


class PostDetailSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source="author.username", read_only=True)

    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author",
            "category",
            "image_url",
            "created_at",
            "updated_at",
            "comments",
        ]


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "image_url",
        ]


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]
