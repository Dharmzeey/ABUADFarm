# Generated by Django 4.1.2 on 2022-10-09 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_blog_alter_news_options_alter_news_body"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="news",
            name="slug",
            field=models.SlugField(blank=True, null=True),
        ),
    ]
