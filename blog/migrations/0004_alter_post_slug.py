# Generated by Django 3.2.4 on 2021-06-17 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_slug_populate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
