# Generated by Django 5.1.6 on 2025-02-27 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_restaurant_cuisine_type_restaurant_price_for_two_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='is_open',
            field=models.BooleanField(default=True),
        ),
    ]
