import pytest

from app_blog.serializers import (
    CommentSerializer,
    CommentWriteSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostWriteSerializer,
)

# ===== Post serializers =====


@pytest.mark.django_db
def test_post_list_serializer(post):
    serializer = PostListSerializer(post)

    assert serializer.data["title"] == post.title
    assert serializer.data["author"] == post.author.username
    assert serializer.data["category"] == post.category


@pytest.mark.django_db
def test_post_detail_serializer(post, comment):
    serializer = PostDetailSerializer(post)

    assert serializer.data["title"] == post.title
    assert serializer.data["content"] == post.content
    assert serializer.data["author"] == post.author.username

    assert len(serializer.data["comments"]) == 1
    assert serializer.data["comments"][0]["text"] == comment.text


@pytest.mark.django_db
def test_post_write_serializer_valid():
    serializer = PostWriteSerializer(
        data={
            "title": "AI News",
            "content": "New AI article",
            "category": "AI",
            "image_url": "",
        }
    )

    assert serializer.is_valid()


# ===== Comment serializers =====


@pytest.mark.django_db
def test_comment_serializer(comment):
    serializer = CommentSerializer(comment)

    assert serializer.data["text"] == comment.text
    assert serializer.data["author"] == comment.author.username


@pytest.mark.django_db
def test_comment_write_serializer_valid():
    serializer = CommentWriteSerializer(
        data={
            "text": "Interesting article!",
        }
    )

    assert serializer.is_valid()
