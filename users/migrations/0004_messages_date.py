# Generated by Django 4.0.6 on 2022-07-23 23:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
