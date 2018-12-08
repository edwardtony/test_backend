# Generated by Django 2.1.2 on 2018-11-30 15:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0027_auto_20181130_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='agent',
            name='code',
            field=models.CharField(default='AUT1234567', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresafocal',
            name='code',
            field=models.CharField(default='PFO1234567', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 2, 10, 48, 13, 638063)),
        ),
    ]