# Generated by Django 4.1.5 on 2023-02-12 14:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0031_event_vehicle_alter_event_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='Vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='final.vehicle'),
        ),
    ]
