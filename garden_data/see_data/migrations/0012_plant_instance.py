# Generated by Django 2.0.5 on 2018-05-31 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('see_data', '0011_auto_20180531_0314'),
    ]

    operations = [
        migrations.AddField(
            model_name='plant',
            name='instance',
            field=models.CharField(default='plant1', max_length=50),
        ),
    ]
