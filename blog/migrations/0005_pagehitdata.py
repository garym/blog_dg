# Generated by Django 3.2.4 on 2021-06-20 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageHitData',
            fields=[
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='page_hits', serialize=False, to='blog.post')),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]