# Generated by Django 4.0.6 on 2022-08-20 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_goods_add_feedback_goods_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='feedback_read',
            field=models.BooleanField(default=False),
        ),
    ]
