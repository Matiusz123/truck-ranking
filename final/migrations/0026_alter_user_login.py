# Generated by Django 4.1.5 on 2023-02-09 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0025_remove_user_date_joined_remove_user_hide_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]