# Generated by Django 4.1.5 on 2023-02-06 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0020_vehicle_average_fuel_consumption_from_update_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='average_fuel_consumption_from_update',
            field=models.FloatField(default=0),
        ),
    ]