# Generated by Django 4.1.5 on 2023-02-01 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0005_api'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='final.vehicle'),
        ),
    ]
