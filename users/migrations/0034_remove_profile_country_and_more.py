# Generated by Django 4.1.2 on 2022-11-09 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0033_profile_country_profile_local_government_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="country",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="local_government",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="state",
        ),
    ]
