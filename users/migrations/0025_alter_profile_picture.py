# Generated by Django 4.0.6 on 2022-08-21 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_rename_picture_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default="{% static 'images/avatar.png' %}", upload_to=''),
        ),
    ]
