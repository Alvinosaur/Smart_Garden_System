# Generated by Django 2.0.5 on 2018-05-31 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('see_data', '0009_auto_20180531_0300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='owner',
            name='plant',
        ),
    ]
