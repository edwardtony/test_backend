# Generated by Django 2.1.2 on 2018-12-10 03:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0041_auto_20181209_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='empresafocal',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 11, 22, 32, 39, 735285)),
        ),
    ]
