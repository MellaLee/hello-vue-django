from django.db import models

# Create your models here.

class User(models.Model):
    userNo = models.IntegerField(default=0x01)
    ip = models.CharField(null=True, max_length = 100)

# label为0表示善意访问, 人工标记结果
# cluster_label为0表示善意访问, 聚类标记结果
# predict_label为0表示善意访问, 预测标记结果
class  QuantitativeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(default=0x02, max_length = 100)
    similarEuc = models.FloatField(default=0x00)
    urlArgsEntropy = models.FloatField(default=0x00)
    abnormalTimeProbability = models.FloatField(default=0x00)
    sameArgsDiversity = models.FloatField(default=0x00)
    webClassify = models.FloatField(default=0x00)
    predict_label = models.IntegerField(default=0x00)
    label = models.IntegerField(default=0x00)
    cluster_label = models.IntegerField(default=0x00)

# mark为1表示需要标记
class UrlLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.CharField(default=0x02, max_length = 100)
    urlArgs = models.TextField(null=True)
    times = models.TextField(null=True)
    mark = models.IntegerField(default=0x01)

class UrlArgsTestMethod(models.Model):
    url = models.CharField(default=0x02, max_length = 100)
    args = models.TextField(null=True)
    method1 = models.TextField(null=True)
    method2 = models.TextField(null=True)