# Generated by Django 2.0.5 on 2018-05-31 14:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('see_data', '0015_auto_20180531_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='start_date',
            field=models.DateField(default=datetime.date(2018, 5, 31)),
        ),
    ]
