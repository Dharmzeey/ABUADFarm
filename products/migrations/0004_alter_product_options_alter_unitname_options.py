# Generated by Django 4.0.6 on 2022-08-12 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['unit']},
        ),
        migrations.AlterModelOptions(
            name='unitname',
            options={'ordering': ['name']},
        ),
    ]
