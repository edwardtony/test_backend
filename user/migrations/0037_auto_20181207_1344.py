# Generated by Django 2.1.2 on 2018-12-07 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0036_auto_20181207_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='theme',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 9, 13, 44, 50, 587725)),
        ),
    ]