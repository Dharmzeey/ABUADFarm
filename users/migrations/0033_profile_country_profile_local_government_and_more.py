# Generated by Django 4.1.2 on 2022-11-07 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0032_country_remove_profile_city_remove_profile_state_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="country",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner_country",
                to="users.country",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profile",
            name="local_government",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner_lga",
                to="users.lga",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="profile",
            name="state",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="owner_state",
                to="users.state",
            ),
            preserve_default=False,
        ),
    ]