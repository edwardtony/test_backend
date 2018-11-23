# Generated by Django 2.1.2 on 2018-11-20 08:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_auto_20181118_2225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitude',
            old_name='magnitude',
            new_name='priority',
        ),
        migrations.AlterField(
            model_name='item',
            name='product',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 22, 3, 38, 9, 659804)),
        ),
    ]
