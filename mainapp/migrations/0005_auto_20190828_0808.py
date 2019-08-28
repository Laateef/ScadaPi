# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-08-28 08:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20190828_0806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_1',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_2',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_3',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_4',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_5',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_6',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_7',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='temperature',
            name='thermistor_8',
            field=models.DecimalField(decimal_places=1, max_digits=4, null=True),
        ),
    ]
