# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-26 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendModels', '0007_quantitativelog_urlsimilaroriginseries'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantitativelog',
            name='similarStd',
            field=models.FloatField(default=0),
        ),
    ]