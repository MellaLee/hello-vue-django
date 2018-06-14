from django.db import models

# Create your models here.

class User(models.Model):
    userNo = models.IntegerField(default=0x01)
    ip = models.CharField(null=True, max_length = 100)

class UrlLog(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(default=0x02, max_length = 100)
    urlArgs = models.TextField(null=True)
    time = models.DateTimeField()

class  QuantitativeLog(models.Model):
    user = models.ForeignKey(User)
    url = models.CharField(default=0x02, max_length = 100)
    similarEuc = models.FloatField(default=0x00)
    urlArgsEntropy = models.FloatField(default=0x00)
    abnormalTimeProbability = models.FloatField(default=0x00)
    sameArgsDiversity = models.FloatField(default=0x00)
    webClassify = models.FloatField(default=0x00)

class UrlArgsTestMethod(models.Model):
    url = models.CharField(default=0x02, max_length = 100)
    args = models.TextField(null=True)
    method1 = models.TextField(null=True)
    method2 = models.TextField(null=True)