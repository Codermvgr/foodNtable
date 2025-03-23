# Generated by Django 3.2.5 on 2021-08-26 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_category_team'),
    ]

    operations = [
        
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(upload_to='dishes/%Y/%m/%d')),
                ('ingredients', models.TextField()),
                ('details', models.TextField(blank=True)),
                ('price', models.FloatField()),
                ('discounted_price', models.FloatField(blank=True)),
                ('is_available', models.BooleanField(default=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
            options={
                'verbose_name_plural': 'Dish Table',
            },
        ),
    ]
