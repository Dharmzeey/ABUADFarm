# Generated by Django 4.0.6 on 2022-08-19 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_goods_note_customerfeedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goods',
            old_name='add_note',
            new_name='add_description',
        ),
        migrations.RenameField(
            model_name='goods',
            old_name='note',
            new_name='description',
        ),
    ]