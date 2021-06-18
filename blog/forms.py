from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

    def clean(self):
        cleaned_data = super().clean()
        slug = slugify(cleaned_data['title'])
        slug_posts = Post.objects.filter(slug=slug)
        if slug_posts and slug_posts.first().id != self.instance.id:
            raise ValidationError(
                "Current Title would create a non-unique 'slug'"
            )
        return cleaned_data
