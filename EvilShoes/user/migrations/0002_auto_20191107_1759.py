# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-07 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='login_time',
            field=models.DateTimeField(verbose_name='登录时间'),
        ),
    ]
