# Generated by Django 4.1.5 on 2023-02-03 02:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0013_remove_vehicle_user_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='final.user'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='last_data_upload',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 3, 2, 28, 48, 154023)),
        ),
    ]