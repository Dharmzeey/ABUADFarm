# Generated by Django 4.0.6 on 2022-08-15 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_goods_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='sex',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=10),
        ),
    ]