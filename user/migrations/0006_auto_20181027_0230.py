# Generated by Django 2.1.2 on 2018-10-27 07:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_agent_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='date',
            field=models.DateTimeField(default=datetime.datetime),
        ),
    ]