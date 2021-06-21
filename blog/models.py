from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def unpublish(self):
        self.published_date = None
        self.save()

    def page_title(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.validate_unique()
        super().save(*args, **kwargs)

        if not hasattr(self, 'page_hits'):
            PageHitData.objects.create(post=self)

    def __str__(self):
        return self.title


class PageHitData(models.Model):
    post = models.OneToOneField(
        'Post',
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='page_hits',
    )
    count = models.PositiveIntegerField(default=0)
