# Generated by Django 2.0.5 on 2018-05-31 03:00

from django.db import migrations, models
import django.db.models.deletion
import see_data.models


class Migration(migrations.Migration):

    dependencies = [
        ('see_data', '0008_owner_plant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='plant',
            field=models.ForeignKey(default=see_data.models.Plant, on_delete=django.db.models.deletion.CASCADE, to='see_data.Plant'),
        ),
    ]
