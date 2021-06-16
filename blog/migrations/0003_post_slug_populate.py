from django.db import migrations
from django.utils.text import slugify


def resave_posts(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for post in Post.objects.all():
        post.slug = slugify(post.title)
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_slug'),
    ]

    operations = [
        migrations.RunPython(resave_posts),
    ]
