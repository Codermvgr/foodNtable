# Generated by Django 3.2.5 on 2021-08-30 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_profile_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='contact_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
