# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-10 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodity', '0004_auto_20191110_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodityinfo',
            name='storage',
            field=models.IntegerField(default=1000, verbose_name='库存'),
        ),
    ]
