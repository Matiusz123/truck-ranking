# Generated by Django 4.1.5 on 2023-02-02 20:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0011_vehicle_last_data_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='last_data_upload',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 20, 9, 26, 975693)),
        ),
    ]
