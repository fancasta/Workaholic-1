# Generated by Django 3.0.6 on 2020-07-08 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20200707_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='last_modified_item',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
