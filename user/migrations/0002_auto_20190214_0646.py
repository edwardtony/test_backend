# Generated by Django 2.1.2 on 2019-02-14 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solicitude',
            name='authority',
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2019, 2, 16, 6, 46, 24, 456397)),
        ),
    ]
