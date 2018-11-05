# Generated by Django 2.1.2 on 2018-11-02 03:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_auto_20181029_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='phone',
            field=models.CharField(error_messages={'unique': 'Este teléfono ya ha sido usado'}, max_length=9),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2018, 11, 4, 3, 11, 15, 425924)),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='district',
            field=models.CharField(choices=[('Distrito 1', 'Distrito 1'), ('Distrito 2', 'Distrito 2'), ('Distrito 3', 'Distrito 3'), ('Distrito 4', 'Distrito 4'), ('Distrito 5', 'Distrito 5')], max_length=20),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='emergency',
            field=models.CharField(choices=[('Emergencia 1', 'Emergencia 1'), ('Emergencia 2', 'Emergencia 2'), ('Emergencia 3', 'Emergencia 3'), ('Emergencia 4', 'Emergencia 4'), ('Emergencia 5', 'Emergencia 5')], max_length=20),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='magnitude',
            field=models.CharField(choices=[('Magnitud 1', 'Magnitud 1'), ('Magnitud 2', 'Magnitud 2'), ('Magnitud 3', 'Magnitud 3'), ('Magnitud 4', 'Magnitud 4'), ('Magnitud 5', 'Magnitud 5')], max_length=20),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='province',
            field=models.CharField(choices=[('Provincia 1', 'Provincia 1'), ('Provincia 2', 'Provincia 2'), ('Provincia 3', 'Provincia 3'), ('Provincia 4', 'Provincia 4'), ('Provincia 5', 'Provincia 5')], max_length=20),
        ),
        migrations.AlterField(
            model_name='solicitude',
            name='region',
            field=models.CharField(choices=[('Región 1', 'Región 1'), ('Región 2', 'Región 2'), ('Región 3', 'Región 3'), ('Región 4', 'Región 4'), ('Región 5', 'Región 5')], max_length=20),
        ),
    ]
