# Generated by Django 4.1.5 on 2023-02-01 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0006_alter_api_vehicle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='anticipation',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='braking',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='coasting',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='idling',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='speedAdaption',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='standstill',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='total_score',
        ),
    ]