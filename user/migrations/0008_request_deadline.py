# Generated by Django 2.1.2 on 2018-10-27 07:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20181027_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 29, 2, 36, 35, 777862)),
        ),
    ]