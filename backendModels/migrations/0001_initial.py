# Generated by Django 2.1.3 on 2018-11-28 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuantitativeLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=2, max_length=100)),
                ('similarEuc', models.FloatField(default=0)),
                ('urlArgsEntropy', models.FloatField(default=0)),
                ('abnormalTimeProbability', models.FloatField(default=0)),
                ('sameArgsDiversity', models.FloatField(default=0)),
                ('webClassify', models.FloatField(default=0)),
                ('predict_label', models.IntegerField(default=0)),
                ('label', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UrlArgsTestMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=2, max_length=100)),
                ('args', models.TextField(null=True)),
                ('method1', models.TextField(null=True)),
                ('method2', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrlLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=2, max_length=100)),
                ('urlArgs', models.TextField(null=True)),
                ('times', models.TextField(null=True)),
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
        migrations.AddField(
            model_name='quantitativelog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backendModels.User'),
        ),
    ]
