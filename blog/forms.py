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
        if Post.objects.filter(slug=slug):
            raise ValidationError(
                "Current Title would create a non-unique 'slug'"
            )
