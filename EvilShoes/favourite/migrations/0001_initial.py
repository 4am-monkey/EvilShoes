# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-11-09 15:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0004_merge_20191107_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='商品ID')),
                ('name', models.CharField(max_length=180, verbose_name='商品名')),
                ('description', models.TextField(verbose_name='商品描述')),
                ('images', models.ImageField(blank=True, null=True, upload_to='commodity/', verbose_name='商品图片')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserInfo')),
            ],
            options={
                'verbose_name': '收藏商品',
                'verbose_name_plural': '收藏商品',
                'db_table': 'favourite',
            },
        ),
    ]