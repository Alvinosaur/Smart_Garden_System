# Generated by Django 2.0.5 on 2018-05-31 02:43

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('see_data', '0005_auto_20180530_1448'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Owners',
            new_name='Owner',
        ),
        migrations.RenameModel(
            old_name='Plants',
            new_name='Plant',
        ),
    ]
