# Generated by Django 4.1.5 on 2023-02-02 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0009_user_company_name_vehicle_last_data_upload'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='last_data_upload',
        ),
    ]
