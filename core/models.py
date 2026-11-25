from django.db import models
from django.conf import settings


class Post(models.Model):
    author_name = models.CharField(
        max_length=100,
        default="Brindha R."
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.author_name} - {self.created_at}"


class Like(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    user_name = models.CharField(
        max_length=100,
        default="Brindha R."
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user_name} liked Post {self.post.id}"


class SavedPost(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="saved_by_users"
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} saved a post"