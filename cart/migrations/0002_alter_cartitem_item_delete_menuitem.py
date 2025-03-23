# Generated by Django 5.1.6 on 2025-03-10 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('restaurant', '0010_item_is_available_restaurant_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.item'),
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
    ]
