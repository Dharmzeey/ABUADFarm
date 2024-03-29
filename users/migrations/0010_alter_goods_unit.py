# Generated by Django 4.0.6 on 2022-08-13 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_product_options_alter_unitname_options'),
        ('users', '0009_goods_unit_alter_goods_add_note_alter_goods_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_good', to='products.unitname'),
        ),
    ]
