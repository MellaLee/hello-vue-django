# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-15 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UrlLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=2, max_length=100)),
                ('urlArgs', models.CharField(max_length=200, null=True)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userNo', models.IntegerField(default=1)),
                ('ip', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='urllog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backendModels.User'),
        ),
    ]