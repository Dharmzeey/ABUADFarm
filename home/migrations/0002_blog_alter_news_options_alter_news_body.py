# Generated by Django 4.0.6 on 2022-10-05 19:39

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='blog')),
                ('body', ckeditor.fields.RichTextField()),
                ('date_created', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterField(
            model_name='news',
            name='body',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
