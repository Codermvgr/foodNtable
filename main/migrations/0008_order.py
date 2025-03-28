# Generated by Django 3.2.5 on 2021-09-01 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(blank=True, max_length=100)),
                ('payer_id', models.CharField(blank=True, max_length=100)),
                ('ordered_on', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.dish')),
            ],
            options={
                'verbose_name_plural': 'Order Table',
            },
        ),
    ]
