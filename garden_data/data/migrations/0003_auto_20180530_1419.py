# Generated by Django 2.0.5 on 2018-05-30 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('see_data', '0002_auto_20180529_0757'),
    ]

    operations = [
        migrations.AddField(
            model_name='plants',
            name='image',
            field=models.CharField(default='http://www.ciaoimports.com/assets/images/Strawberry.jpg', max_length=100),
        ),
        migrations.AddField(
            model_name='plants',
            name='instance',
            field=models.CharField(default='plant1', max_length=253),
        ),
        migrations.AddField(
            model_name='plants',
            name='species',
            field=models.CharField(default='Strawberry', max_length=250),
        ),
    ]