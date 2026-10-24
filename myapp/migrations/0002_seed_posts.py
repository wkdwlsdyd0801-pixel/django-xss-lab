# Inserts sample posts when you run `python manage.py migrate`.
# One post carries a <script> payload so the stored-XSS demo works right away.
from django.db import migrations

POSTS = [
    ("student", "첫 글입니다. 반갑습니다!"),
    ("guest", "질문 있어요. 실행 방법이 궁금합니다."),
    # Stored-XSS payload: harmless alert() that proves the script ran.
    ("attacker", "<script>alert('stored XSS')</script>"),
]


def seed(apps, schema_editor):
    Post = apps.get_model("myapp", "Post")
    for author, content in POSTS:
        Post.objects.get_or_create(author=author, content=content)


def unseed(apps, schema_editor):
    # Lets `migrate myapp 0001` roll the seed back.
    Post = apps.get_model("myapp", "Post")
    Post.objects.filter(content__in=[c for _, c in POSTS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
