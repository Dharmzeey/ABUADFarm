# Generated by Django 4.0.6 on 2022-08-15 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_profile_sex'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10),
        ),
    ]
