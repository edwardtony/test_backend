# Generated by Django 2.1.2 on 2018-11-25 20:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20181125_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='focal',
            name='empresa_focal',
        ),
        migrations.RemoveField(
            model_name='help',
            name='focal',
        ),
        migrations.AddField(
            model_name='help',
            name='RUC_or_DNI',
            field=models.CharField(default=0, max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='help',
            name='empresa_focal',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='user.EmpresaFocal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='help',
            name='name',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 27, 15, 51, 25, 543021)),
        ),
        migrations.DeleteModel(
            name='Focal',
        ),
    ]
