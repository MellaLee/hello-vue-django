# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-16 12:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendModels', '0002_auto_20180516_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='userNo',
            field=models.IntegerField(default=1),
        ),
    ]