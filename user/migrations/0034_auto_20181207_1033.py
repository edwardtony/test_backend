# Generated by Django 2.1.2 on 2018-12-07 15:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0033_auto_20181205_1120'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('image', models.CharField(max_length=14)),
            ],
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 9, 10, 33, 0, 366554)),
        ),
    ]