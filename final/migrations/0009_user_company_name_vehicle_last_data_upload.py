# Generated by Django 4.1.5 on 2023-02-02 20:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0008_remove_vehiclesinfleet_amount_fleet_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(default='No Company name', max_length=40),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='last_data_upload',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 20, 7, 38, 76906)),
        ),
    ]