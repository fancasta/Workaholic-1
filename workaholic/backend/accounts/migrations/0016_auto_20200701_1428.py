# Generated by Django 3.0.6 on 2020-07-01 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_notification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='notification',
            new_name='message',
        ),
    ]
