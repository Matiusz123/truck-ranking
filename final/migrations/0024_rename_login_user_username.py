# Generated by Django 4.1.5 on 2023-02-08 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('final', '0023_user_date_joined_user_hide_email_user_is_active_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='login',
            new_name='username',
        ),
    ]
