# Generated by Django 2.1.2 on 2018-11-15 16:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_auto_20181104_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 17, 11, 4, 21, 307568)),
        ),
    ]
