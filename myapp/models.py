from django.db import models


class Post(models.Model):
    """A board post (table name: myapp_post).

    The content is stored exactly as the user typed it, including any HTML or
    <script> tags. Storing raw input is fine; the XSS risk appears only when a
    template later prints it WITHOUT escaping (see the vulnerable board view).
    """

    author = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.content[:20]}"
