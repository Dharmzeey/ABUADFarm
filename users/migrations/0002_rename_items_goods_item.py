# Generated by Django 4.0.6 on 2022-07-17 22:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='items',
            new_name='item',
        ),
    ]
