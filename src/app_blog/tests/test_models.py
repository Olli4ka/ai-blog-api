import pytest

from app_blog.models import Comment, Post

# ===== Post model =====


@pytest.mark.django_db
def test_post_str(post):
    assert str(post) == post.title


@pytest.mark.django_db
def test_post_ordering(editor_user):
    older = Post.objects.create(
        title="Older post",
        content="Old content",
        category="AI",
        image_url="",
        author=editor_user,
    )

    newer = Post.objects.create(
        title="Newer post",
        content="New content",
        category="AI",
        image_url="",
        author=editor_user,
    )

    posts = list(Post.objects.all())

    assert posts[0] == newer
    assert posts[1] == older


# ===== Comment model =====


@pytest.mark.django_db
def test_comment_str(comment):
    expected = f"{comment.author.username}: {comment.text[:30]}"
    assert str(comment) == expected


@pytest.mark.django_db
def test_comment_ordering(post, viewer_user):
    older = Comment.objects.create(
        text="Older comment",
        post=post,
        author=viewer_user,
    )

    newer = Comment.objects.create(
        text="Newer comment",
        post=post,
        author=viewer_user,
    )

    comments = list(Comment.objects.all())

    assert comments[0] == newer
    assert comments[1] == older
